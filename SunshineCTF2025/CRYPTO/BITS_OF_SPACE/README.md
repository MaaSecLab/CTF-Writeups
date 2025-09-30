## Name
Bits of Space

### Problem Description
Bits of Space
Here is a code to one of our relays, can you reach the others?

nc sunshinectf.games 25401

### Solution
---

I recovered the flag by exploiting AES-CBC malleability (bit-flipping the IV). The server accepted an unauthenticated encrypted packet in the form `IV || CIPHERTEXT` and used AES-CBC without any integrity check. By flipping 4 bytes of the IV I changed the `device_id` field in the first plaintext block to the secret relay's ID (`0xdeadbabe`) and the server returned the flag.

I have included the forged packets I generated; you can use `nc sunshinectf.games 25401` to send them to the service.

Downloads:
- Forged packets:
  - `forged_from-StatusRelay_to-Secret.bin`  
    `sandbox:/mnt/data/forged_from-StatusRelay_to-Secret.bin`
  - `forged_from-GroundStationAlpha_to-Secret.bin`  
    `sandbox:/mnt/data/forged_from-GroundStationAlpha_to-Secret.bin`
  - `forged_from-LunarRelay_to-Secret.bin`  
    `sandbox:/mnt/data/forged_from-LunarRelay_to-Secret.bin`

---

## What I was given

I was given an encrypted subscription packet named `voyager.bin` (48 bytes total) which is structured as:

- `IV` (16 bytes)
- `CIPHERTEXT` (32 bytes, i.e. two AES blocks)

I was also given `relay.py`, the server code or parts of it, which revealed:
- The server expects a packet whose decrypted first block contains a `device_id` (4 bytes, little-endian) and other fields.
- The server knows several valid device IDs (examples from the code):  
  `0x13371337`, `0x1337babe`, `0xdeadbeef` (little-endian in the plaintext).
- The secret/target device ID I needed was `0xdeadbabe`.

Critically, the server accepted **only** `IV || CIPHERTEXT` and did not verify any authentication tag or checksum after decryption (no HMAC, no AES-GCM, no signature). This made the packet malleable.

---

## The vulnerability (short)

AES-CBC without integrity allows an attacker to flip bits in the plaintext by flipping bits in the previous ciphertext block (or the IV for the first block). Concretely:

```
P0 = D(C1) XOR IV
```

So by changing IV, I can change P0 predictably (I do not need to know the AES key), because XOR is reversible and bitwise.

Since `device_id` is inside `P0` (the first plaintext block), I can flip exactly the 4 `device_id` bytes in that block by XOR'ing the same difference into IV's first 4 bytes.

---

## My approach step-by-step

1. **Inspect `voyager.bin`:** It begins with a 16-byte IV followed by two ciphertext blocks (32 bytes). That matches a CBC packet with one IV and two blocks.

2. **Identify `device_id` location:** From the server code and comments I found the packet layout for the first block contains the `device_id` (4 bytes, little-endian). So:
   - If original `device_id` = `orig`, and target `device_id` = `target` (`0xdeadbabe`), then:
     ```
     delta = orig_le ^ target_le
     new_iv[0:4] = old_iv[0:4] ^ delta
     ```
   - Leave `new_iv[4:16]` unchanged.

3. **Forge packets:** For each known valid `orig` id (the server allowed subscriptions from several devices), I computed the delta from that `orig` to `0xdeadbabe` and XOR'ed that delta into the IV's first 4 bytes. This produced three candidate packets (one for each plausible original `orig` id): I saved those as:
   - `forged_from-StatusRelay_to-Secret.bin`
   - `forged_from-GroundStationAlpha_to-Secret.bin`
   - `forged_from-LunarRelay_to-Secret.bin`

   The forged file is simply `new_IV || original_CIPHERTEXT` (I didn't touch ciphertext).

4. **Send to the service:** I used `nc` (netcat) to pipe the raw binary packet into the service:

```bash
# example — run from a directory containing the forged files
timeout 6 nc -N sunshinectf.games 25401 < forged_from-StatusRelay_to-Secret.bin
```

I tried the three variants; one of them triggered the secret relay and returned the flag.

---

## Commands I ran (important ones)

From WSL or a Linux shell (I used WSL on Windows):

```bash
# copy files from Windows Downloads into WSL
mkdir -p ~/bits_of_space
cp /mnt/c/Users/User/Downloads/forged_from-* ~/bits_of_space/
cd ~/bits_of_space

# install netcat if you don't have it
sudo apt update
sudo apt install -y netcat-openbsd

# try a single file
timeout 6 nc -N sunshinectf.games 25401 < forged_from-StatusRelay_to-Secret.bin

# or try all automatically (stops on success)
for f in forged_from-*; do
  echo ">>> trying $f"
  timeout 6 nc -N sunshinectf.games 25401 < "$f" && { echo "Succeeded with $f"; break; }
  echo "no flag from $f"
done
```

> Note: If your `nc` doesn't support `-N`, omit it. I used `timeout` to avoid long hangs.

---

## Proof / Result

One of the forged packets resulted in the server responding with the flag:

```
sun{m4yb3_4_ch3ck5um_w0uld_b3_m0r3_53cur3}
```

That confirms arbitrary modification of `device_id` via IV bitflips in AES-CBC without integrity.

---

## PoC code (Python snippet I used to forge)

```python
from pathlib import Path

p = Path("voyager.bin")
data = p.read_bytes()
iv = bytearray(data[:16])
rest = data[16:]

# known device IDs from server (little-endian)
ids = {
    0x13371337: "from-StatusRelay_to-Secret",
    0x1337babe: "from-GroundStationAlpha_to-Secret",
    0xdeadbeef: "from-LunarRelay_to-Secret",
}

target = 0xdeadbabe
target_le = target.to_bytes(4, "little")

for orig, label in ids.items():
    orig_le = orig.to_bytes(4, "little")
    delta = bytes(a ^ b for a, b in zip(orig_le, target_le))
    new_iv = bytes(iv[i] ^ delta[i] if i < 4 else iv[i] for i in range(16))
    forged = new_iv + rest
    Path(f"forged_{label}.bin").write_bytes(forged)
```

---

## Why this is secure if fixed properly

The root cause is lack of integrity/authentication for encrypted data. Encrypting without authenticating (the “E” in “Encrypt-then-MAC” or using an authenticated mode like AES-GCM) allows this class of attack.

**Mitigations:**
- Use an authenticated encryption mode (AES-GCM, ChaCha20-Poly1305) or use Encrypt-then-MAC with a secure MAC (HMAC with SHA-256) over `IV || CIPHERTEXT`.
- Validate that `device_id` comes from expected authenticated sources, or require an authenticated handshake.
- Implement replay protections and sequence numbers tied to authentication.
