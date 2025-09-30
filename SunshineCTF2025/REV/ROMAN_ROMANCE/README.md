## Name
Roman Romance

### Problem Description
When in Rome...

currently has nonstandard flag format sunshine{}

### Solution
# CTF Writeup — Roman Romance (reverse engineering)


## Summary 

I recovered the flag by inspecting the provided `enc.txt` file, noticing that every byte in the file was the original flag with each character shifted **up by 1** in ASCII. I wrote a tiny Python script to subtract `1` from each byte, which revealed the flag.

**Flag:** `sunshine{kN0w_y0u4_r0m@n_hI5t0rY}`

---

## What I looked at first

I began by listing the files and checking basic file types to understand what I was dealing with:

```bash
ls -la
file enc.txt
file romanromance
```

`enc.txt` reported as a small text/binary file; `romanromance` looked like an ELF or an extra program the author included. For this challenge the encrypted text file was the key.

## Inspecting the encrypted file

I opened the file in a hex viewer to look for patterns that suggested a simple transformation instead of strong crypto.

```bash
hexdump -C enc.txt | sed -n '1,8p'
# or
xxd enc.txt | sed -n '1,8p'
```

What I observed was that the bytes were printable and looked like ASCII, but every expected letter was "off by one" — e.g. where I expected an `s` I saw `t`, where I expected `{` I saw `|`, etc. That strongly suggested an *increment-by-1* transformation on ASCII codes.

To confirm, I printed the bytes and compared them numerically:

```python
# quick check (interactive)
with open('enc.txt','rb') as f:
    data = f.read()
print(list(data[:20]))
```

Seeing that the bytes were all in the printable range and consistently one value higher than readable text convinced me the correct transform was to subtract `1` from every byte.

## Decoding: the exact command I used

I used a one-liner to decode the flag directly from `enc.txt`:

```bash
python3 -c "print(bytes([(b-1) % 256 for b in open('enc.txt','rb').read()]).decode())"
```

Alternatively, a short script (safer and easier to read):

```python
#!/usr/bin/env python3

with open('enc.txt','rb') as fin:
    data = fin.read()

decoded = bytes([(b-1) % 256 for b in data])
print(decoded.decode())
```

Running either of those produced the cleartext flag shown above.

## Notes and reasoning

* I prioritized simple transformations first (shifts, XOR with a single byte, base encodings) because many CTFs deliberately use low-effort obfuscation.
* Hex viewers (`hexdump`, `xxd`) make these patterns obvious: printable bytes that are consistently offset tend to indicate a Caesar-like shift on bytes.
* I checked that the transformation applied to all bytes and that the result decoded cleanly as UTF-8 — that gave me confidence the output was the intended flag rather than garbage.

## Optional: how I would patch the provided program (if required)

If the challenge had required automating decoding on the `romanromance` binary rather than the `enc.txt` file, I would have:

1. Run `strace` and `ltrace` to see file I/O and library calls.
2. Use `objdump -d` / `gdb` or `radare2`/`ghidra` to find the decoding routine.
3. Either patch the binary to print the decoded flag directly or supply input such that the program produces the flag.

I did not need to do that here because the `enc.txt` file contained the whole encoded flag.

## Final result

I recovered the flag and verified it decodes to:

```
sunshine{kN0w_y0u4_r0m@n_hI5t0rY}
```

---
