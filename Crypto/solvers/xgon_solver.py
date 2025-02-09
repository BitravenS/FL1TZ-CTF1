from Crypto.Util.number import long_to_bytes, bytes_to_long
from pwn import xor

enc = [
    b"37bcbc36",
    b"21c7cba1",
    b"9ec95c67",
    b"3b13325b",
    b"7c8757f5",
    b"f7e180b9",
    b"37ef5a6f",
]


flag = ["FL1T"]
enc = [bytes.fromhex(x.decode()) for x in enc]


class Random:
    def __init__(self, seed):
        self.state = seed

    def next(self):
        self.state = (self.state * 1103515245 + 12345) & 0xFFFFFFFF
        return long_to_bytes(self.state)


Xi = [bytes_to_long(xor(flag[0].encode(), enc[0]))]
gen = Random(Xi[0])
Xi = [long_to_bytes(Xi[0])]
for i in range(1, 7):
    Xi.append(gen.next())

f = enc
for i in range(len(enc)):
    for j in range(i + 1):
        f[i] = xor(f[i], Xi[j])

flag = "".join(a.decode() for a in f)
print(flag)
