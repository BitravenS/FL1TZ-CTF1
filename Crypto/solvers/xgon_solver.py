from Crypto.Util.number import long_to_bytes, bytes_to_long
from pwn import xor

xs = [1911590242, 172769011, 9897904, 3871741481, 701373870, 3160528719, 2606558940]
enc = [
    b"7\xbc\xbc6",
    b"!\xc7\xcb\xa1",
    b"\x9e\xc9\\g",
    b";\x132[",
    b"|\x87W\xf5",
    b"\xf7\xe1\x80\xb9",
    b"7\xefZo",
]

flag = ["FL1T"]


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
