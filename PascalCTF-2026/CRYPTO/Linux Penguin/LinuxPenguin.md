# Linux Penguin — PascalCTF Full Writeup

## Challenge Description
We connect to the service:

```
nc penguin.ctf.pascalctf.it 5003
```

The service displays ASCII art and then repeatedly asks:

```
Give me 4 words to encrypt (max 16 chars):
Word 1:
Word 2:
Word 3:
Word 4:
```

After providing 4 words, the server responds with:

```
Encrypted words: <hex1> <hex2> <hex3> <hex4>
```

After several rounds, it prints:

```
Ciphertext: <5 hex blocks>
Guess the word 1:
```

We must guess the 5 original words used to produce the ciphertext blocks.

The list of valid words is fixed and known (28 words).

---

## Observations

From the provided server code and interaction:

- AES encryption is used
- Mode = ECB
- Each word is padded to 16 bytes using `ljust(16)`
- Same AES key is used for the entire session
- Each word encrypts to exactly **one AES block**
- The final secret is made of **5 encrypted blocks**

---

## Vulnerability

AES in ECB mode is deterministic:

```
AES(key, plaintext) = same ciphertext every time
```

Because:
- The word list is known
- There are only 28 possible words
- Each word is exactly 16 bytes when padded

We can build a dictionary:

```
ciphertext_block → plaintext_word
```

This is a classic **ECB dictionary attack**.

---

## Attack Strategy

1. Send all 28 words to the service (4 per round = 7 rounds)
2. Record each ciphertext block
3. Build mapping of ciphertext → word
4. When final 5 ciphertext blocks are given, reverse-map them
5. Send the recovered words back
6. Receive the flag

---

## Word List

We send these words in order:

Round 1:
- biocompatibility
- biodegradability
- characterization
- contraindication

Round 2:
- counterbalancing
- counterintuitive
- decentralization
- disproportionate

Round 3:
- electrochemistry
- electromagnetism
- environmentalist
- internationality

Round 4:
- internationalism
- institutionalize
- microlithography
- microphotography

Round 5:
- misappropriation
- mischaracterized
- miscommunication
- misunderstanding

Round 6:
- photolithography
- phonocardiograph
- psychophysiology
- rationalizations

Round 7:
- representational
- responsibilities
- transcontinental
- unconstitutional

---

## Example Mapping (from interaction)

From the captured session:

```
internationality  -> 88b857de798eed3567e43b14a2a5b886
biocompatibility -> 09e721e5d5cda58a73e96aa4ca5c3bae
contraindication -> d881354112d99ce8103ce130c9362633
transcontinental -> 5e371aba545815f3cec44e1710d9d476
internationalism -> 7327d6b5476a55012baf8bf536870b30
```

Final ciphertext:
```
88b857de798eed3567e43b14a2a5b886
09e721e5d5cda58a73e96aa4ca5c3bae
d881354112d99ce8103ce130c9362633
5e371aba545815f3cec44e1710d9d476
7327d6b5476a55012baf8bf536870b30
```

Recovered words:
1. internationality
2. biocompatibility
3. contraindication
4. transcontinental
5. internationalism

---

## Manual Solution

At the prompts:

```
Guess the word 1: internationality
Guess the word 2: biocompatibility
Guess the word 3: contraindication
Guess the word 4: transcontinental
Guess the word 5: internationalism
```

The server responds with the flag.

---

## Automated Solver (Python)

```python
import socket, re

HOST = "penguin.ctf.pascalctf.it"
PORT = 5003

WORDS = [
    "biocompatibility","biodegradability","characterization","contraindication",
    "counterbalancing","counterintuitive","decentralization","disproportionate",
    "electrochemistry","electromagnetism","environmentalist","internationality",
    "internationalism","institutionalize","microlithography","microphotography",
    "misappropriation","mischaracterized","miscommunication","misunderstanding",
    "photolithography","phonocardiograph","psychophysiology","rationalizations",
    "representational","responsibilities","transcontinental","unconstitutional"
]

def recv_until(sock, token):
    data = b""
    while token not in data:
        data += sock.recv(4096)
    return data

def send(sock, s):
    sock.sendall((s+"\n").encode())

s = socket.create_connection((HOST,PORT))
recv_until(s,b"Word 1:")

ct_map = {}
i = 0

for _ in range(7):
    batch = WORDS[i:i+4]
    i += 4
    for w in batch:
        recv_until(s,b":")
        send(s,w)

    data = recv_until(s,b"Encrypted")
    blocks = re.findall(rb"[0-9a-f]{32}", data)
    for w,b in zip(batch,blocks):
        ct_map[b.decode()] = w

data = recv_until(s,b"Ciphertext")
final_blocks = re.findall(rb"[0-9a-f]{32}", data)
secret = [ct_map[b.decode()] for b in final_blocks]

for w in secret:
    recv_until(s,b":")
    send(s,w)

print(s.recv(4096).decode())
```

---

## Lessons Learned

- AES-ECB should never be used for secrets
- Deterministic encryption enables dictionary attacks
- Known plaintext space makes cryptography trivial to break
- Always use randomized modes like CBC or GCM

---

## Conclusion

This challenge demonstrates why ECB mode is insecure and how predictable encryption with a small plaintext domain can be completely reversed using a dictionary attack.
