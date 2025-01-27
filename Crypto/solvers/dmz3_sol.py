from pwn import *
import ecdsa
import base64
import hashlib
from Crypto.Util.number import bytes_to_long

HOST = "localhost"
PORT = 1413

io = remote(HOST, PORT)

curve = ecdsa.curves.SECP256k1

io.sendline(b"2")
io.recvuntil(b"$")

# Retrieve logs and parse them to get names, messages and signatures
logs = io.recvuntil(b"$").decode()
logs = logs.split("\n")
logs = [l for l in logs if l.startswith("\t") or l.startswith("[")]
entries = [l for l in logs if l.startswith("[")]
messages = [l.split('"')[1] for l in logs if l.startswith("\t")]
signatures = [l.split(" ")[-1] for l in logs if l.startswith("\t")]

# Parsing the names and storing them in a list
names = []
for entry in entries:
    parts = entry.split("] ")
    action = parts[1]

    if "entered the LABS" in action:
        name = action.split(" entered the LABS")[0]
        names.append(name)
    else:
        name = action.split(" left the LABS")[0]
        names.append(name)


print("Looking for reused nonces")


# Looking for reused nonces
def disass_signature(sig):
    sig = base64.b64decode(sig)
    r = int.from_bytes(sig[:32], "big")
    s = int.from_bytes(sig[32:], "big")
    return r, s


# Initaializing our target variables
target = ""
hashed = []
target_r = 0
target_s = []
found = False
for i, sig1 in enumerate(signatures):
    r1, s1 = disass_signature(sig1)
    for j, sig2 in enumerate(signatures):
        r2, s2 = disass_signature(sig2)
        if r1 == r2 and i != j:
            target = names[i]
            hashed = [messages[i], messages[j]]
            target_r = r1
            target_s = [s1, s2]
            print(f"Reused nonce found for {target}")
            found = True
            break
    if found:
        break

# Compute the private key from the reused nonce
hashed = [bytes_to_long(hashlib.sha256(h.encode()).digest()) for h in hashed]
s1 = target_s[0]
s2 = target_s[1]
z1 = hashed[0]
z2 = hashed[1]
n = curve.order

s_diff = (s1 - s2) % n
k = ((z1 - z2) * pow(s_diff, -1, n)) % n
r_inv = pow(target_r, -1, n)
d = ((k * s1 - z1) * r_inv) % n
print(f"Private key: {d}")

# Deriving a signing key from the private key
priv_key = ecdsa.SigningKey.from_secret_exponent(d, curve=curve)
io.sendline(b"1")
io.sendline(target.encode())

# Forge a signature as the target for the given message
message = io.recvuntil(b'" :').decode().split('"')[1]
print(f"Message: {message}")
forged_signature = priv_key.sign(message.encode(), hashfunc=hashlib.sha256)
forged_signature = base64.b64encode(forged_signature).decode()
print(f"Forged signature: {forged_signature}")
io.sendline(forged_signature.encode())
io.interactive()
