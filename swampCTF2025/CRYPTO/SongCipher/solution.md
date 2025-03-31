## SongCipher
### Problem Description
Sombody once told me the cipher was gonna roll me. You are the sharpest tool in the shed <3 After this challenge, you might want to add that song to your playlist :)

A text file titled **data.txt** was also provided and it contained the encrypted message:

```
aa, d7, ce, d9, 82, d0, d6, de, 40, e8, dd, d8, 85, 84, e3, d8, da, cb, 40, d6, d3, 40, e1, e1, 85, 93, ee, d0, df, dc, a3, 40, bc, ea, 81, d4, df, 8f, 8e, b4, 97, d3, dc, dc, 8d, 40, c0, dc, 81, b6, 90, 82, 89, bd, 8f, a0, 40, d8, cd, c6, 92, 94, 88, b8, da, df, c6, 94, 94, 61, e0, db, 8f, de, 89, d0, d6, 94, a0, 88, cc, 85, e7, 88, d4, d9, 94, 73, d7, cb, 40, df, c6, e5, 85, 9a, 8f, b0, d7, d5, 8e, d6, 86, 8b, e2, dd, d9, 4c, 8f, d3, 8f, da, da, 8d, cb, 94, 98, 89, b7, d7, 8d, cd, 85, e1, 8e, 87, 89, ba, cc, d9, 99, 93, 81, d5, d3, 41, 88, b9, da, 85, 94, ce, e1, ce, c9, 40, b2, e1, 40, e7, df, c6, 8d, e3, ab, b5, b6, e0, 73, a0, d3, 90, cd, a1, 7f, 75, 7c, 90, 87, ce, 9e, 74, b8, c4, b5, 51, d6, d7, a5, d7, e5
```

### Solution
#### Step 1
Upon opening the text file, it was instantly noticed that the ciphertext was given in hexadecimal format. Therefore, python was used to convert the message into a list of integer values.

```python
# Convert hex ciphertext to bytes
ciphertext_hex = "aa, d7, ce,..."  #Shortened to improve readability
tokens = re.split(r',\s*', ciphertext_hex)
ciphertext_bytes = [int(t.strip(), 16) for t in tokens]
```

#### Step 2
The description of the challenge made it clear that the song "All Star" by Smash Mouth had to be used somewhere in the decryption process. Therefore, the lyrics were encoded into ASCII bytes to be used as the encryption key.

```python
key_str = ("Somebody once told me the world is gonna roll me ..." )#Shortened to improve readability
key_bytes = key_str.encode('ascii')
```

#### Step 3
It as then discovered that the method used to encypt the message was modulo-256 subtraction cipher. To decrypt the message, each byte in the ciphertext was subtracted (mod 256) by the corresponding byte in the key (cycling through if necessary). If the result was a printable ASCII character (32–126), it was directly added to the plaintext. Otherwise, it was left in hexadecimal format for clarity.
```python
plaintext = []
for i, c in enumerate(ciphertext_bytes):
    k = key_bytes[i % len(key_bytes)]
    p = (c - k) % 256
    if 32 <= p <= 126:
        plaintext.append(chr(p))
    else:
        plaintext.append(f"[{p:02x}]")
```

#### Step 4
Convert the decrypted message into a readable format by joining the extracted plaintext characters into a single string. And then print it.
```python
full_output = ''.join(plaintext)
print("Complete Decryption:\n", full_output)
```

#### Result

After running, the final decrypted message will be revealed as: `What are you doing in my swamp? Swamp! Swamp! Swamp! Oh, dear! Whoa! All right, get out of here. All of you, move it! Come on! Let's go! The flag is swampCTF{S1mpl3_S0ng_0TP_C1ph3r}`

Finally, in that message, the flag is revealed to be **swampCTF{S1mpl3_S0ng_0TP_C1ph3r}**

## Final Code

```python
import re

# Ciphertext and its conversion to bytes
ciphertext_hex = "aa, d7, ce, d9, 82, d0, d6, de, 40, e8, dd, d8, 85, 84, e3, d8, da, cb, 40, d6, d3, 40, e1, e1, 85, 93, ee, d0, df, dc, a3, 40, bc, ea, 81, d4, df, 8f, 8e, b4, 97, d3, dc, dc, 8d, 40, c0, dc, 81, b6, 90, 82, 89, bd, 8f, a0, 40, d8, cd, c6, 92, 94, 88, b8, da, df, c6, 94, 94, 61, e0, db, 8f, de, 89, d0, d6, 94, a0, 88, cc, 85, e7, 88, d4, d9, 94, 73, d7, cb, 40, df, c6, e5, 85, 9a, 8f, b0, d7, d5, 8e, d6, 86, 8b, e2, dd, d9, 4c, 8f, d3, 8f, da, da, 8d, cb, 94, 98, 89, b7, d7, 8d, cd, 85, e1, 8e, 87, 89, ba, cc, d9, 99, 93, 81, d5, d3, 41, 88, b9, da, 85, 94, ce, e1, ce, c9, 40, b2, e1, 40, e7, df, c6, 8d, e3, ab, b5, b6, e0, 73, a0, d3, 90, cd, a1, 7f, 75, 7c, 90, 87, ce, 9e, 74, b8, c4, b5, 51, d6, d7, a5, d7, e5"
tokens = re.split(r',\s*', ciphertext_hex)
ciphertext_bytes = [int(t.strip(), 16) for t in tokens]

# Key made of lyrics from Smash Mouth's "All Star"
key_str = (
    "Somebody once told me the world is gonna roll me I ain't the sharpest tool in the shed "
    "She was looking kind of dumb with her finger and her thumb "
    "In the shape of an \"L\" on her forehead "
)
key_bytes = key_str.encode('ascii')

# Decryption process using the key
plaintext = []
for i, c in enumerate(ciphertext_bytes):
    k = key_bytes[i % len(key_bytes)]
    p = (c - k) % 256
    if 32 <= p <= 126:
        plaintext.append(chr(p))
    else:
        plaintext.append(f"[{p:02x}]")

# Convert decrypted output to readable format
full_output = ''.join(plaintext)
print("Complete Decryption:\n", full_output)

# EXTRA STEP: Automatic flag extraction
flag_start = full_output.find('swampCTF{')
flag_end = full_output.find('}', flag_start) + 1

if flag_start != -1:
    print("\nFlag Found:", full_output[flag_start:flag_end])
else:
    print("\nFlag extraction failed")
```

Have a great day :D [https://github.com/JoelDha](https://github.com/JoelDha)
