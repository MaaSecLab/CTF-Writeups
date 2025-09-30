## Name
Palatine Pack

### Problem Description
Caesar is raiding the Roman treasury to pay off his debts to his Gallic allies, and to you and his army. Help him find the password to make this Lucius Caecilius Metellus guy give up the money! >:) (he is sacrosanct so no violence!)

currently has nonstandard flag format sunshine{}

### Solution

I was given a ciphertext file (`flag.txt`) produced by the challenge ELF and asked to recover the original flag. I loaded the binary and quickly inspected its behavior: it reads `flag.txt`, runs a `flipBits()` routine, then an `expand()` routine three times, and finally prints the result. My approach was to reverse those transformations in order.

## Static analysis / behavior I observed

- The program reads the entire `flag.txt` into memory.
- It calls `flipBits()` once.
- It calls `expand()` **three times** (each `expand` doubles the buffer length).
- The resulting buffer is written to stdout / printed as the flag.

From reversing the assembly and/or replicating logic by reading it, I determined the two main routines worked like this:

### `expand()` (forward direction)
- Takes an input buffer of length `N` and produces an output of length `2N`.
- It processes bytes two at a time, splitting each original byte into two nibbles and writing them into two output bytes **in a toggling order**.
- There is a rolling key `k` in the binary that is updated (`k = (11*k) & 0xff`) and used in the forward routine, but critically, the actual data layout can be inverted simply by recombining nibbles — the key is not required to reverse the nibble interleaving, because the key was only combined into the forward-byte values before output; masking the nibbles and reassembling recovers the original byte.

Concretely, if `in` is the expanded buffer:
- Maintain a `state` that toggles every byte (0/1).
- For each original byte index `i`, take `a = in[2*i]` and `b = in[2*i+1]`
  - If `state == 0`: original byte = `(b & 0xF0) | (a & 0x0F)`
  - If `state == 1`: original byte = `(a & 0xF0) | (b & 0x0F)`
- Toggle `state` after each byte.

This is invertible and is what I implemented.

### `flipBits()` (forward direction)
- Alternates per byte:
  - On bytes where `state == 0` it applies bitwise NOT (`~byte`).
  - On bytes where `state == 1` it applies XOR with a key `k`, and after that XOR the key increments by `0x20` (`k += 0x20`) for its next use.
- The routine toggles `state` every byte.

Importantly, the sequence of operations is its own inverse if applied in the same alternating pattern: doing `~` then `^k` (with the same key progression) twice returns the original. Thus I can recover the plaintext by applying the same operation sequence to the ciphertext.

## My reversing plan

1. Read the provided ciphertext (`flag.txt`).
2. Apply the inverse of the last operation first. The binary did: `flipBits()` → `expand()` ×3. So the ciphertext = `expand(expand(expand(flipBits(plaintext))))`.  
   To invert: `plaintext = inv_flip(inv_expand(inv_expand(inv_expand(ciphertext))))`.
3. Implement the two inverse routines (`inv_expand` and `inv_flip`) in Python and run them on `flag.txt`.
4. Retrieve the plaintext flag.

## My implementation (Python)

I wrote the following Python script (I ran it locally against the challenge `flag.txt`):

```python
def inv_expand(data: bytes) -> bytes:
    # data length must be even
    out = bytearray(len(data)//2)
    state = 0
    for i in range(len(out)):
        a = data[2*i]
        b = data[2*i + 1]
        if state == 0:
            out[i] = ((b & 0xF0) | (a & 0x0F))
        else:
            out[i] = ((a & 0xF0) | (b & 0x0F))
        state ^= 1
    return bytes(out)

def inv_flip(buf: bytes) -> bytes:
    out = bytearray(len(buf))
    k = 0x69
    state = 0
    for i, x in enumerate(buf):
        if state == 0:
            out[i] = (~x) & 0xFF
        else:
            out[i] = x ^ k
            k = (k + 0x20) & 0xFF
        state ^= 1
    return bytes(out)

# Usage:
cipher = open("flag.txt", "rb").read()
pt = inv_flip(inv_expand(inv_expand(inv_expand(cipher))))
print(pt)
```

I verified the script produced readable ASCII including the flag.

## Example commands I ran

```bash
python3 decrypt_flag.py   # where decrypt_flag.py contains the code above and opens flag.txt
# or, interactively:
python3 - <<'PY'
PY
```

## Result (flag)

After running the script against the provided `flag.txt`, I recovered the flag:

```
sunshine{C3A5ER_CR055ED_TH3_RUB1C0N}
```

## Notes / Observations

- The `expand()` routine stores nibbles into bytes in an alternating order which doubles the size. Because the high nibble or low nibble positions are deterministic and only maskable operations are needed, reversing did not require the rolling key used in the forward path.
- `flipBits()` mixes simple bitwise transforms in an alternating pattern, but because that pattern is symmetric, the same logic is its own inverse when replayed exactly.
- Small pitfalls: be careful with Python's `~` operator — you must mask with `& 0xFF` to keep bytes in the 0–255 range.

