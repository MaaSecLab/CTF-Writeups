# Challenge Description:

We were able to listen in on our opponents for a while and managed to capture the ciphertexts and plaintexts of 
their communication, but were eventually kicked out. We’ll send you a dump of what we managed to get so far.

Long story short, there are pairs of encrypted and decrypted communications.
We have reason to believe they're not following !!!!otp-imal!!!! security practices, 
and the most valuable communication should be happening any second now...


# Initial Analysis:
We were given a ZIP file containing:
Several folders (M1 through M5), each with:
     encrypted.txt → a binary ciphertext
     decrypted.txt → a binary plaintext followed by the ASCII translation

A separate file Important_Message_Captured.txt containing a long binary string (the final encrypted message we need to decrypt).
The hint "otp-imal security" strongly suggests a One-Time Pad (OTP) cipher — and more importantly, OTP misuse, likely through keystream reuse, aka a “many-time pad” scenario.


# Exploit Strategy:
In a secure OTP, the keystream (random pad) must be used only once.
But if the same keystream is reused with multiple plaintexts, you can recover it via:

            keystream = ciphertext XOR plaintext




# Steps to solve:

1. Extract Known Keystream
    For each of the five messages (M1–M5):
    Read the binary plaintext from the first line of decrypted.txt
    Read the binary ciphertext from encrypted.txt
    XOR the plaintext and ciphertext bit-by-bit to extract the keystream
    Store the keystream bits by position

2. Apply Keystream to the Final Message
    Read the final encrypted binary from Important_Message_Captured.txt
    XOR the bits at all known positions with the recovered keystream
    For unknown bits, assume 0 (which just means “don't decrypt”)
    Convert the resulting binary string into ASCII

3. Search for the Flag
    The decrypted message contained mostly garbage due to incomplete keystream coverage.
    However, near the end of the message, we found the flag:

Result ...÷\x9eampCTF{Nev3r_r3Use_a_0TP}] -> swampCTF{Nev3r_r3Use_a_OTP}


```python
# Your Python code
import os

def xor_bin_strings(a, b):
    return ''.join(str(int(x) ^ int(y)) for x, y in zip(a, b))

def binary_to_ascii(binary_str):
    chars = [binary_str[i:i+8] for i in range(0, len(binary_str), 8)]
    return ''.join(chr(int(char, 2)) for char in chars if len(char) == 8)

def ascii_to_binary(s):
    return ''.join(f"{ord(c):08b}" for c in s)

updated_comms_path = "/home/rr/Desktop/scripts/ciphertext-plaintextOTP/Captured_comms"  # <-- change this to your actual path

positioned_keystream = {}

for i in range(1, 6):
    msg_path = os.path.join(updated_comms_path, f'M{i}')
    
    with open(os.path.join(msg_path, 'decrypted.txt'), 'r') as f:
        contents = f.read().strip().splitlines()
    
    binary_plaintext = contents[0].strip()
    ascii_plaintext = contents[1].strip()
    ascii_binary = ascii_to_binary(ascii_plaintext)
    
    min_len = min(len(binary_plaintext), len(ascii_binary))
    if binary_plaintext[:min_len] != ascii_binary[:min_len]:
        print(f"[!] M{i} mismatch between binary and ASCII representation.")
    
    with open(os.path.join(msg_path, 'encrypted.txt'), 'r') as f:
        ciphertext = f.read().strip()
    
    for j in range(min_len):
        kbit = str(int(ciphertext[j]) ^ int(binary_plaintext[j]))
        positioned_keystream[j] = kbit

with open(os.path.join(updated_comms_path, 'Important_Message_Captured.txt'), 'r') as f:
    final_ciphertext_bits = f.read().strip()

final_keystream = ''.join(positioned_keystream.get(i, '0') for i in range(len(final_ciphertext_bits)))
final_decrypted_bits = xor_bin_strings(final_ciphertext_bits, final_keystream)
final_decrypted_text = binary_to_ascii(final_decrypted_bits)

print(final_decrypted_text[-500:])


# Show the last 1000 characters
print("\n[+] Decrypted tail (for manual inspection):")
print(final_decrypted_text[-1000:])

# Try flexible flag detection
import re
match = re.search(r'[a-zA-Z0-9_\-]{0,10}CTF\{.*?\}', final_decrypted_text)
if match:
    print(f"\n🎉 Flag found: {match.group()}")
else:
    print("\n[!] Flag not found.")

