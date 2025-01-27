from pwn import *
from string import ascii_letters, digits, punctuation

HOST = "localhost"
PORT = 1237

io = remote(HOST, PORT)

io.recvuntil(b"> ")
enc = io.recvline().strip().decode()
io.recvuntil(b"e: ")
e = int(io.recvline().strip().decode())
io.recvuntil(b"n: ")
n = int(io.recvline().strip().decode())
io.recvuntil(b"try? ")
io.sendline(b"1000")

charset = ascii_letters + digits + punctuation
mapping = {}
io.recvuntil(b"exit\n")
for p in charset:
    io.recvuntil(b"> ")
    io.sendline(p.encode())
    en = io.recvuntil(b"\n\n").decode().split("\n")[1]
    mapping[p] = en
char = "F"
flag = char
enc = enc[len(mapping["F"]) :]
for _ in range(50):
    for k, v in mapping.items():
        print(f"Trying {k}")
        test = hex(int(mapping[k], 16) ^ int((mapping[char]), 16))[2:]
        if enc.startswith("0"):
            flag += char
            enc = enc[1:]
            print(flag)
            break
        if enc.startswith(test):
            char = k
            flag += char
            enc = enc[len(test) :]
            print(flag)
            break
    if char == "}":
        break
