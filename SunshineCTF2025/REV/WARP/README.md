## Name
Warp

### Problem Description
The warp tunnel is letting people past our firewall!

### Solution
## Summary 

I found that an XDP program attached to the host interface checked for a packet beginning with `W4rp` followed by a 30-byte secret; after reconstructing the secret I sent the exact UDP packet from Windows to WSL and the userspace program printed the flag.

---



## What I observed

1. Running the `warp` binary required root (it attaches an eBPF/XDP program). I started it with `sudo` and logged its output to a file so I could watch live:

```bash
mkdir -p ~/warp_chal
cp /mnt/c/Users/User/Downloads/warp ~/warp_chal/warp
cd ~/warp_chal
chmod +x warp
sudo nohup ./warp > /tmp/warp.out 2>&1 &
# then in another terminal:
tail -f /tmp/warp.out
```

2. The program printed `This proram is listening...` (note: the program has a typo). When I sent packets from WSL to `127.0.0.1` the program did not see them because XDP was attached to the physical interface and loopback traffic doesn't traverse that ingress path.

3. `ip -4 addr show` revealed a non-loopback IP like `172.29.146.148` on `eth0` and `ip -d link show` showed `xdpgeneric` attached — this confirmed the XDP program was active on `eth0`.

---

## Recon / Reverse engineering notes (how I derived the payload)

* I inspected the embedded BPF object / the binary to find two important data items:

  * a 4-byte `prefix` containing `W4rp`
  * a 30-byte `check` array in `.rodata` that the BPF program uses to derive the expected bytes

* The userspace code (and the BPF program) compared the packet payload's first bytes to `prefix` and then compared the rest to a transformed version of `check` (the BPF used a small transform: `check[i] ^ 0x60` and additional printable handling). The end result was a particular 30-byte string the program wanted.

* From the binary analysis I reconstructed the **exact payload** the program compares against (prefix + 30-byte secret). In my interactive trial-and-error I discovered the program would print `Message recieved, no flag warped. <truncated>` when the payload reached only part of the secret: that helped me realize the packet being received was mangled by PowerShell escaping (the backtick character). Fixing that to send the literal backtick completed the payload and produced the flag.

---

## Exact payload I used

> **Important:** keep the payload bytes exact (including the backtick `` ` `` and punctuation).

```
W4rpDF?L?_?08A`0q!u04@5608_03CCCCN
```

*(Note: during my verification I used this exact byte sequence as raw ASCII payload sent over UDP to the WSL interface IP.)*

---

## How I sent the packet (reproducible steps)

Because XDP on `eth0` inspects ingress packets, I sent the packet from Windows to WSL (Windows -> WSL forces ingress).

### On WSL (start the challenge and watch output)

```bash
cd ~/warp_chal
sudo nohup ./warp > /tmp/warp.out 2>&1 &
# note the PID printed by the shell; then:
tail -f /tmp/warp.out
```

Look for `This proram is listening...` and then any `Message recieved...` or the eventual `Oh look! A flag came out of the warp tunnel!` line.

### On Windows PowerShell (send literal bytes; single quotes preserve the backtick)

```powershell
$ip = '172.29.146.148'   # replace with the WSL eth0 IP you found with `ip addr`
$port = 496              # the challenge listened on 496 for me; if nothing happens try 4242
$payload = [System.Text.Encoding]::ASCII.GetBytes('W4rpDF?L?_?08A`0q!u04@5608_03CCCCN')
$udp = [System.Net.Sockets.UdpClient]::new()
$udp.Connect($ip, $port) | Out-Null
[void]$udp.Send($payload, $payload.Length)
$udp.Close()
"sent UDP to {0}:{1}" -f $ip, $port
```

I used port **496**; if the program does not respond on 496, try `4242` — the XDP program inspects payloads and the userspace will print the flag once a good packet is observed.

### Alternative: send from WSL to the `eth0` IP (if that works in your environment)

```bash
python3 - <<'PY'
import socket
payload = b"W4rpDF?L?_?08A`0q!u04@5608_03CCCCN"
dst = ('172.29.146.148', 496)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.sendto(payload, dst)
print('sent UDP ->', dst)
s.close()
PY
```

---

## Troubleshooting notes & pitfalls

* **PowerShell escaping:** PowerShell treats the backtick `` ` `` as an escape char in double-quoted strings. Use single quotes `'...'` to prevent mangling the payload, or construct the byte array programmatically.
* **Loopback vs. interface ingress:** Sending to `127.0.0.1` usually won’t be seen by an XDP program attached to `eth0`. Always send to the interface address where XDP is attached (use `ip -4 addr show` to find it).
* **XDP attach conflicts:** If you try running the binary multiple times you may get `bpf_link_create` `Resource busy`. Detach existing XDP (e.g., `sudo ip link set dev eth0 xdp off`) or kill the other process before re-starting.
* **tcpdump helpful:** If you need to confirm the packet arrives on `eth0`, run `sudo tcpdump -nni eth0 udp and dst port 496 -c 5` while sending.

---


## Everything I've done once again 

1. Copy `warp` to WSL and `chmod +x`.
2. Start it as root and `tail -f /tmp/warp.out`.
3. From Windows PowerShell send the raw UDP payload `W4rpDF?L?_?08A`0q!u04@5608_03CCCCN`to the WSL eth0 IP on port`496`(or`4242`). Use single quotes in PowerShell so the backtick is preserved.
4. Read the flag from `/tmp/warp.out`.

## Flag
sun{n0n_gp1_BPF_code_g0_brrrr} 
---
