# Albo delle eccellenze — Reverse Engineering Writeup

## Challenge Info

**Name:** Albo delle eccellenze (`albo`)  
**Category:** Reverse Engineering  
**Remote:**

```bash
nc albo.ctf.pascalctf.it 7004
```

**Story:** A former Blaisone CTF Team member earned a medal in Cyberchallenge.IT and wants to know if he received a prize.

---

## TL;DR

The binary’s “code verification” logic is **broken**: it prints **`Code matched!` regardless of the input**, then reads a local file named **`flag`** and prints its contents.

So on the remote service you can type **anything** for the prompts and still receive the flag (the “prize”).

---

## Files Provided

The archive contains a Linux ELF binary:

- `albo` — statically linked, stripped ELF (no symbols), which makes static reversing slightly more annoying but still straightforward.

---

## Recon & Initial Observations

Running the program shows a sequence of prompts asking for:

- name  
- surname  
- date of birth  
- sex  
- place of birth  

Then it claims to compute/verify a “code”. While reversing, the binary contains strings such as:

- `Code matched!`
- `Code did not match...`
- a hardcoded-looking code string: `A11D612LPSCBLS37` (likely intended as a reference / expected value)

This suggests the intended challenge was some kind of **fiscal code / identification code** computation and comparison.

---

## The Bug (Why It Always Works)

Even though the binary includes both success and failure messages, the control-flow for the check is wrong:

- The verification result is effectively ignored (or the conditional is inverted/short-circuited).
- The program always reaches the success branch:
  1. prints `Code matched!`
  2. opens a file called `flag`
  3. prints it to stdout

### What this implies

On the remote infrastructure, the service typically runs the binary in a directory where a `flag` file exists. Since the code path always tries to open and print it, the flag is leaked for any inputs.

---

## How to Solve Remotely

### Manual

Connect and respond with any 5 lines:

```bash
nc albo.ctf.pascalctf.it 7004
```

Example input:

```
a
b
01/01/2000
M
abc
```

Expected behavior:

```
Code matched!
Here is the flag: <FLAG>
```

### One-liner

```bash
printf "a\nb\n01/01/2000\nM\nabc\n" | nc albo.ctf.pascalctf.it 7004
```

### Pwntools Solver

```python
#!/usr/bin/env python3
from pwn import remote

HOST = "albo.ctf.pascalctf.it"
PORT = 7004

io = remote(HOST, PORT)

io.sendlineafter(b"name", b"a")
io.sendlineafter(b"surname", b"b")
io.sendlineafter(b"date", b"01/01/2000")
io.sendlineafter(b"sex", b"M")
io.sendlineafter(b"place", b"abc")

print(io.recvall(timeout=5).decode(errors="ignore"))
```

---

## Local Verification (Optional)

If you run the binary locally, you can confirm the behavior by creating a file called `flag` in the same directory:

```bash
echo "FAKEFLAG{test}" > flag
./albo
```

No matter what inputs you provide, it should still print `Code matched!` and then print the file contents.

---

## Root Cause (Typical Scenarios)

Without symbols, the exact line is not visible, but common reasons for this kind of bug in C/C++ binaries include:

- Comparing strings incorrectly (e.g., using `strcmp(...)` result wrong-way-round)
- Using the wrong conditional jump (e.g., `jne` instead of `je`)
- Overwriting the result variable before branching
- Returning a constant value from a check function
- Falling through to the success branch due to missing `return`/`else`

Regardless of which of the above occurred, the observable exploit is the same: **success is unconditional**.

---

## Conclusion

This is a classic “reverse” challenge that rewards noticing behavior rather than reconstructing the intended algorithm:

1. Observe the verification is ineffective  
2. Realize the binary always prints success and leaks `flag`  
3. Exploit remotely by sending any inputs  

**Result:** You reliably obtain the “prize” (flag) from the service.

---

