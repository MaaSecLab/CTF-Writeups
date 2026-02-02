
# Challenge Writeup — ZazaStore

## Description
This challenge is solved by chaining a broken authentication mechanism with a logic flaw in cart price calculation. Authentication can be bypassed by supplying any username and password. By adding a non-existent product to the cart, the checkout total becomes NaN, bypassing the balance check. This allows the expensive item RealZa, mapped directly to process.env.FLAG, to be added to the inventory, causing the flag to be rendered on the inventory page.

## Authentication Bypass

The login endpoint does not validate credentials and only checks for their presence:
```
app.post('/login', (req, res) => {
        const { username, password } = req.body;
        if (username && password) {
            req.session.user = true;
            req.session.balance = 100;
            return res.json({ success: true });
        }
    });
```

Any credentials work (e.g. admin:admin), granting a valid authenticated session.

![[Pasted image 20260202202404.png]]
## Flag Location

From the source code, the item RealZa is mapped directly to the flag:
```
const content = {
        "RealZa": process.env.FLAG,
        ...
    };
```

If RealZa exists in the user’s inventory, the flag will be displayed on /inventory.  
However, RealZa costs more than the available balance.
## NaN Checkout Logic Bug

During checkout, the total cost is calculated without validating that products exist in the price list:
```
let total = 0;
    for (const product in cart) {
        total += prices[product] * cart[product];
    }
```
    

If a product is not present in prices, the calculation results in NaN.  
The balance check then incorrectly allows checkout. Since NaN > balance is always false, the checkout succeeds.

![[Pasted image 20260202202541.png]]
![[Pasted image 20260202202556.png]]
![[Pasted image 20260202202619.png]]
## Exploitation

1. Log in with any credentials  
2. Add a non-existent product to the cart (forces NaN)  
3. Add RealZa to the cart  
4. Checkout succeeds despite insufficient balance  
5. Visit /inventory to retrieve the flag  

![[Pasted image 20260202202636.png]]