import os
import re
import base64
import pyshark

os.environ["PATH"] += os.pathsep + r"D:\Wireshark"
pcap_path = "chall.pcap"

print("[] Scanning for potential base64 fragments...")

capture = pyshark.FileCapture(pcap_path, include_raw=True, use_json=True, tshark_path=r"D:\Wireshark\tshark.exe")

fragments = []

base64_pattern = re.compile(r'[a-zA-Z0-9+/=]{8,}')

packet_num = 0
for packet in capture:
    try:
        raw = packet.get_raw_packet()
        text = raw.decode(errors="ignore")

        matches = base64pattern.findall(text)
        for match in matches:
            for pad in ["", "=", "=="]:
                try:
                    decoded = base64.b64decode(match + pad).decode("utf-8", errors="ignore")
                    if any(x in decoded for x in ['grey', '{', '}', '', 'flag']):
                        print(f"[Packet #{packet.number}] Match: {match} → {decoded}")
                        fragments.append(decoded)
                        break
                except:
                    continue
    except:
        continue

capture.close()

print("\n[] Attempting reconstruction from decoded fragments...")
flag_candidates = set()

for i in range(len(fragments)):
    for j in range(i + 1, len(fragments)):
        combined = fragments[i] + fragments[j]
        if 'grey{' in combined and '}' in combined:
            maybe_flag = re.findall(r'grey{[^}]+}', combined)
            for flag in maybe_flag:
                flag_candidates.add(flag)

if flag_candidates:
    print("\nGuessed flag(s):")
    for flag in flag_candidates:
        print(flag)
else:
    print("No valid flags reconstructed.")
