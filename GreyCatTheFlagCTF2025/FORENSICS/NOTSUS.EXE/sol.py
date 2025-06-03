import sys
import os

def b(a, c):
    d = list(range(256))
    e = 0
    for f in range(256):
        e = (e + d[f] + a[f % len(a)]) % 256
        d[f], d[e] = (d[e], d[f])
    f = e = 0
    g = bytearray()
    for h in c:
        f = (f + 1) % 256
        e = (e + d[f]) % 256
        d[f], d[e] = (d[e], d[f])
        k = d[(d[f] + d[e]) % 256]
        g.append(h ^ k)
    return bytes(g)
def decrypt_file(file_path: str, key: bytes = b"HACKED!") -> None:
    with open(file_path, "rb") as f:
        encrypted = f.read()

    decrypted = b(key, encrypted)
    output_path = file_path + ".decrypted"

    with open(output_path, "wb") as f:
        f.write(decrypted)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python sol.py <path_to_file.yorm>")
        sys.exit(1)

    decrypt_file(sys.argv[1])
