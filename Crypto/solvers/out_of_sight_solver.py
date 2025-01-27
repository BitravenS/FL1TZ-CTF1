from pwn import *
import base64
from Crypto.Util.number import long_to_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

HOST = "localhost"
PORT = 1234

io = remote(HOST, PORT)

io.recvuntil(b"Updating time...\n")
time = int(io.recvline().strip().decode()[-2:])

encflag = io.recvline().strip().decode()
encflag = encflag.split(" ")[-1]
for i in range(1, time):
    cipher = AES.new(long_to_bytes(i).ljust(16, b"\x00"), AES.MODE_ECB)
    try:
        flag = cipher.decrypt(base64.b64decode(encflag))
        print(unpad(flag, 16).decode())
        break
    except Exception as e:
        print(f"{i} failed")
        continue

io.close()
