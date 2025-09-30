## Name
Numbers Game

### Problem Description
Welcome to the Numbers Game! You'll need some luck for this one.
nc chal.sunshinectf.games 25101

### Solution
I reversed the binary, found it seeded `rand()` with `time(NULL)` and constructed a 64‑bit target from three `rand()` calls. By predicting the same `rand()` outputs for likely epoch-second seeds and sending the resulting 64‑bit number to the service, I retrieved the flag.

---

## Recon / Observations

When I ran the service manually with `nc`, I saw:

```
Let's make a deal! If you can guess the number of fingers I am holding up behind my back, I'll let you have my flag.
Hint: I am polydactyl and have 18,466,744,073,709,551,615 fingers.
```

The hint was a red herring. I then loaded the provided `numbers-game` binary into a disassembler and inspected the code paths around input processing, random seeding, and the check that prints the flag.

---

## Reverse engineering notes

While inspecting the binary (static analysis / quick disassembly), I confirmed the following behavior:

- The program calls `srand(time(NULL));`
- It calls `rand()` three times:
  - `r1 = rand();`
  - `r2 = rand();`
  - `r3 = rand();`
- It constructs the 64‑bit `target` as:

```c
target = (uint64_t)r1
       | ((uint64_t)r2 << 31)
       | ((uint64_t)(r3 & 0x3) << 62);
```

Because `rand()` returns up to 31 bits on glibc, the composition effectively places `r1` in bits [0..30], `r2` in bits [31..61], and the lowest 2 bits of `r3` into bits [62..63].

The program reads an unsigned decimal number from the client (`%llu`) and compares it to `target`. If equal, it executes `system("cat flag.txt")`.

Key takeaways:
- The PRNG is the standard `rand()` from glibc, seeded with `time(NULL)`.
- The service accepts **one** guess per connection (it closes after responding).
- The numeric input is decimal only (because of `%llu`).

---

## Exploit strategy

Because `srand(time(NULL))` seeds with the current epoch second, if I can guess the seed (which is usually very close to my local time), I can reproduce the same `rand()` output and reconstruct `target`. The steps are:

1. For a candidate seed `s`, compute:
   - `srand(s); r1 = rand(); r2 = rand(); r3 = rand();`
   - `target = r1 | (r2 << 31) | ((r3 & 3) << 62)`
2. Connect to the service and send `target` as a decimal line.
3. If the server prints the flag, success; if the server replies "WRONG", try a nearby seed (± a few seconds).

Because network and clock skew are possible, I probe a small window around the current epoch-second (I tried ±300 s ordered by proximity to now).

---

## Solver (Python)

I wrote a robust solver that uses local glibc `srand()`/`rand()` via `ctypes` so the outputs match the remote service. Below is the core of the solver I used (cleaned up):

```python
import ctypes, time, socket

HOST = "chal.sunshinectf.games"
PORT = 25101
libc = ctypes.CDLL("libc.so.6")
libc.srand.argtypes = [ctypes.c_uint]
libc.rand.restype = ctypes.c_int

def target_for_seed(seed):
    libc.srand(seed)
    r1 = libc.rand()
    r2 = libc.rand()
    r3 = libc.rand()
    return ((r3 & 0x3) << 62) | ((r2 & 0x7fffffff) << 31) | (r1 & 0x7fffffff)

def try_guess(guess):
    s = socket.create_connection((HOST, PORT), timeout=5)
    try:
        # read banner
        try:
            s.recv(4096)
        except:
            pass
        s.sendall(str(guess).encode() + b"\n")
        # read everything until the server closes
        resp = b""
        while True:
            try:
                data = s.recv(4096)
                if not data:
                    break
                resp += data
            except:
                break
        return resp.decode(errors="ignore")
    finally:
        s.close()

now = int(time.time())
# probe seeds close to now first
offsets = [0]
for d in range(1, 301):
    offsets.extend([-d, d])

for off in offsets:
    seed = now + off
    guess = target_for_seed(seed)
    reply = try_guess(guess)
    if "WRONG" not in reply:
        print("Seed:", seed)
        print("Guess:", guess)
        print("Reply:\n", reply)
        break
```

I ordered seed probes by closeness to `now` so I would find the correct epoch-second quickly.

---

## Results

Using the approach above I successfully retrieved the flag from the remote service. The important bits that made it work:

- Matching the remote PRNG (glibc `rand`) using `ctypes` so my `rand()` output matched the server exactly.
- Accounting for time-based seeding (probing an epoch-second window).
- Reconnecting for every guess because the server closes the socket after answering.

---

## Notes & mitigations

- This is a classic example of why `srand(time(NULL))` + `rand()` is not secure for generating unpredictable values for authentication. Use cryptographically secure RNGs (e.g., `getrandom()`, `/dev/urandom`, or `arc4random()` where appropriate) for security-sensitive generation.
- If a service must use `rand()` for any reason, avoid constructing secrets directly from `time(NULL)`-seeded `rand()` values.

---

## Appendix — quick commands

Send a single guess from shell:

```bash
printf "%s\n" 6929181862867936308 | nc chal.sunshinectf.games 25101 -N
```

(Depending on your `nc` variant, omit `-N` if it is unsupported.)

---

## Flag
sun{I_KNOW_YOU_PLACED_A_MIRROR_BEHIND_ME}
