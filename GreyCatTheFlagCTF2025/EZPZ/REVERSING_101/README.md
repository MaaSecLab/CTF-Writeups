## Reversing 101

### Problem Description

The challenge consists of two parts:

1. Breaking into a password-protected executable.
2. Passing the knowledge verification quiz.

---

### Solution

By analyzing the decompiled source code of the software, we observe the following:

#### 1. Main Flow

* Reads password input.
* Calls function `a()` to get the password length (a custom implementation of `strlen`).
* Checks if the password length is exactly 15 characters.
* Calls function `b()`, a deterministic key generation algorithm (returns the same key every time).
* Calls function `c()`, which performs **RC4 encryption** using the password and a key passed via the `RDX` register.

---

### Exploitation Steps

1. **Set a breakpoint** at function `c`, then enter a 15-character password.

2. When the breakpoint is hit, **inspect the `RDX` register** to retrieve the encryption key (```x/8bx $rdx```):

   ```
   RDX = 0xc1de1494171d9e2f
   ```

3. **Extract the encrypted password** (the `enc` array) by printing its contents in GDB (```x/15bx &enc```):

   ```
   0x406058 <enc+0>:  0xd1  0x58  0x15  0x8a  0xee  0xb5  0xbb  0x52
   0x406060 <enc+8>:  0x0c  0x6b  0xa4  0xab  0x6d  0x7d  0xb7
   ```

---

### Final Step

Write a simple Python script to decrypt the `enc` array using the RC4 algorithm and the extracted key. Since RC4 is symmetric, decryption is straightforward.

Once decrypted, you just need to complete the quiz on the server with the things found along the way and you get the flag.

