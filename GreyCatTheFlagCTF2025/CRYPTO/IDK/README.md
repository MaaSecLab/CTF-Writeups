## IDK 
### Problem Description
I've been really into zero knowledge proofs lately! I wrote a simple program that can prove that I'm the only person who knows how to decrypt this message, and because I'm so confident, I'll even give you some dumps of my proofs!

<br>

### Provided Files
1. verifier.py
2. prover.py
3. dump1.txt
4. dump2.txt
5. message.txt

<br>

### Solution
In prover.py, it became evident that **p** and **q** are the same value, even though in an RSA algorithm, they should be different values. Therefore, we needed to find the correct values using the dump files provided. And then decrypt the flag in message.txt

- The dump files contain:
  - **F_hex**
  - **sigma_values**
  - **mu_values**
- The message file contains:
  - **N**
  - **e**
  - **c**


#### Step 1
Extract mu values as integers.

```python
def parse_dump_file(filename):
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f.readlines()]
    
    kappa = 128
    alpha = 65537
    m1 = ceil(kappa / log2(alpha))  # ≈ 8
    m2 = ceil(kappa * 32 * 0.69314718056)  # ≈ 2843
    
    # Extract mu values (skip F_hex and sigma values)
    mu_values = lines[m1+1:m1+1+m2]
    
    mu_ints = []
    for mu_hex in mu_values:
        if mu_hex == '0':
            mu_ints.append(0)
        else:
            mu_ints.append(int(mu_hex, 16))
    
    return mu_ints
```

#### Step 2
For modulus `N=pq`, any quadratic residue has four square roots: `±a, ±b mod N`. If two different roots `(a ≠ ±b)` are found for the same residue:

```math
a² ≡ b² \mod N ⟹ (a-b)(a+b) ≡ 0 \mod N
```

This implies `gcd(a-b, N)` reveals **p** or **q**.

```python
if (mu1 != 0 and mu2 != 0 and 
    mu1 != mu2 and 
    mu1 != (N - mu2) % N):
    # Valid collision found
```



#### Step 3
Iterate through mu pairs until a non-trivial GCD is found (neither 1 nor N itself):

```python
diff = abs(mu1 - mu2)
factor = gcd(diff, N)

if 1 < factor < N:
    return factor, N//factor
```

#### Step 4
Use factorization to get the private key. 
1. Compute `φ(N) = (p-1)(q-1)`
```python
phi = (p - 1) * (q - 1)
```


2. Find private exponent:

```python
d = pow(e, -1, phi)
```

#### Step 5
Decrypt the ciphertext from message.txt.

```python
m = pow(c, d, N)
flag = m.to_bytes((m.bit_length() + 7) // 8, 'big').decode('utf-8') # Converts flag to string
```

<br>

### Final Decryption Algorithm
```python
from math import gcd, ceil, log2

def parse_dump_file(filename):
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f.readlines()]
    
    kappa = 128
    alpha = 65537
    m1 = ceil(kappa / log2(alpha))  # ≈ 8
    m2 = ceil(kappa * 32 * 0.69314718056)  # ≈ 2843
    
    # Extract mu values (skip F_hex and sigma values)
    mu_values = lines[m1+1:m1+1+m2]
    
    mu_ints = []
    for mu_hex in mu_values:
        if mu_hex == '0':
            mu_ints.append(0)
        else:
            mu_ints.append(int(mu_hex, 16))
    
    return mu_ints

def factor_rsa_from_dumps(dump1_file, dump2_file, N):
    mu1_values = parse_dump_file(dump1_file)
    mu2_values = parse_dump_file(dump2_file)
    
    for i in range(min(len(mu1_values), len(mu2_values))):
        mu1 = mu1_values[i]
        mu2 = mu2_values[i]
        
        if (mu1 != 0 and mu2 != 0 and 
            mu1 != mu2 and 
            mu1 != (N - mu2) % N):
            
            diff = abs(mu1 - mu2)
            factor = gcd(diff, N)
            
            if 1 < factor < N:
                return factor, N // factor
    
    return None, None

# RSA parameters from message.txt
N = 15259097618051614944787283201589661884102249046616617256551480013493757323043057001133186203348289474506700039004930848402024292749905563056243342761253435345816868449755336453407731146923196889610809491263200406510991293039335293922238906575279513387821338778400627499247445875657691237123480841964214842823837627909211018434713132509495011638024236950770898539782783100892213299968842119162995568246332594379413334064200048625302908007017119275389226217690052712216992320294529086400612432370014378344799040883185774674160252898485975444900325929903357977580734114234840431642981854150872126659027766615908376730393
e = 65537
c = 6820410793279074698184582789817653270130724082616000242491680434155953264066785246638433152548701097104342512841159863108848825283569511618965315125022079145973783083887057935295021036668795627456282794393398690975486485865242636068814436388602152569008950258223165626016102975011626088643114257324163026095853419397075140539144105058615243349994512495476754237666344974066561982636000283731809741806084909326748565899503330745696805094211629412690046965596957064965140083265525186046896681441692279075201572766504836062294500730288025016825377342799012299214883484810385513662108351683772695197185326845529252411353

# Factor N using the dumps
p, q = factor_rsa_from_dumps('dump1.txt', 'dump2.txt', N)

if p and q:
    # Decrypt the message
    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)
    m = pow(c, d, N)
    
    # Convert to string
    flag = m.to_bytes((m.bit_length() + 7) // 8, 'big').decode('utf-8')
    print(f"Flag: {flag}")
```


Have a great day :D [https://github.com/JoelDha](https://github.com/JoelDha)