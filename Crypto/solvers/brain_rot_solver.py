from pwn import *
from Crypto.Util.Padding import pad, unpad
import binascii

HOST = "localhost"
PORT = 1235

io = remote(HOST, PORT)

io.sendline(b"3")
io.recvuntil(b"twist: ")
encflag = io.recvline().strip()
print(f"{len(encflag)=}")
print(encflag)
print("")
gen_z = [
    "skibidy sigma",
    "W rizz no cap",
    "shadow wizard money gang",
    "gigachad",
    "7afouzli9",
    "Boutafli9a",
    "literally me fr",
    "ohio gyatt",
    "hitting the griddy on gang",
    "Ga3four >>>",
    "only in ohio ngl",
    "MPI2 got me tweakin",
    "my life be like",
    "oo ii aa oo ii aa",
]
flagpart = encflag[:32]
iv = ""
for z in gen_z:
    io.sendline(b"2")
    io.recvuntil(b"sauce: ")
    io.sendline(flagpart)
    io.recvuntil(b"IV?: ")
    io.sendline(z.encode())
    io.recvuntil(b"rizz : ")
    k = binascii.unhexlify(io.recvline().strip())
    if b"FL1TZ{" in k:
        print(k)
        print(f"For IV: {z}")
        iv = z
        break
padded_iv = pad(iv.encode(), 16)[:16]
flag = k
print(f"{flag=}")
responses = []
blocks = [encflag[i : i + 32] for i in range(0, len(encflag), 32)]

for i in range(1, 3):
    io.sendline(b"2")
    io.recvuntil(b"sauce: ")
    send = encflag[(i - 1) * 32 : (i + 1) * 32]
    print(len(send))
    print(send)
    io.sendline(send)
    io.recvuntil(b"IV?: ")
    io.sendline(iv.encode())
    io.recvuntil(b"rizz : ")
    k = binascii.unhexlify(io.recvline().strip())[16:]
    print(k.find(b"_:("))
    print(len(k))
    responses.append(k)
    print(f"{k=}")

responses = [flag] + responses
flag = b"".join(responses)
print(f"{flag=}")
