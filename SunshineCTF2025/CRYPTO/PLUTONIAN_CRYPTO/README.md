## Name
Plutonian Crypto

### Problem Description
One of our deep space listening stations has been receiving a repeating message that appears to be coming from Pluto. It is encrypted with some sort of cipher but our best scientists have at least been able to decrypt the first part of the message, "Greetings, Earthlings."

See if you are able to somehow break their encryption and find out what the message is!

nc chal.sunshinectf.games 25403

### Solution
I connected to the challenge server and exploited a predictable AES-CTR keystream reuse pattern. Because each transmission restarted AES-CTR with the same key/nonce but with the initial counter shifted by one, each line leaked one 16-byte keystream block. Knowing the plaintext prefix `Greetings, Earthlings.` allowed me to recover keystream blocks and decrypt the first ciphertext fully. The flag I recovered:

```
sun{n3v3r_c0unt_0ut_th3_p1ut0ni4ns}
```

---

## Vulnerability summary 
The server encrypts the same plaintext message repeatedly using AES in CTR mode, but every time it begins encryption the counter value used for the first block is incremented by 1 (and the nonce is constant). That means line `n` uses keystream blocks `KS[n], KS[n+1], ...`. The fixed nonce + predictable counter progression creates a sliding-window keystream reuse across outputs. Because the plaintext starts with a known prefix, each new line directly reveals the keystream block for that line's first 16 bytes.

---

## Attack idea 
1. Observe that AES-CTR yields ciphertext: `ct = pt XOR KS` where `KS` is the stream of AES(key, nonce, counter) outputs.
2. Line `0` uses `KS[0], KS[1], ...`; line `1` uses `KS[1], KS[2], ...` and so on.
3. The first 16 bytes of line `n` are `pt[:16] XOR KS[n]`.
4. I know `pt[:16] = b"Greetings, Earthl"` (the first 16 bytes of `Greetings, Earthlings.`), so:
   ```
   KS[n] = ct_line_n[:16] XOR pt[:16]
   ```
5. Collect `KS[0..N-1]` for enough `n` (where `N` is number of blocks in the first ciphertext). Then XOR the first ciphertext with the assembled keystream to recover the full plaintext.

---

## My exploit script (core parts)
I wrote a small Python script that:
- connects to `chal.sunshinectf.games:25403`,
- reads ciphertext lines (hex),
- for line index `i` computes `ks[i] = ct[:16] XOR b"Greetings, Earthl"`,
- once I have `ks[0..(blocks_needed-1)]` I decrypt the first captured ciphertext and print it.

Key function used to XOR:
```python
def xor_bytes(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))
```

I saved the full working script as `solve_plutonian_crypto.py` when solving locally.

---

## Example run & output
When I ran the exploit I saw output like:

```
[+] Captured first ciphertext: 417 bytes (27 blocks)
[+] Line 0: learned keystream block 0. Progress 1/27
...
[+] Line 26: learned keystream block 26. Progress 27/27

================= DECRYPTED MESSAGE =================
Greetings, Earthlings. It has come to our attention that you have chosen to downgrade our mighty planet to the status of 'dwarf'. ...
Use this transmission code: sun{n3v3r_c0unt_0ut_th3_p1ut0ni4ns}
=====================================================
```

---

## Flag
```
sun{n3v3r_c0unt_0ut_th3_p1ut0ni4ns}
```

---

## Remediation / lessons learned
- **Never reuse a nonce with CTR mode** for different messages (and never use predictable or incrementing counter handling across different encryptions of the same plaintext). If you must increment counters, ensure the starting counter/nonce is fresh and unpredictable for each message.
- Use authenticated encryption (e.g., AES-GCM) to avoid subtle misuse of primitives.
- If the plaintext contains known headers or repeated content, reuse of keystream blocks leaks information quickly.
