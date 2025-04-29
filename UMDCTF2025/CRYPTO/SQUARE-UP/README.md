## SQUARE-UP
### Problem Description
erm my encrypted flag be bussin but on jod the decrypt fails the vibe check frfr no cap

<br>

### Provided Files
#### main.py
```python
from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes
from os import urandom

with open("flag.txt", "rb") as f:
	flag = f.read()
	m = bytes_to_long(flag)

p = q = 0
while p % 4 != 3: p = getPrime(384)
while q % 4 != 3: q = getPrime(384)

N = p * q
print(f"{N = }")
def encrypt(m):
	lp = (pow(m, (p-1)//2, p) + 1) % p - 1
	lq = (pow(m, (q-1)//2, q) + 1) % q - 1
	return m * m % N, lp, lq

def decrypt(c, lp, lq):
	yq = pow(q, -1, p)
	yp = (1 - yq * q) // p

	mp = pow(c, (p+1)//4, p)
	mq = pow(c, (q+1)//4, q)
	
	if (pow(mp, (p-1)//2, p) - lp) % p != 0: mp = p - mp
	if (pow(mq, (q-1)//2, q) - lq) % q != 0: mq = q - mp

	return (yp * p * mq + yq * q * mp) % N
	

c, lp, lq = encrypt(m)
print(f"{(c, lp, lq) = }")
print(f"{long_to_bytes(decrypt(c, lp, lq)) = }")
```

#### output.txt
```
N = 1298690852855676717877172430649235439701166577296380685015744142960768447038281361897617173145966407353660262643273693068083328108519398663073368426744653753236312330497119252304579628565448615356293308415969827357877088267274695333
(c, lp, lq) = (162345251908758036296170413099695514860545515965805244415511843227313118622229046299657295062100889503276740904118647336251473821440423216697485906153356736210597508871299190718706584361947325513349221296586217139380060755033205077, 1, -1)
long_to_bytes(decrypt(c, lp, lq)) = b'\x1bR \xc4\xf0\x8f\xa7l\xa4\xdd\xbf\xf73\xf3\xe9(\xc8Q\xdd\xbd,\x08\xbd\x7f\xafm\x9b\xbf\xa0\xbe\xd4)t\xd4e\xc0,J\xb8H\x93i\xea\xbcy\x9a7AA\xeb]q\xae\x00\xebJ(Y\x8a\xa4B\xdc\t(\x8b\xcef&@b\x91\x06Y~\x88m\xaf\x9bl\\\x12\xf2\x9f\xe1\x1f\x18q\x16\xd8\xb4\x9f$\x88%8\x0f'
```

<br>

### Solution
#### Step 1
Analyzing the code revealed that the encryption algorithm being used was a **Rabin Cryptosystem**. Furthermore, given the problem description, it became evident that the decrypt method in **main.py** was faulty. But what part of it was faulty?

#### Step 2
When studying the Rabin Cryptosystem, it was discovered that the decryption process involves multiple steps:
1. Calculate the square roots of the ciphertext modulo p and q. 
$$N=p×q$$
2. Use Legendre symbols to determine the correct square roots. *The Legendre symbol is a mathematical notation that indicates whether a number is a quadratic residue modulo p or q.*
3. Use the Chinese Remainder Theorem (CRT) to combine the results.

#### Step 3
Now, we can find out why the decryption logic failed in **main.py**.  In the Rabin cryptosystem, when choosing the correct square root modulo $q$, the code should flip $mq$ if the Legendre symbol does not match. However, the code incorrectly sets $mq = q - mp$ instead of $mq = q - mq$. This error causes the decryption to output a value that is not the original plaintext, but instead a "broken" root unrelated to the flag.

#### Step 4
We know what to fix, but we have a problem. We do not know what p and q were when the ciphertext was generated. However, we do know that the ciphertext is a quadratic residue modulo p and q. Therefore, we can use the broken decryption to find p and q. 
```Python
D = int.from_bytes(broken_decryption_bytes, 'big')
p = math.gcd(D*D - c, N)
q = N // p
```

#### Step 5
Now that we have p and q, we can use the correct decryption algorithm to find the flag. The correct decryption algorithm is as follows:
```Python
# Compute square roots modulo primes
mp = pow(c, (p+1)//4, p)
mq = pow(c, (q+1)//4, q)

# Adjust roots using Legendre symbols
if (pow(mp, (p - 1) // 2, p) - lp) % p != 0: mp = p - mp
if (pow(mq, (q - 1) // 2, q) - lq) % q != 0: mq = q - mq

# Chinese Remainder Theorem
yq = pow(q, -1, p)
yp = (1 - yq * q) // p

message = (yp * p * mq + yq * q * mp) % N
```


#### Step 6
Finally, we can convert the decrypted message into a readable format by converting the long integer to bytes and then decoding it.
```Python
flag = long_to_bytes(message)
print(flag.decode(errors='ignore'))
```

#### Result
The final decrypted message will be revealed as: `UMDCTF{e=3_has_many_attacks_and_e=2_has_its_own_problems...maybe_we_should_try_e=1_next?}`

<br>

### Final Decryption Algorithm
```Python
import math

def long_to_bytes(val):
    return val.to_bytes((val.bit_length() + 7) // 8, 'big')

# Given output
N = 1298690852855676717877172430649235439701166577296380685015744142960768447038281361897617173145966407353660262643273693068083328108519398663073368426744653753236312330497119252304579628565448615356293308415969827357877088267274695333
c = 162345251908758036296170413099695514860545515965805244415511843227313118622229046299657295062100889503276740904118647336251473821440423216697485906153356736210597508871299190718706584361947325513349221296586217139380060755033205077
lp = 1
lq = -1
broken_decryption_bytes = b'\x1bR \xc4\xf0\x8f\xa7l\xa4\xdd\xbf\xf73\xf3\xe9(\xc8Q\xdd\xbd,\x08\xbd\x7f\xafm\x9b\xbf\xa0\xbe\xd4)t\xd4e\xc0,J\xb8H\x93i\xea\xbcy\x9a7AA\xeb]q\xae\x00\xebJ(Y\x8a\xa4B\xdc\t(\x8b\xcef&@b\x91\x06Y~\x88m\xaf\x9bl\\\x12\xf2\x9f\xe1\x1f\x18q\x16\xd8\xb4\x9f$\x88%8\x0f'

# Step 1: Find N using broken decryption
D = int.from_bytes(broken_decryption_bytes, 'big')
p = math.gcd(D*D - c, N)
q = N // p

# Step 2: Perform correct decryption
# Compute square roots modulo primes
mp = pow(c, (p+1)//4, p)
mq = pow(c, (q+1)//4, q)

# Adjust roots using Legendre symbols
if (pow(mp, (p - 1) // 2, p) - lp) % p != 0: mp = p - mp
if (pow(mq, (q - 1) // 2, q) - lq) % q != 0: mq = q - mq

# Chinese Remainder Theorem
yq = pow(q, -1, p)
yp = (1 - yq * q) // p

message = (yp * p * mq + yq * q * mp) % N

# Convert to flag and print
flag = long_to_bytes(message)
print(flag.decode(errors='ignore'))
```

Have a great day :D [https://github.com/JoelDha](https://github.com/JoelDha)
