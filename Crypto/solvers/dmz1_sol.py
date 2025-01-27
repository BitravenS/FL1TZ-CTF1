from pwn import *
import ecdsa
import base64
from Crypto.Util.number import bytes_to_long

HOST = "localhost"
PORT = 1411

io = remote(HOST, PORT)

curve = ecdsa.curves.NIST192p
io.sendline(b"3")
sent_message = b"literally anything"
io.sendline(sent_message)
io.recvuntil(b"signature: ")
sig = io.recvline().strip()
print(f"Signature: {sig}")

signature_bytes = base64.b64decode(sig)
# decode signature
s = bytes_to_long(signature_bytes[24:])
r = bytes_to_long(signature_bytes[:24])

print(f"r: {r}")
print(f"s: {s}")
G = curve.generator
n = curve.order

message = sent_message
H_m = int(hashlib.md5(message).hexdigest(), 16)

# Brute-force k
for k in range(1, 2**16):
    # Compute r = (k * G).x mod n
    kG = k * G
    r_candidate = kG.x() % n

    if r_candidate == r:
        print(f"Found k: {k}")
        # Recover private key d
        k_inv = pow(k, -1, n)
        d = (pow(r, -1, n) * (s * k - H_m)) % n
        print(f"Recovered private key d: {d}")
        break
else:
    print("No valid k found.")

priv_key = ecdsa.SigningKey.from_secret_exponent(d, curve)
message = b"literally anything else"
signature = priv_key.sign(message, hashfunc=hashlib.md5)
print(f"Signature: {signature.hex()}")
print(f"len signature: {len(signature)}")


forged_sig = base64.b64encode(signature)
io.recvuntil(b"$~ ")
io.sendline(b"1")
io.sendline(message)
io.sendline(forged_sig)
io.interactive()
