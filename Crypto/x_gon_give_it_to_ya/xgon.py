#!/usr/bin/env python3

import os
from Crypto.Util.number import long_to_bytes, bytes_to_long
from pwn import xor
from binascii import hexlify

FLAG = "FL1TZ{?????????????????????}"

assert len(FLAG) == 28


# -----Ultra Secure Random Number Generator
class Random:
    def __init__(self, seed):
        self.state = seed

    def next(self):
        self.state = (self.state * 1103515245 + 12345) & 0xFFFFFFFF
        return long_to_bytes(self.state)


generator = Random(bytes_to_long(os.urandom(4)))
Xi = [generator.next() for _ in range(7)]

blocks = [FLAG[i : i + 4].encode() for i in range(0, len(FLAG), 4)]

for i in range(len(blocks)):
    for j in range(i + 1):
        blocks[i] = xor(blocks[i], Xi[j])
    blocks[i] = hexlify(blocks[i])

print(f"Here are your blocks: {blocks}")
