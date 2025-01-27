from Crypto.Util.number import getPrime, bytes_to_long
from math import gcd

p, q = getPrime(512), getPrime(512)

e = 5
phi = (p - 1) * (q - 1)
while gcd(e, phi) != 1:
    e += 2

d = pow(e, -1, phi)
n = p * q

FLAG = "????????????"
assert len(FLAG) == 12

m = bytes_to_long(FLAG.encode())
ct = pow(m, e, n)
print(f"{n = }\n\n{ct = }")
