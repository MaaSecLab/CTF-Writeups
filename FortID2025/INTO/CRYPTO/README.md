This is just a template, you don't need to follow it. Feel free to change it as you see fit.
## Name
Crypto
### Problem Description
These keys look completely different, yet they have something in common...
### Solution
Parse the public keys to get n1,e and n2,e.
Compute p = gcd(n1,n2).
If p > 1 then
   n1 = p * q1
   n2 = p * q2
Compute phi1 = (p-1)(q1-1) and phi2 = (p-1)(q2-1).
Compute d1 = inverse(e, phi1) and d2 = inverse(e, phi2).
RSA-decrypt:
   m1 = c1^d1 mod n1
   m2 = c2^d2 mod n2
Convert m1 and m2 to bytes of length equal to modulus size.
Unpad each message with OAEP using SHA-256 and empty label.
Concatenate the two plaintexts to get the flag.


Flag: FortID{4nd_1_Sa1d_Wh47_Ab07_4_C0mm0n_Pr1m3_F4ct0r?}

Code:

from pathlib import Path
from math import gcd
import hashlib, math
from cryptography.hazmat.primitives import serialization

###load keys
k1 = serialization.load_pem_public_key(Path("key1.pub").read_bytes())
k2 = serialization.load_pem_public_key(Path("key2.pub").read_bytes())
n1, e = k1.public_numbers().n, k1.publicnumbers().e
n2,  = k2.public_numbers().n, k2.public_numbers().e

###shared prime
p = gcd(n1, n2)
q1, q2 = n1//p, n2//p
phi1, phi2 = (p-1)(q1-1), (p-1)(q2-1)
d1 = pow(e, -1, phi1)
d2 = pow(e, -1, phi2)

###load ciphertexts
c1 = int(Path("flag1.enc").read_text().strip(), 16)
c2 = int(Path("flag2.enc").read_text().strip(), 16)

###RSA decrypt
m1 = pow(c1, d1, n1)
m2 = pow(c2, d2, n2)

###OAEP-SHA256 unpad
def mgf1(seed, length, h=hashlib.sha256):
    hlen = h().digest_size
    out = b""
    for i in range((length + hlen - 1)//hlen):
        out += h(seed + i.to_bytes(4,'big')).digest()
    return out[:length]

###def oaep_unpad(em, k=256, h=hashlib.sha256, label=b""):
    em = em.rjust(k, b"\x00")
    hlen = h().digest_size
    assert em[0] == 0
    masked_seed, masked_db = em[1:1+hlen], em[1+hlen:]
    seed = bytes(a^b for a,b in zip(masked_seed, mgf1(masked_db, hlen, h)))
    db   = bytes(a^b for a,b in zip(masked_db, mgf1(seed, k-hlen-1, h)))
    lhash = h(label).digest()
    assert db[:hlen] == lhash
    idx = db.index(b"\x01", hlen)
    return db[idx+1:]

k = (n1.bit_length()+7)//8
msg1 = oaep_unpad(m1.to_bytes(k, 'big'), k)
msg2 = oaep_unpad(m2.to_bytes(k, 'big'), k)

print((msg1+msg2).decode())
