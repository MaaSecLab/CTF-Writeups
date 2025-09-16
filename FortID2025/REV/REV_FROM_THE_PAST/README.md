## Rev From the Past 


### Problem Description
Last year you've enjoyed pwning a binary from the MS-DOS era.

This year, we challenge you to reverse engineer one such binary.
### Solution
The COM:
t expects the flag as a command-line arg starting with FortID{ and exactly 33 chars until }.

It builds a 256-byte table at 0x279 (Fisher–Yates shuffle) using a Galois LFSR seeded with the 16-bit value at [0x254] = 0xB4C1.

It takes a 33-byte blob at 0x37E, XORs each byte with 0x64 (because BL = ([0x254] & 0xFF) ^ 0xA5 = 0xC1 ^ 0xA5 = 0x64), and those are the target bytes.

For each input byte x, it checks S[x] == target[i] (XLATB with base at 0x279).

So the required input byte is x = S^{-1}[target[i]].

Code:
#!/usr/bin/env python3
from pathlib import Path

COM = Path("CHAL.COM").read_bytes()

Offsets in the file (COM is loaded at 0x100)
seed = int.from_bytes(COM[0x254-0x100:0x256-0x100], "little")  # 0xB4C1
blob = COM[0x37e-0x100:0x37e-0x100+0x21]  # 33 bytes

Build the 256-byte permutation table S using the COM's routine
S = list(range(256))
state = seed
for cx in range(0xFF, 0, -1):
    ax = state
    carry = ax & 1
    ax >>= 1
    if carry:
        ax ^= 0xB400           # Galois LFSR step
    state = ax
    j = state % (cx + 1)       # Fisher–Yates swap index
    S[cx], S[j] = S[j], S[cx]

Pre-xor on the target bytes (the binary does: target ^= 0x64)
target = bytes(b ^ 0x64 for b in blob)

Invert S and map target -> input bytes
Sinv = [0]*256
for i, v in enumerate(S):
    Sinv[v] = i

body = bytes(Sinv[b] for b in target)
flag = b"FortID{" + body + b"}"
print(flag.decode())
