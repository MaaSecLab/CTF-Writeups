# CTF Write-up: MuddyWater Intrusion  

## Challenge Description  
> *We caught a threat actor, called MuddyWater, brute-forcing a login for our Domain Controller. We have a packet capture of the intrusion. Can you figure out which account they logged into and what the password is?*  

> **Flag format:** `swampCTF{<username>:<password>}`  

### Provided Files  
- `muddywater.pcap`  

---

## Solution  

### 1. Analyzing the Packet Capture  
Since we have a **PCAP** file, we inspect it using **Wireshark**. We identify multiple authentication attempts using the **NTLMSSP protocol**.  

To filter for **successful authentication attempts**, we use the following Wireshark filter:  
```plaintext
smb2.cmd == 1 && smb2.nt_status == 0x00000000
```  
- `smb2.cmd == 1` → Filters **Session Setup Requests**  
- `smb2.nt_status == 0x00000000` → Filters **Successful Logins**  

This reveals **one successful authentication attempt**.  

### 2. Extracting NTLM Hash Data  
Following the related packet stream, we retrieve the necessary information for password cracking:  

- **Account:** `hackbackzip`  
- **Domain:** `DESKTOP-0TNOE4V`  
- **NTLM Response:** `eb1b0afc1eef819c1dccd514c962320101010000000000006f233d3d9f9edb01755959535466696d0000000002001e004400450053004b0054004f0050002d00300054004e004f0045003400560001001e004400450053004b0054004f0050002d00300054004e004f0045003400560004001e004400450053004b0054004f0050002d00300054004e004f0045003400560003001e004400450053004b0054004f0050002d00300054004e004f00450034005600070008006f233d3d9f9edb010900280063006900660073002f004400450053004b0054004f0050002d00300054004e004f004500340056000000000000000000`  
- **NTLM Server Challenge:** `d102444d56e078f4`  
- **NTProofStr:** `eb1b0afc1eef819c1dccd514c9623201`  

### 3. Formatting for Hashcat  
To crack the NTLM hash, we format it as follows:  

```plaintext
hackbackzip::DESKTOP-0TNOE4V:d102444d56e078f4:eb1b0afc1eef819c1dccd514c9623201:01010000000000006f233d3d9f9edb01755959535466696d0000000002001e004400450053004b0054004f0050002d00300054004e004f0045003400560001001e004400450053004b0054004f0050002d00300054004e004f0045003400560004001e004400450053004b0054004f0050002d00300054004e004f0045003400560003001e004400450053004b0054004f0050002d00300054004e004f00450034005600070008006f233d3d9f9edb010900280063006900660073002f004400450053004b0054004f0050002d00300054004e004f004500340056000000000000000000
```  

### 4. Cracking the Password  
We use **Hashcat** with mode `5600` (NTLMv2-SSP Hash) and the **rockyou.txt** wordlist:  

```bash
hashcat -m 5600 hash.txt /usr/share/wordlists/rockyou.txt
```  

This reveals the cracked password:  

- **Password:** `pikeplace`  

### 5. Submitting the Flag  
The final flag is:  

```plaintext
swampCTF{hackbackzip:pikeplace}
```

---

## Tools Used  
- **Wireshark** (Packet Analysis)  
- **Hashcat** (Password Cracking)  
- **rockyou.txt** (Wordlist for cracking)  


---

🏆 **Flag:** `swampCTF{hackbackzip:pikeplace}`  
