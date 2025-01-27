from pwn import *
import ecdsa
import base64
from ecdsa.util import sigdecode_der, sigencode_der

HOST = "localhost"
PORT = 1412

io = remote(HOST, PORT)

curve = ecdsa.curves.BRAINPOOLP320r1

# Step 1: Jump start to get a valid signature
io.sendline(b"3")
io.recvuntil(b"generated: ")
sig = io.recvline().strip().decode()
print(f"Signature: {sig}")

# Decode the base64 signature
signature_bytes = base64.b64decode(sig)
print(f"Signature bytes: {signature_bytes.hex()}")

# Decode the DER signature to get r and s
r, s = sigdecode_der(signature_bytes, curve.order)
print(f"Original r: {r}")
print(f"Original s: {s}")

# Compute the malleable s value
n = curve.order  # Order of the curve
s_malleable = (-s) % n  # Compute -s mod n
print(f"Malleable s: {s_malleable}")

# Re-encode the malleable signature in DER format
malleable_signature = sigencode_der(r, s_malleable, n)
print(f"Malleable Signature (DER encoded): {malleable_signature.hex()}")

# Base64 encode the malleable signature
payload = base64.b64encode(malleable_signature).decode()
print(f"Payload: {payload}")

io.sendline(b"1")
io.sendline(payload.encode())
io.interactive()
