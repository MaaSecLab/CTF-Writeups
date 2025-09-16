This is just a template, you don't need to follow it. Feel free to change it as you see fit.
## Name
Free Candy
### Problem Description
Woah, free candy... sign me up!
### Solution

from pwn import remote, context
import re, json, base64, hashlib, csv, os, time, argparse

context.log_level = "warning"

HOST, PORT = "0.cloud.chals.io", 19521

P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
Gx= 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy= 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
G = (Gx, Gy)

def ensure_csv(path: str):
    if not os.path.exists(path):
        with open(path, "w", newline="") as f:
            csv.writer(f).writerow(
                ["chain_id","kind","index","ticket_id","ticket_id_mod_N","r","s","z","base64"]
            )

def append_csv(path: str, chain_id: str, kind: str, index: int, tid: int, r: int, s: int, z: int, b64: str):
    with open(path, "a", newline="") as f:
        csv.writer(f).writerow([chain_id, kind, index, str(tid), str(tid % N), str(r), str(s), str(z), b64])

def inv(a, m): return pow(a % m, -1, m)

def ec_add(P1, P2):
    if P1 is None: return P2
    if P2 is None: return P1
    x1,y1 = P1; x2,y2 = P2
    if x1 == x2 and (y1 + y2) % P == 0: return None
    if P1 == P2:
        lam = (3*x1*x1) * inv(2*y1, P) % P
    else:
        lam = (y2 - y1) * inv((x2 - x1) % P, P) % P
    x3 = (lam*lam - x1 - x2) % P
    y3 = (lam*(x1 - x3) - y1) % P
    return (x3, y3)

def ec_mul(k, Pt):
    if k % N == 0 or Pt is None: return None
    k %= N
    Q = None; A = Pt
    while k:
        if k & 1: Q = ec_add(Q, A)
        A = ec_add(A, A)
        k >>= 1
    return Q

def sha256_int(m: bytes) -> int:
    return int.from_bytes(hashlib.sha256(m).digest(), "big") % N

def canon_payload_bytes(tid: int) -> bytes:
    return json.dumps({"ticket_id": tid}, separators=(',', ':'), sort_keys=True).encode()

def parse_ticket_b64(b64s: str):
    raw = base64.b64decode(b64s, validate=True)
    t = json.loads(raw.decode())
    tid = int(t["payload"]["ticket_id"])
    sig = bytes.fromhex(t["signature"]); assert len(sig) == 64
    r = int.from_bytes(sig[:32], "big")
    s = int.from_bytes(sig[32:], "big")
    msg = canon_payload_bytes(tid)
    z = sha256_int(msg)
    return tid, r, s, z, msg, b64s

def recv_menu(io):
    io.recvuntil(b"Choose an action:")
    io.recvline(); io.recvline()

def get_first(io) -> str:
    recv_menu(io)
    io.sendline(b"1")
    for _ in range(10):
        line = io.recvline(timeout=2)
        if not line: break
        s = line.strip().decode()
        if re.fullmatch(r'[A-Za-z0-9+/=]+', s):
            return s
    raise RuntimeError("did not receive base64 ticket")

def claim_and_maybe_next(io, b64: str):
    recv_menu(io)
    io.sendline(b"2")
    io.recvuntil(b"Enter your ticket:")
    io.sendline(b64.encode())
    for _ in range(20):
        line = io.recvline(timeout=2)
        if not line: break
        s = line.decode().strip()
        if "brand new ticket:" in s:
            cand = s.split(":", 1)[1].strip()
            if re.fullmatch(r'[A-Za-z0-9+/=]+', cand):
                return cand
        if s.startswith("You won some free candy") or "Invalid ticket" in s:
            return None
    return None

def recover_AB(u0,u1,u2,u3):
    denom = (u0*u2 - u1*u1) % N
    if denom == 0: raise RuntimeError("singular system for A,B")
    B = ((u1*u3 - u2*u2) * inv(denom, N)) % N
    A = ((u2 + B*u0) * inv(u1, N)) % N
    return A,B

def recover_d(A,B, trip):
    (r0,s0,z0),(r1,s1,z1),(r2,s2,z2) = trip
    a0 = r0 * inv(s0, N) % N; b0 = z0 * inv(s0, N) % N
    a1 = r1 * inv(s1, N) % N; b1 = z1 * inv(s1, N) % N
    a2 = r2 * inv(s2, N) % N; b2 = z2 * inv(s2, N) % N
    num = (A*b1 - B*b0 - b2) % N
    den = (a2 - A*a1 + B*a0) % N
    if den == 0: raise RuntimeError("zero denominator while solving for d")
    return num * inv(den, N) % N

def forge(d: int, msg: bytes):
    z = sha256_int(msg)
    k = 1
    while True:
        R = ec_mul(k, G)
        if R is None: k += 1; continue
        r = R[0] % N
        if r == 0: k += 1; continue
        s = (inv(k, N) * (z + r*d)) % N
        if s == 0: k += 1; continue
        return r, s

def make_b64(tid: int, r: int, s: int) -> str:
    sig = r.to_bytes(32,"big") + s.to_bytes(32,"big")
    obj = {"payload":{"ticket_id": tid}, "signature": sig.hex()}
    raw = json.dumps(obj, separators=(',', ':'), sort_keys=True).encode()
    return base64.b64encode(raw).decode()

def main():
    ap = argparse.ArgumentParser(description="Lucky Shop solver (same-session submit, CSV logging)")
    ap.add_argument("--csv", default="tickets.csv", help="CSV output path (default: tickets.csv)")
    args = ap.parse_args()

    ensure_csv(args.csv)
    chain_id = f"chain_{int(time.time()*1000)}"

    while True:
        io = remote(HOST, PORT)
        try:
            chain = []
            b64 = get_first(io)
            tid,r,s,z,msg = parse_ticket_b64(b64)[:5]
            chain.append((tid,r,s,z,msg,b64))
            while len(chain) < 4 and tid % 2 == 0:
                nb64 = claim_and_maybe_next(io, b64)
                if not nb64: break
                tid,r,s,z,msg = parse_ticket_b64(nb64)[:5]
                chain.append((tid,r,s,z,msg,nb64))
                b64 = nb64

            if len(chain) < 4:
                io.close()
                continue  

            for idx, (tid,r,s,z,_m,b64) in enumerate(chain):
                append_csv(args.csv, chain_id, "harvested", idx, tid, r, s, z, b64)
            print("[*] harvested 4 tickets")

            (u0,r0,s0,z0,_m0,_b0) = chain[0]
            (u1,r1,s1,z1,_m1,_b1) = chain[1]
            (u2,r2,s2,z2,_m2,_b2) = chain[2]
            (u3,r3,s3,z3,_m3,_b3) = chain[3]

            A,B = recover_AB(u0 % N, u1 % N, u2 % N, u3 % N)
            print(f"[*] A={A}\n[*] B={B}")
            d = recover_d(A,B, [(r0,s0,z0),(r1,s1,z1),(r2,s2,z2)])
            print(f"[*] d={d}")

            target_tid = int.from_bytes(hashlib.sha256(b"I'd like the flag please").digest(), "big")
            target_msg = canon_payload_bytes(target_tid)
            fr, fs = forge(d, target_msg)
            forged_b64 = make_b64(target_tid, fr, fs)
            append_csv(args.csv, chain_id, "forged", -1, target_tid, fr, fs, sha256_int(target_msg), forged_b64)
            print(f"[*] forged ticket ready; logging to {args.csv}")

            recv_menu(io)
            io.sendline(b"2")
            io.recvuntil(b"Enter your ticket:")
            io.sendline(forged_b64.encode())
            out = io.recvall(timeout=5).decode(errors="ignore")
            print(out.strip())
            io.close()
            break

        except Exception as e:
            try: io.close()
            except: pass
            continue

if __name__ == "__main__":
    import time, argparse
    main()

