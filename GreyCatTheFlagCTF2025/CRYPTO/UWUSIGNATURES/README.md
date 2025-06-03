## Uwusignatures 
### Problem Description
As an uwu girl, I decided to make this digital signature scheme to share my signatures with everyone!

I'll only show you half of my signature though, because I'm shy...

Surely, no one would steal from a cutie like myself... right?

`nc challs.nusgreyhats.org 33301 `

`nc challs2.nusgreyhats.org 33301 `

<br>

### Provided Files
#### uwusignatures.py
```python
from Crypto.Util.number import *
import json
import hashlib

KEY_LENGTH = 2048
FLAG = "grey{fakeflagfornow}"

class Uwu:
    def __init__(self, keylen):
        self.p = getPrime(keylen)
        self.g = getRandomRange(1, self.p)
        self.x = getRandomRange(2, self.p) # x is private key
        self.y = pow(self.g, self.x, self.p) # y is public key
        self.k = getRandomRange(1, self.p)
        while GCD(self.k, self.p - 1) != 1:
            self.k = getRandomRange(1, self.p)
        print(f"{self.p :} {self.g :} {self.y :}")
        print(f"k: {self.k}")
    def hash_m(self, m):
        sha = hashlib.sha256()
        sha.update(long_to_bytes(m))
        return bytes_to_long(sha.digest())
    def sign(self, m):
        assert m > 0
        assert m < self.p
        h = self.hash_m(m)
        r = pow(self.g, self.k, self.p)
        s = ((h - self.x * r) * pow(self.k, -1, self.p - 1)) % (self.p - 1) 
        return (r, s)
    def verify(self, m, signature):
        r, s = signature
        assert r >= 1
        assert r < self.p
        h = self.hash_m(m)
        lhs = pow(self.g, h, self.p)
        rhs = (pow(self.y, r, self.p) * pow(r, s, self.p)) % self.p
        return lhs == rhs 

def main():
    print("Welcome to my super uwu secure digital signature scheme!")
    uwu = Uwu(KEY_LENGTH)
    sign_count = 0   
    while True:
        print("1. Show me some of your cutesy patootie signatures!")
        print("2. Get some of my uwu signatures (max 2)")
        choice = int(input("> "))
        if choice == 1:
            data = json.loads(input("Send me a message and a signature: "))
            m, r, s = data["m"], data["r"], data["s"]
            if m == bytes_to_long(b"gib flag pls uwu"):
                if uwu.verify(m, (r, s)):
                    print("Very cutesy, very mindful, very demure!")
                    print(FLAG)
                    exit()
                else:
                    print("Very cutesy, but not very mindful")
                    exit()
            else:
                print("Not very cutesy")
                exit()
        elif choice == 2:
            if sign_count >= 2:
                print("Y-Y-You'd steal from poor me? U_U")
                exit()
            data = json.loads(input("Send me a message: "))
            m = data["m"]
            if type(m) is not int or m == bytes_to_long(b"gib flag pls uwu"):
                print("Y-Y-You'd trick poor me? U_U")
                exit()
            r, s = uwu.sign(m)
            print(f"Here's your uwu signature! {s :}")
            sign_count += 1
        else:
            print("Not very smart of you OmO")
            exit()

if __name__ == "__main__":
    main()
```
<br>

### Solution
In the code, we can see that if we select **1** and submit a message "gib flag pls uwu", the flag will be given to us, so that is exactly what we are going to do. But, we need to find a couple of things to doing that.

#### Step 1
Run the **nc** command on a linux webshell. You will see that the **p**, **g**, **y**, and **k** values are given to you. These values are:
```
p = [prime]
g = [generator]
y = [public key] 
k = [nonce value]
```

#### Step 2
1. Select **2** to submit a message as an integer value
   - This allows you to obtain a signature of your message
2. In my case, I have submitted `{"m": 448378203247}` which is "hello" as a long. 
3. Copy the signature given.

#### Step 3 
Calculate the missing **r** value using the leaked **k**:

```python
r = pow(g, k, p)  # r = g^k mod p
```


#### Step 4
Now, we can calculate the private key **X**. The code gives us the equation

```python
s = ((h - self.x * r) * pow(self.k, -1, self.p - 1)) % (self.p - 1)
```

We can rearrange this formula to calculate **x**.
```python
x = ((h - s * k) * pow(r, -1, p-1)) % p-1
```


#### Step 5
1. Compute hash of target message:

```python
m_target = bytes_to_long(b"gib flag pls uwu")
h_target = sha256_long(m_target)
```

1. Calculate signature:

```python
s_target = ((h_target - x * r) * pow(k, -1, p-1)) % p-1
```


#### Step 6
1. Select **1**
2. Send the JSON payload containing **m**, **r**, and **s**
3. You will then recieve the flag



### Final Decryption Algorithm
```python
from Crypto.Util.number import bytes_to_long
import hashlib
import json

# Step 1: Note down values given by server
p = 31940470473383084784328811065886626868990171555271930907683148815033282669491324030995537327093511018499116665757713347579545199872884109126308368912695808050771898627763908595987739851216254747981177065129562738962188553010314098066483984562809927454673367548146538211105498553246312156011921765168737618805514203761278541368782313861430306944703291975731033041554621305117078771452185860676463530294963492950206183834389434466176373146015835772066968139955358664323127334506576394544099827650102444068024568326148373574019538182218070513836285298318218481639859648479204103304310095263940246706421004193896407335297
g = 8192222294410690021047189075242055127065383674165613436969719718610734827329884661077386445679863215356599064719176621474522754299455801180324230016034385741650766831075662603515507043698299756797913874176983627595262910224889325185478901714027701018399528095733413101440255423903852486907095885588759606054472607234991395133873034265697034818411314328864171400036150207258279347445753072438831597384039226449490321836654919424301607303763105033856169328834075682155437754239542061687170353797738502759108090851728810576118562398525482049946862947806142788738834162985197522519645184224212213363541343391630987657661
y = 8666322459489152192381458032411417013963753862667489022346910494876675717472001154225902659079392934590222526923413209200968584032752947294668313283155341096318941570566952190887532825235803985693561837357128658692366048033792221536220103070022854565885820447807846215505583395078392407013964282841384343338340532017794242183355402080518228008737313365957326233079150190191985478883346952987257304615477403828027575773244321048380922373950863782069067038831592298300019536399510426890518014534669242336223080553685143678922246705686862223089579593004319997157487852336700418147989386959845820483442272717191871872783
k = 20003195546765648475709052871522397428294233626877638756779639038689041201587615505072278781045790583590528258352681216431699614454958285495157372428343898817024148007911695802985613279128678112671051012800146784319055012972291113254558693550302731659645965778413898111034536608853043991039968726154673041192335163970760123137822148154047010464558656374431164208300189205511801913967723209981468425459708557489196600767126100055584013228175649906903581936005513322578546625858305693545145695153428568358819442849823894508499878039404643234156828623932457730708769590000517848965397602826603459233265511452432192900269

# Step 2: Getting Signature
m = 448378203247  # Message that I submitted
s = 31303252926290997664394489061538268243258455599280222431380218798980260412739300983746153522795672269802282209202912346409959342806160627515896509745970218838820428179656698379096977639666132440666529193686858339703425997743043986389013843841006595159902513694839507187808958810959537569334930663953444623345442582495012974715692432896151131485530996279568044415293199643604933954669065498063165414327222747525469854716213326945843439459233693652573725698532871491475795966265716822358023176861795087161613112334879311853689988387564321321813231363280929499515401193812794638242304139290056987751241501942597888276920

def sha256_long(m):
    return int.from_bytes(hashlib.sha256(m.to_bytes((m.bit_length()+7)//8, 'big')).digest(), 'big')

# Step 3: Calculate r
r = pow(g, k, p)  # r = g^k mod p

# Step 4: Calculate X
h = sha256_long(m)
x = ((h - s * k) * pow(r, -1, p-1)) % (p-1)

# Step 5: Forge signature
m_target = bytes_to_long(b"gib flag pls uwu")
h_target = sha256_long(m_target)
s_target = ((h_target - x * r) * pow(k, -1, p-1)) % (p-1)

# Step 6: Print values to submit
print(json.dumps({
    "m": m_target,
    "r": r,
    "s": int(s_target)
}))
```


Have a great day :D [https://github.com/JoelDha](https://github.com/JoelDha)