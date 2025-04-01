
# CTF Write-up: Translation  

## Challenge Description  
> *We found this program which we know has a flag somewhere, but nothing we've tried has been able to extract it. Can you figure it out?*  

### Running the Program  
The provided JavaScript program can be run using **NodeJS** (recommended version: 18.17.1 or higher).  

### Provided Files  
- `Translation.zip` containing:  
  - `challenge.js`  
  - `package.json`  
  - `package-lock.json`  

---

## Solution  

### 1. Analyzing the Code  


At first glance, the code seems normal, but **there are unusual whitespace patterns**, particularly in the indentation and spacing of certain lines. This suggests **the presence of hidden data using a whitespace-based cipher**.

---

### 2. Detecting a Whitespace Cipher  
Since the code structure looked suspicious, we suspected it might use the **Whitespace esoteric programming language** or a similar encoding technique.  

To confirm this, we used **dCode’s Whitespace decoder**:  

🔗 **Tool:** [dCode Whitespace Decoder](https://www.dcode.fr/whitespace-language)

By pasting the entire file into the decoder, we extracted the hidden message embedded in the whitespace characters.

---

### 3. Extracting the Flag  
Decoding the whitespace content revealed the flag:  

```plaintext
swampCTF{Whit30ut_W0rk5_W0nd3r5}
```

---

## Tools Used  
- **Whitespace Decoder (dCode)** – Extracting hidden characters  
- **Node.js** – Running and inspecting the script  
- **Text Editors (VSCode, Sublime Text)** – Viewing invisible whitespace  

---

🏆 **Flag:** `swampCTF{Whit30ut_W0rk5_W0nd3r5}`  
