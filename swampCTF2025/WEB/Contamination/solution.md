
# CTF Write-up: Reverse Proxy Bypass  

## Challenge Description  
> *I have created a safe reverse proxy that only forwards requests to retrieve debug information from the backend. What could go wrong?*  

### Target  
- **Website**  

### Files Provided  
- **contamination.zip**  
  - `Proxy/server.rb`  
  - `Backend/backend.py`  

---

## Solution  

### 1. Analyzing the Backend  
Looking at **backend.py**, we found the following routes:  
- **`getFlag`** – *Seems to retrieve the flag if an exception occurs.*  
- **`getInfo`** – *Returns non-useful debug information.*  

The **proxy (server.rb)** prevents direct access to `getFlag`, only allowing requests to `getInfo`.

---

### 2. Bypassing the Proxy  
We experimented with the API requests and found a **bypass technique** using **parameter pollution**:  

```http
http://chals.swampctf.com:41234/api?&action=getFlag&action=getInfo
```  

This bypasses the **proxy verification** and allows us to access the `getFlag` action.

---

### 3. Triggering an Exception in Python  
When sending **normal JSON**, we got:  
```json
{
  "message": "Parsed JSON successfully"
}
```  
This confirmed we were accessing `getFlag`, but we still needed to **crash the Python JSON parser** while keeping the **Ruby one intact**.

---

### 4. Finding the Exploit  
Through experimenting, we discovered that the following **malformed JSON** caused a crash in **Python’s JSON parser**, but **not in Ruby**:  

```json
{
  "key": "\x80"
}
```

This caused an **exception in Python**, revealing the **flag**.

---

## Flag  
```plaintext
swampCTF{1nt3r0p3r4b1l1ty_p4r4m_p0llut10n_x7q9z3882e}
```

---

## Tools & Techniques Used  
- **Source Code Review** – Understanding the **backend.py** and **server.rb** logic.  
- **Parameter Pollution** – Exploiting how **multiple parameters are handled** in URLs.  
- **JSON Parsing Quirks** – Using **non-UTF8 characters (`\x80`)** to crash Python’s JSON parser.  


---

🏆 **Final Flag:** `swampCTF{1nt3r0p3r4b1l1ty_p4r4m_p0llut10n_x7q9z3882e}`
