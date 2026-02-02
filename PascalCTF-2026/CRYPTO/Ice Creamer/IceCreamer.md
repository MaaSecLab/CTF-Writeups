# PascalCTF – Ice Creamer Writeup

## Challenge Description

The service prints a square linear system of equations where each unknown corresponds to the ASCII value of a character in the flag:

x_0 = ord(flag[0])
x_1 = ord(flag[1])
...
x_{n-1} = ord(flag[n-1])

The server outputs exactly n equations with n unknowns, each being a random integer linear combination of the variables.

Goal: Recover all x_i, convert them back to characters, and print the flag

---

## Solution Strategy

1. Connect to the remote service.
2. Parse the equations into matrix form A x = b.
3. Solve the system using Gaussian elimination with exact rational arithmetic.
4. Convert the resulting integers into ASCII characters.
5. Print the reconstructed flag.

Python’s fractions.Fraction is used to avoid floating-point errors.

---

## Solver Script

```python
#!/usr/bin/env python3
import re
from fractions import Fraction
import socket

HOST = "cramer.ctf.pascalctf.it"
PORT = 5002

term_re = re.compile(r'([+-]?\d+)\*x_(\d+)')

def recv_all(sock: socket.socket) -> str:
    sock.settimeout(5)
    data = b""
    while True:
        try:
            chunk = sock.recv(4096)
            if not chunk:
                break
            data += chunk
        except socket.timeout:
            break
    return data.decode(errors="replace")

def parse_system(text: str):
    """
    Returns (A, b) where A is n x n list of Fractions and b is n list of Fractions.
    """
    lines = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if "Solve the system" in line:
            break
        if "= " in line and "*x_" in line:
            lines.append(line)

    if not lines:
        raise ValueError("No equations found in output.")

    # Determine n from max x_i index
    max_idx = -1
    for ln in lines:
        for _, idx in term_re.findall(ln):
            max_idx = max(max_idx, int(idx))
    n = max_idx + 1

    A = [[Fraction(0) for _ in range(n)] for __ in range(n)]
    b = [Fraction(0) for _ in range(n)]

    if len(lines) != n:
        # Should be square in this challenge, but keep it explicit.
        raise ValueError(f"Expected {n} equations, got {len(lines)}.")

    for row, ln in enumerate(lines):
        left, right = ln.split("=")
        right = right.strip()
        b[row] = Fraction(int(right))

        for coeff, idx in term_re.findall(left):
            c = int(coeff)
            j = int(idx)
            A[row][j] += Fraction(c)

    return A, b

def gauss_solve(A, b):
    """
    Solve A x = b with exact Fractions. A is n x n, b is n.
    Returns x list of Fractions.
    """
    n = len(A)
    # Augment matrix
    M = [A[i][:] + [b[i]] for i in range(n)]

    # Forward elimination
    for col in range(n):
        # Find pivot
        pivot = None
        for r in range(col, n):
            if M[r][col] != 0:
                pivot = r
                break
        if pivot is None:
            raise ValueError("Singular matrix / no unique solution (unexpected).")

        # Swap pivot row into place
        if pivot != col:
            M[col], M[pivot] = M[pivot], M[col]

        # Normalize pivot row
        pv = M[col][col]
        for c in range(col, n+1):
            M[col][c] /= pv

        # Eliminate below
        for r in range(col+1, n):
            factor = M[r][col]
            if factor == 0:
                continue
            for c in range(col, n+1):
                M[r][c] -= factor * M[col][c]

    # Back substitution
    x = [Fraction(0) for _ in range(n)]
    for r in range(n-1, -1, -1):
        x[r] = M[r][n] - sum(M[r][c] * x[c] for c in range(r+1, n))
        # M[r][r] should be 1 after normalization
    return x

def main():
    with socket.create_connection((HOST, PORT), timeout=5) as sock:
        text = recv_all(sock)

    A, b = parse_system(text)
    sol = gauss_solve(A, b)

    # Convert to chars
    vals = []
    for i, v in enumerate(sol):
        if v.denominator != 1:
            raise ValueError(f"x_{i} is not an integer: {v}")
        vals.append(int(v))

    inner = "".join(chr(v) for v in vals)
    print("pascalCTF{" + inner + "}")

if __name__ == "__main__":
    main()
```

## Conclusion

This challenge reduces to solving a linear system over the rationals and decoding the result as ASCII characters.
Using Gaussian elimination with Fraction ensures correctness and reliability.
