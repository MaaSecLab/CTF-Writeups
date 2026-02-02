# StrangeVM — Reverse Engineering Writeup

## Challenge

> A 🧙🏻‍♂️ stranger once built a VM and hid the Forbidden Key🥀, can you uncover it?  
> P.S.: Keep all the files in the same directory for easier debugging and execution.

**Files provided:**
- `vm` (ELF executable)
- `code.pascal` (bytecode/program for the VM)

---

## Summary

The binary `vm` implements a small custom virtual machine that:
1. Loads `code.pascal`
2. Allocates a memory buffer (`mem`) used by the VM
3. Runs the bytecode, which:
   - reads **40 bytes** of input into memory
   - transforms them based on their index
   - compares the transformed buffer to a hidden 40-byte constant in `.rodata`

By reversing the VM instruction set and the bytecode, we can **invert the transformation** and recover the required input (the “Forbidden Key”).

Final flag:

```
pascalCTF{VMs_4r3_d14bol1c4l_3n0ugh_d0nt_y0u_th1nk}
```

---

## VM Architecture

### High-level behavior

`vm` loads `code.pascal` from the current directory (hence the hint about keeping files together), then interprets it with a function similar to `executeVM`.

During execution, the VM uses a small byte-addressable memory array:

- `mem[0x400]` (1024 bytes)

The bytecode program reads input, transforms it, and the outer program finally checks the result with something like:

```c
strcmp((char*)mem, expected_bytes) == 0
```

Where `expected_bytes` is a 40-byte blob stored in `.rodata` (not printable as a string).

---

## Instruction Set (Observed)

From reversing the interpreter, the following opcodes are used:

| Opcode | Operands         | Meaning |
|-------:|------------------|---------|
| `0x05` | `addr`           | Read 1 raw char into `mem[addr]` (`scanf("%c")`) |
| `0x01` | `addr, imm`      | `mem[addr] += imm` |
| `0x02` | `addr, imm`      | `mem[addr] -= imm` |
| `0x03` | `addr, imm`      | `mem[addr] %= imm` |
| `0x04` | `addr, imm`      | `mem[addr] = imm` |
| `0x06` | `addr, off`      | If `mem[addr] == 0`, then `pc += off` (conditional jump) |

This is enough to understand the bytecode’s control flow and data transformations.

---

## Bytecode Behavior

### Input stage

The program reads **40 characters** into memory:

- `mem[0]` … `mem[39]`

It also reads one additional character (often the newline), which later gets overwritten/ignored. This is why sending the key followed by a newline works perfectly.

### Transformation stage

For each index `i` from `0` to `39`, it applies an index-dependent transform:

- If `i` is **even**:
  - `mem[i] = input[i] + i` (mod 256)
- If `i` is **odd**:
  - `mem[i] = input[i] - i` (mod 256)

This is exactly the kind of logic you’d expect to see implemented via opcode sequences like:

- `READ mem[i]`
- `ADD/SUB immediate i`
- (optionally) `MOD 256` to keep bytes in range

### Final comparison

After transforming the buffer, `vm` compares `mem[0..39]` to a hidden 40-byte constant embedded in the binary.

So the correct input is the inverse transform applied to the constant target bytes.

---

## Reversing the Key (Inverting the Transform)

Since the VM does:

- even i: `out = in + i`
- odd i:  `out = in - i`

We invert it as:

- even i: `in = out - i`
- odd i:  `in = out + i`

Applying this inversion to the embedded 40-byte target yields the unique valid 40-character string:

```
VMs_4r3_d14bol1c4l_3n0ugh_d0nt_y0u_th1nk
```

Length check:

- exactly **40 characters** ✅

---

## Getting the Flag

When the correct key is provided, the program prints the flag.

The flag format is:

```
pascalCTF{<forbidden_key>}
```

So the final flag is:

```
pascalCTF{VMs_4r3_d14bol1c4l_3n0ugh_d0nt_y0u_th1nk}
```

---

## Running It (Local / Remote)

### Local

```bash
./vm
# paste:
VMs_4r3_d14bol1c4l_3n0ugh_d0nt_y0u_th1nk
```

### Over netcat

If the challenge is hosted remotely, you can typically solve with:

```bash
printf "VMs_4r3_d14bol1c4l_3n0ugh_d0nt_y0u_th1nk\n" | nc <HOST> <PORT>
```

(The VM reads an extra char; the newline is ideal for that.)

### Pwntools template

```python
#!/usr/bin/env python3
from pwn import remote

HOST = "<HOST>"
PORT = <PORT>

key = b"VMs_4r3_d14bol1c4l_3n0ugh_d0nt_y0u_th1nk"

io = remote(HOST, PORT)
io.sendline(key)
print(io.recvall(timeout=5).decode(errors="ignore"))
```

---

## Notes

This challenge is a great example of:
- identifying a custom VM’s instruction set
- reading bytecode intent
- spotting a reversible transformation
- recovering the required input by inversion rather than brute force

The “keep all files together” hint matters because `vm` expects to load `code.pascal` relative to its working directory.

