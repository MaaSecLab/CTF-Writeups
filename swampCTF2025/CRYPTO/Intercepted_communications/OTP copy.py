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


print("\n[+] Decrypted tail (for manual inspection):")
print(final_decrypted_text[-1000:])

import re
match = re.search(r'[a-zA-Z0-9_\-]{0,10}CTF\{.*?\}', final_decrypted_text)
if match:
    print(f"\n🎉 Flag found: {match.group()}")
else:
    print("\n[!] Flag not found.")

