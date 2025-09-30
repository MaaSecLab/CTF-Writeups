## Name
Hail Mary

### Problem Description
Dr. Ryland Grace is in a tough spot! He has been tasked with performing an experiment on some "taumoeba" (Amoebas collected in the Tau Ceti system). He needs to try to breed them to meet certain biological parameters to ensure their survival when they return to Earth. See if you can help guide the experiments to find the optimal genetic code needed and you will be rewarded!

nc chal.sunshinectf.games 25201

### Solution
## Challenge Description

The prompt said:

> “Welcome to the NASA Evolutionary Biology Lab! … You have **100 generations** to reach an average **95.0%** that survive. Submit populations of 100 gene samples, each **10 floats (0–1)** in JSON.”

Input format:
```json
{"samples":[[f1,...,f10], ..., [f1,...,f10]]}
```

The service prints a line per generation. Critically, it also emits a JSON blob like:
```json
{"generation": 17, "average": 0.6840465, "scores": [ ...100 floats... ]}
```
So the `average` is **0..1**, and `scores` are per-sample fitnesses.

---

## Approach

I started with a simple hill‑climber that cloned a single genome 100× per generation. That worked for a percent‑text output, but it wasted the server’s ability to evaluate 100 different candidates at once.

When I noticed the service returning JSON with **per-sample scores**, I switched to a proper **batch evolutionary strategy**:

1. **Population (N=100)** per generation, each genome has **D=10** floats clipped in \[0,1].  
2. **Gen 1:** Latin Hypercube Sampling (LHS) for broad coverage.  
3. **Selection:** sort by fitness; keep top **μ=20** elites.  
4. **Recombination:** compute a new mean as a **log‑rank weighted** average of elites (CMA‑style weights).  
5. **Step‑size (σ) adaptation:** pull σ toward the elites’ per‑dimension spread (robust in box domains), with a blend that shrinks on stalls and expands on improvements.  
6. **Restarts:** if the average stalls for 15 generations, soft‑restart around fresh LHS seeds.
7. **Exit:** when average ≥ 95% (i.e., `avg >= 0.95 * 100 = 95%`).

I also hardened parsing to accept either `%` strings or JSON (`average` + `scores`).

---

## Connectivity Hiccup

Initially I hit `ConnectionRefusedError`. I added a resolver that tries **both IPv4 and IPv6** addresses with retries and small backoff. Once the organizers brought the service back up, it connected cleanly.

---

## Final Solver

```python
# hail_mary_solver.py
import socket, sys, json, re, time, random, argparse
from typing import Optional, List, Tuple

DEFAULT_HOST = "chal.sunshinectf.games"
DEFAULT_PORT = 25201

# --- Parsing helpers -------------------------------------------------------

PERCENT_RE   = re.compile(r"(\d+(?:\.\d+)?)\s*%")
JSON_OBJ_RE  = re.compile(r"\{.*?\}", re.DOTALL)

def recv_all(sock: socket.socket, timeout=0.7) -> str:
    sock.settimeout(timeout)
    chunks = []
    while True:
        try:
            data = sock.recv(65536)
            if not data:
                break
            chunks.append(data.decode("utf-8", errors="replace"))
            time.sleep(0.03)
        except socket.timeout:
            break
    return "".join(chunks)

def parse_feedback(text: str) -> Tuple[Optional[float], Optional[List[float]]]:
    objs = list(JSON_OBJ_RE.finditer(text))
    for m in reversed(objs):
        try:
            obj = json.loads(m.group(0))
            if isinstance(obj, dict):
                avg = obj.get("average", None)
                scores = obj.get("scores", None)
                avg_pct = None
                if isinstance(avg, (int, float)):
                    avg_pct = float(avg) * 100.0 if 0.0 <= avg <= 1.0 else float(avg)
                if isinstance(scores, list) and scores and all(isinstance(v, (int, float)) for v in scores):
                    sc = [float(v) for v in scores]
                    if any(v > 1.0 for v in sc):
                        sc = [max(0.0, min(1.0, v / 100.0)) for v in sc]
                    else:
                        sc = [max(0.0, min(1.0, v)) for v in sc]
                    return avg_pct, sc
                if avg_pct is not None:
                    return avg_pct, None
        except Exception:
            pass
    m = list(PERCENT_RE.finditer(text))
    if m:
        return float(m[-1].group(1)), None
    m2 = re.findall(r'average["\']?\s*[:=]\s*([0-9]*\.?[0-9]+)', text)
    if m2:
        val = float(m2[-1])
        return (val * 100.0 if 0.0 <= val <= 1.0 else val), None
    return None, None

# --- Math helpers ----------------------------------------------------------

def clip01_vec(vec): return [0.0 if v < 0.0 else 1.0 if v > 1.0 else v for v in vec]
def zeros(n): return [0.0] * n
def add(a, b): return [x + y for x, y in zip(a, b)]
def mul(a, k): return [x * k for x in a]
def mean(vs):
    n = len(vs); d = len(vs[0]); out = [0.0]*d
    for v in vs:
        for i, x in enumerate(v): out[i] += x
    return [x / n for x in out]
def stddev(vs):
    n=len(vs); d=len(vs[0]); m=mean(vs); var=[0.0]*d
    for v in vs:
        for i, x in enumerate(v):
            dx = x - m[i]; var[i] += dx*dx
    return [ (var[i]/max(1,n-1))**0.5 for i in range(d) ]

def lhs_pop(pop_size, dim, rng):
    strata = [list((i + rng.random()) / pop_size for i in range(pop_size)) for _ in range(dim)]
    for d in range(dim): rng.shuffle(strata[d])
    return [[strata[d][i] for d in range(dim)] for i in range(pop_size)]

def gaussian_pop(mean_vec, sigma, pop_size, rng):
    d=len(mean_vec); pop=[]
    for _ in range(pop_size):
        v=[mean_vec[i]+rng.gauss(0.0,sigma) for i in range(d)]
        pop.append(clip01_vec(v))
    return pop

def logrank_weights(mu):
    import math
    ws=[math.log(mu+0.5)-math.log(i+1.0) for i in range(mu)]
    s=sum(ws)
    return [w/s for w in ws]

# --- Networking ------------------------------------------------------------

def connect_any(host, port, tries=5, base_timeout=4.0):
    last_err=None
    for attempt in range(1, tries+1):
        try:
            infos=socket.getaddrinfo(host, port, proto=socket.IPPROTO_TCP, type=socket.SOCK_STREAM)
        except Exception as e:
            last_err=e; time.sleep(0.5*attempt); continue
        for fam, socktype, proto, canonname, sockaddr in infos:
            try:
                s=socket.socket(fam, socktype, proto); s.settimeout(base_timeout); s.connect(sockaddr)
                print(f"[connect] Connected to {sockaddr} (family={fam}) on attempt {attempt}."); return s
            except Exception as e:
                last_err=e
                try: s.close()
                except Exception: pass
        time.sleep(min(2.0*attempt,5.0))
    raise OSError(f"Could not connect to {host}:{port}. Last error: {last_err}")

def send_population(sock, samples):
    payload={"samples": samples}
    sock.sendall((json.dumps(payload)+"\n").encode())

# --- Core solver -----------------------------------------------------------

def solve(host, port):
    rng=random.Random(); rng.seed()
    D=10; POP=100; MU=20; MAX_GENS=100; TARGET_PCT=95.0; NO_IMPROVE_RESTART=15
    mean_vec=[0.5]*D; sigma=0.25; best_avg=-1.0; stall=0; gen0_done=False
    with connect_any(host, port) as s:
        banner=recv_all(s, timeout=2.0)
        if banner: sys.stdout.write(banner); sys.stdout.flush()
        for gen in range(1, MAX_GENS+1):
            pop = lhs_pop(POP,D,rng) if not gen0_done else gaussian_pop(mean_vec,sigma,POP,rng)
            send_population(s, pop)
            resp=recv_all(s, timeout=3.0)
            if resp: sys.stdout.write(resp); sys.stdout.flush()
            avg_pct, scores01 = parse_feedback(resp)
            if avg_pct is None or (scores01 is None and not gen0_done):
                more=recv_all(s, timeout=1.0)
                if more: sys.stdout.write(more); sys.stdout.flush()
                avg2, scr2 = parse_feedback(resp+more)
                avg_pct = avg_pct if avg_pct is not None else avg2
                scores01 = scores01 if scores01 is not None else scr2
            if avg_pct is None: avg_pct=0.0
            print(f"[gen {gen}] avg={avg_pct:.2f}%  sigma={sigma:.3f}")
            if avg_pct >= TARGET_PCT:
                print("[*] Reached ≥95%. If a flag printed above, grab it! Exiting."); return
            improved = avg_pct > best_avg + 1e-9
            stall = 0 if improved else stall+1
            if scores01 is None or len(scores01)!=POP:
                step = 0.15 if gen<=5 else 0.07
                mean_vec = clip01_vec([m + rng.gauss(0.0, step) for m in mean_vec])
                sigma = max(0.02, min(0.35, sigma * (1.2 if improved else 0.8)))
                gen0_done=True
                if stall>=NO_IMPROVE_RESTART:
                    mean_vec=[rng.random() for _ in range(D)]; sigma=0.25; stall=0
                continue
            idx=list(range(POP)); idx.sort(key=lambda i: scores01[i], reverse=True)
            elites=[pop[i] for i in idx[:MU]]
            ws=logrank_weights(MU)
            new_mean=zeros(D)
            for w,ind in zip(ws,elites): new_mean=add(new_mean, mul(ind, w))
            spread = stddev(elites); avg_spread = sum(spread)/D
            target_sigma = max(0.03, min(0.30, avg_spread*1.3))
            blend = 0.6 if improved else 0.8
            sigma = max(0.02, min(0.35, blend*sigma + (1.0-blend)*target_sigma))
            mean_vec=new_mean; gen0_done=True
            if stall>=NO_IMPROVE_RESTART:
                seeds = lhs_pop(POP,D,rng); mean_vec = mean(seeds[:MU]); sigma=0.25; stall=0
        print("[!] Max generations reached. Sending one final population...")
        send_population(s, gaussian_pop(mean_vec,sigma,POP,rng))
        tail=recv_all(s, timeout=3.0)
        if tail: sys.stdout.write(tail); sys.stdout.flush()

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--host", default=DEFAULT_HOST)
    ap.add_argument("--port", type=int, default=DEFAULT_PORT)
    args=ap.parse_args()
    try:
        solve(args.host, args.port)
    except KeyboardInterrupt:
        print("\nAborted by user.")
```

---

## Result

It converged quickly; by **gen 18** I saw:
```
[gen 18] avg=94.99%  sigma=0.033
Success! Earth has been saved! Here is your flag: sun{wh4t_4_gr34t_pr0j3ct}



---

## Lessons Learned

- If a judge returns **per-sample scores**, always switch to a **batch** optimizer; cloning a single candidate wastes signal.
- Simple NES/CMA‑ish strategies with log‑rank weights + σ‑adaptation are **easy to implement** and very robust.
- Add resilient network handling (IPv4/IPv6 & retries) early; it saves time during CTFs.
