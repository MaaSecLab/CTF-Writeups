
# AuraTester2000 – Reverse Engineering Challenge Writeup

## Challenge Overview

**Name:** AuraTester2000  
**Category:** Reverse Engineering / Exploitation  
**Goal:** Gain enough aura to unlock the final test, decode an encoded phrase, and retrieve the flag.

The service is accessible via:

```
nc auratester.ctf.pascalctf.it 7001
```

The provided file `AuraTester2000.gyat` is a meme-obfuscated Python script that simulates a quiz-based aura system and a final decoding challenge.

---

## Program Logic Analysis

### Phrase Generation

The program randomly selects between 3 and 5 words from the following list:

```python
words = ["tungtung", "trallalero", "filippo boschi", "zaza", "lakaka", "gubbio", "cucinato"]
phrase = " ".join(random.sample(words, k=random.randint(3, 5)))
steps = random.randint(2, 5)
```

To obtain the flag, the user must reach **aura ≥ 500** and then correctly decode the encoded phrase.

---

## Step 1 – Farming Aura

There are four questions, each with fixed aura rewards:

| Question | yes  | no   |
|----------|------|------|
| Q1       | +150 | -50  |
| Q2       | -1000| +50  |
| Q3       | +450 | -80  |
| Q4       | -100 | +50  |

Correct strategy:

```
yes
no
yes
no
```

Total aura gained:

```
150 + 50 + 450 + 50 = 700
```

This unlocks the final decoding test.

---

## Step 2 – Encoding Algorithm

The encoder works as follows:

```python
def encoder(phrase, steps):
    out = ""
    for i in range(len(phrase)):
        if phrase[i] == " ":
            out += " "
        elif i % steps == 0:
            out += str(ord(phrase[i]))
        else:
            out += phrase[i]
    return out
```

Rules:
- Spaces remain unchanged.
- Every `i % steps == 0` character is converted to its ASCII value (97–122).
- Other characters remain as letters.
- Numbers and letters are mixed without delimiters.

Example concept:

```
tungtung -> 116ung116ung
```

(depending on steps)

---

## Step 3 – Decoding Strategy

We brute-force `steps` from 2 to 5 and parse the encoded string:

- If position `i % steps == 0`, read 2–3 digits and convert from ASCII.
- Otherwise, read a literal character.
- Validate output against known word combinations (3–5 items from word list).

Because only lowercase letters appear, ASCII range is limited to 97–122.

---

## Exploit Script

```python
#!/usr/bin/env python3
from pwn import remote
import re

HOST = "auratester.ctf.pascalctf.it"
PORT = 7001

WORDS = ["tungtung", "trallalero", "filippo boschi", "zaza", "lakaka", "gubbio", "cucinato"]

def can_segment_into_word_items(s):
    memo = {}
    def dfs(rest, k):
        if (rest, k) in memo:
            return memo[(rest, k)]
        if rest in WORDS:
            return 3 <= k+1 <= 5
        for w in WORDS:
            pref = w + " "
            if rest.startswith(pref):
                if dfs(rest[len(pref):], k+1):
                    return True
        return False
    return dfs(s, 0)

def decode_encoded(enc):
    for steps in range(2, 6):
        i = 0
        p = 0
        out = []
        ok = True
        while p < len(enc):
            c = enc[p]
            if c == " ":
                out.append(" ")
                p += 1
                i += 1
                continue
            if i % steps == 0:
                found = False
                for nd in (2,3):
                    if p+nd <= len(enc) and enc[p:p+nd].isdigit():
                        val = int(enc[p:p+nd])
                        if 97 <= val <= 122:
                            out.append(chr(val))
                            p += nd
                            i += 1
                            found = True
                            break
                if not found:
                    ok = False
                    break
            else:
                if c.isdigit():
                    ok = False
                    break
                out.append(c)
                p += 1
                i += 1
        if ok:
            phrase = "".join(out)
            if can_segment_into_word_items(phrase):
                return phrase
    raise ValueError("Decode failed")

def main():
    io = remote(HOST, PORT)
    io.recvuntil(b"> ")
    io.sendline(b"player")
    io.recvuntil(b"> ")
    io.sendline(b"1")

    for ans in [b"yes", b"no", b"yes", b"no"]:
        io.recvuntil(b"> ")
        io.sendline(ans)

    io.recvuntil(b"> ")
    io.sendline(b"3")

    data = io.recvuntil(b"Type the decoded phrase").decode()
    m = re.search(r"secret phrase:\s*(.+)", data)
    enc = m.group(1)

    phrase = decode_encoded(enc)
    io.sendline(phrase.encode())
    print(io.recvall().decode())

if __name__ == "__main__":
    main()
```

---

## Conclusion

This challenge demonstrates:
- Reverse engineering obfuscated Python logic
- Predictable scoring exploitation
- Custom decoding without delimiters
- Constraint-based brute force

The solution guarantees flag retrieval by:
1. Maximizing aura
2. Decoding the phrase via ASCII reconstruction
3. Submitting the valid phrase

---

