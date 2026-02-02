# PascalCTF – Elliptic Curve Smooth Order Writeup

## Challenge Description

The casino gambling system uses an elliptic curve cryptosystem:

E: y^2 = x^3 + 1 (mod p)

with:
p = 1844669347765474229
n = p + 1

A public base point G and a point Q = sG are given, where the secret scalar `s` is chosen randomly:

s = random_8_bytes % n

The server allows interaction via:

nc curve.ctf.pascalctf.it 5004

The goal is to recover the secret scalar `s` and submit it to obtain the flag.

---

## Key Observation

The group order n is extremely smooth:

n = 2 · 3² · 5 · 7 · 11 · 13 · 17 · 19 · 23 · 29 · 31 · 37 · 41 · 43 · 47

Since the order factors completely into small primes, the discrete logarithm problem becomes trivial using the Pohlig–Hellman algorithm.

This means we can compute:

Q = sG  → recover s efficiently

without using the oracle at all.

---

## Solution Strategy

1. Parse curve parameters p, n, G, and Q from the server output.
2. Factor n into small prime powers.
3. For each factor pᵉ:
   - Compute reduced subgroup generators.
   - Solve discrete log via brute force.
4. Combine results using the Chinese Remainder Theorem (CRT).
5. Submit the recovered secret to the server to get the flag.

---

## Mathematical Background

For each prime factor pᵉ of n:

Let:
g_i = (n / pᵉ) · G  
h_i = (n / pᵉ) · Q  

Then solve:
h_i = x_i · g_i   (mod p)

Since pᵉ is small, brute force works.

Finally, combine all x_i using CRT to obtain the full secret modulo n.

---

## Solver Script

```python
#!/usr/bin/env python3
import re
import socket
import time

HOST = "curve.ctf.pascalctf.it"
PORT = 5004

FACTORS = [
    (2,1),(3,2),(5,1),(7,1),(11,1),(13,1),(17,1),(19,1),
    (23,1),(29,1),(31,1),(37,1),(41,1),(43,1),(47,1),
]

class Point:
    __slots__ = ("x","y")
    def __init__(self,x,y):
        self.x=x; self.y=y

INF = Point(None,None)

def inv(a,p):
    return pow(a%p,-1,p)

def add(P,Q,p,a=0):
    if P.x is None: return Q
    if Q.x is None: return P
    if P.x==Q.x and (P.y+Q.y)%p==0: return INF
    if P.x==Q.x:
        s=(3*P.x*P.x+a)*inv(2*P.y,p)%p
    else:
        s=(Q.y-P.y)*inv(Q.x-P.x,p)%p
    x3=(s*s-P.x-Q.x)%p
    y3=(s*(P.x-x3)-P.y)%p
    return Point(x3,y3)

def mul(k,P,p,a=0):
    R=INF
    A=P
    while k:
        if k&1: R=add(R,A,p,a)
        A=add(A,A,p,a)
        k>>=1
    return R

def dlog_bruteforce(g,h,order,p):
    cur=INF
    for x in range(order):
        if cur.x==h.x and cur.y==h.y:
            return x
        cur=add(cur,g,p)
    raise ValueError("dlog not found")

def crt_pair(a1,m1,a2,m2):
    t=((a2-a1)%m2)*inv(m1,m2)%m2
    x=a1+m1*t
    return x%(m1*m2), m1*m2

def main():
    with socket.create_connection((HOST,PORT)) as s:
        data=s.recv(4096).decode()
        p=int(re.search(r"mod\s+(\d+)",data).group(1))
        n=int(re.search(r"n\s*=\s*(\d+)",data).group(1))
        gx,gy=map(int,re.search(r"G\s*=\s*\((\d+),(\d+)\)",data).groups())
        qx,qy=map(int,re.search(r"Q\s*=\s*\((\d+),(\d+)\)",data).groups())

        G=Point(gx,gy)
        Q=Point(qx,qy)

        x_mod,mod=0,1
        for prime,exp in FACTORS:
            pe=prime**exp
            cof=n//pe
            g_i=mul(cof,G,p)
            h_i=mul(cof,Q,p)
            x_i=dlog_bruteforce(g_i,h_i,pe,p)
            x_mod,mod=crt_pair(x_mod,mod,x_i,pe)

        secret=x_mod%n
        secret_hex=f"{secret:x}"

        s.sendall(b"1\n")
        s.recv(1024)
        s.sendall((secret_hex+"\n").encode())
        print(s.recv(4096).decode())

if __name__=="__main__":
    main()
```

---

## Result

The recovered secret is submitted in hex format and the server returns the flag.

---

## Conclusion

This challenge is broken by design due to a smooth group order.  
Elliptic Curve Discrete Logarithm is only secure when the group order has a large prime factor.

Using Pohlig–Hellman and CRT allows instant recovery of the private key.

---


