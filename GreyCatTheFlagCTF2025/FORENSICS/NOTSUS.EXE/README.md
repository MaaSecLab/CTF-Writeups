## NOTSUS.EXE

### Problem Description

This challenge consists of a password-protected ZIP file containing:

* An executable named `notsus.exe`
* A flag file with a strange extension: `.yorm`

---

### Solution Overview

After researching password-protected ZIP vulnerabilities, I discovered a paper on the **classic encryption weaknesses** in ZIP files. It revealed that a **known plaintext attack** is feasible.

I then found a tool called [`bkcrack`](https://github.com/kimci86/bkcrack) that implements this attack. To use it, we need **at least 12 known bytes**, with **8 of them being consecutive** from the plaintext of one of the encrypted files.

#### Known Bytes Selection

The `.exe` file gave me a clue: Windows executables start with a known header (`MZ`), followed by a predictable byte pattern. So, I used this as the known plaintext:

```bash
printf "\x4D\x5A\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00\xFF\xFF\x00\x00\xB8\x00\x00\x00\x00\x00\x00\x00\x40\x00\x00\x00\x00\x00\x00\x00" > known_header.bin
```

---

### Cracking the ZIP File

Using `bkcrack` to find the internal ZIP keys:

```bash
bkcrack -C files.zip -c notsus.exe -p known_header.bin
```

After running, the tool outputs the following keys:

```
d1608c35 d11d350a 4bc3da9c
```

Now we can decrypt both files:

```bash
bkcrack -C files.zip -c notsus.exe -k d1608c35 d11d350a 4bc3da9c -d notsus.exe
bkcrack -C files.zip -c flag.text.yorm -k d1608c35 d11d350a 4bc3da9c -d flag.text.yorm
```

---

### Flag Decryption

Upon extracting `flag.text.yorm`, its contents appear **encrypted gibberish**. Time to reverse-engineer `notsus.exe`.

#### Step 1: Identify the Packager

Running `strings` on `notsus.exe` reveals that it's **PyInstaller-packed**.

#### Step 2: Extract the Python Bytecode

Use [`pyinstxtractor`](https://github.com/extremecoders-re/pyinstxtractor) to extract the contents:

```bash
python pyinstxtractor.py notsus.exe
```

This gives us a `.pyc` file: `notsus.pyc`.

#### Step 3: Decompile the Python File

Decompile using [pylingual.io](https://pylingual.io/).
The code reveals an RC4 encryption function using a **hardcoded key:**

```
"HACKED!"
```

---

### Final Decryption Script

Using the RC4 function copied from the decompiled code, I wrote a simple Python script to decrypt the flag file present in the solution script.

---

### Flag Recovered!

The script successfully decrypts the file and reveals the flag.

