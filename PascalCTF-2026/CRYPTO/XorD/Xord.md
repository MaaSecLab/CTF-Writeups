# XOR D — PascalCTF Writeup

## Challenge Description
We are given a Python script and a ciphertext file. The script seeds Python's RNG with a constant value and XORs a generated keystream with the flag.

## Vulnerability
The RNG is seeded with a fixed value (`1337`), making the keystream predictable.

## Solution
Re-generate the same keystream and XOR it with the ciphertext.

## Exploit Code
```python
import random

random.seed(1337)
with open("output.txt") as f:
    data = bytes.fromhex(f.read().strip())

keystream = bytes(random.getrandbits(8) for _ in range(len(data)))
flag = bytes(a ^ b for a,b in zip(data, keystream))
print(flag.decode())
```

