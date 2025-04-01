# CTF Write-up: GP Nightmare  

## Challenge Description  
> *We have an old Windows Server 2008 instance that we lost the password for. Can you see if you can find one in this packet capture?*  

### Provided Files  
- `gpnightmare.pcap`  

---

## Solution  

### 1. Loading the PCAP File  
We start by opening the packet capture (`gpnightmare.pcap`) in **Wireshark**.  

### 2. Analyzing TCP Streams  
To look for valuable information, we follow the **TCP stream** by navigating to:  
**Wireshark → Right-click a TCP packet → Follow → TCP Stream**  

As we inspect the data, we come across an **XML structure** containing **user account information**:  

```xml
<?xml version="1.0" encoding="utf-8"?>
<Groups clsid="{3125E937-EC16-4b4c-9934-544FC6D24D26}">
    <User clsid="{DF5F1855-52E5-4d24-8B1A-D9BDE98BA1D1}" name="swampctf.com\Administrator" image="2"
          changed="2018-07-18 20:46:06" uid="{EF57DA28-5F69-4530-A59E-AAB58578219D}">
        <Properties action="U" newName="" fullName="" description=""
                    cpassword="dAw7VQvfj9rs53A8t4PudTVf85Ca5cmC1Xjx6TpI/cS8WD4D8DXbKiWIZslihdJw3Rf+ijboX7FgLW7pF0K6x7dfhQ8gxLq34ENGjN8eTOI="
                    changeLogon="0" noChange="1" neverExpires="1" acctDisabled="0" userName="swampctf.com\Administrator"/>
    </User>
</Groups>
```

We notice that the **"cpassword" field** contains an encrypted password.

---

### 3. Understanding Group Policy Password Storage  
Windows Server 2008 **stores passwords in Group Policy Preferences (GPP)** using **AES encryption**.  
We research how these passwords are encrypted and find the **public AES decryption key** used by Microsoft:  

🔗 **Reference:** [Microsoft Documentation on GPP Passwords](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-gppref/2c15cbf0-f086-4c74-8b70-1f2fa45dd4be)

---

### 4. Decrypting the Password  
We use the **AES decryption key** to recover the original password:  

```bash
gpp-decrypt "dAw7VQvfj9rs53A8t4PudTVf85Ca5cmC1Xjx6TpI/cS8WD4D8DXbKiWIZslihdJw3Rf+ijboX7FgLW7pF0K6x7dfhQ8gxLq34ENGjN8eTOI="
```

This reveals the **decrypted password** and gives us the **final flag**:  

```plaintext
swampCTF{4v3r463_w1nd0w5_53cur17y}
```

---

## Tools Used  
- **Wireshark** (Packet analysis)  
- **Microsoft Documentation** (Understanding Windows Server 2008 encryption)  

---

🏆 **Flag:** `swampCTF{4v3r463_w1nd0w5_53cur17y}`  
