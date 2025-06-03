## **TUNG\_TUNG\_TUNG\_SAHUR**

### Problem Description

We are given code that encrypts a flag using RSA, along with its output:

```python
from Crypto.Util.number import getPrime, bytes_to_long

flag = "grey{flag_here}"

e = 3
p, q = getPrime(512), getPrime(512)
N = p * q 
m = bytes_to_long(flag.encode())
C = pow(m, e)

assert C < N 
while (C < N):
    C *= 2
    print("Tung!")

# now C >= N

while (C >= N):
    C -= N 
    print("Sahur!")

print(f"{e = }")
print(f"{N = }")
print(f"{C = }")
```

---

### Solution

From the output file, we observe:

* **164 lines** of `"Tung!"`
* **1 line** of `"Sahur!"`
* Values for **`e = 3`**, `N`, and `C`

#### Key Observations:

* The encryption uses RSA:
  $\text{Ciphertext} = \text{message}^e$
* For each `"Tung!"`, the ciphertext `C` is doubled:
  → $C = \text{original\_C} \times 2^{164}$
* For each `"Sahur!"`, `N` is subtracted once:
  → $\text{final\_C} = C - N$

#### So, we get:

$$
\text{final\_C} = (\text{original\_C} \times 2^{164}) - N
$$

Solving for `original_C`:

$$
\text{original\_C} = \frac{\text{final\_C} + N}{2^{164}} = \text{message}^3
$$

Take the cube root of `original_C`, convert it back to bytes, and extract the flag.

---

### Flag

**`grey{tUn9_t00nG_t0ONg_x7_th3n_s4hUr}`**

---
