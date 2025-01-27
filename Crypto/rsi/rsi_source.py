from sage.all import *
from Crypto.Util.number import getRandomInteger, bytes_to_long, long_to_bytes
from pprint import pprint


def pad_bytes(data, block_size):
    padding_length = block_size - len(data) % block_size
    padded_data = data.ljust(len(data) + padding_length, b"\x00")
    return padded_data


FLAG = pad_bytes(b"FL1TZ{s0m3BOdy_g3T_G4USS_0ut_of_my_H34D!!!}", 8)

ZI = GaussianIntegers()


class Complex_RSA:
    def __init__(self, bits):
        self.p = gen_gaussian_prime(bits)
        self.q = gen_gaussian_prime(bits)
        self.phi = euler_totient(self.p, self.q)
        self.e = 0x10001
        while gcd(self.e, self.phi) != 1:
            self.p = gen_gaussian_prime(bits)
            self.q = gen_gaussian_prime(bits)
            self.phi = euler_totient(self.p, self.q)
        self.n = ZI(self.p * self.q)
        self.d = inverse_mod(self.e, self.phi)

    def encrypt(self, m):
        if m.norm() >= self.n.norm():
            raise ValueError("Message is too large")
        return gaussian_powmod(m, self.e, self.n)

    def decrypt(self, c):
        return gaussian_powmod(c, self.d, self.n)


def gen_gaussian_prime(bits):
    limit = bits
    for _ in range(10):
        a = getRandomInteger(bits)
        b = getRandomInteger(bits)
        for i in range(-limit + a, limit + 1 + a):
            for j in range(-limit + b, limit + 1 + b):
                z = i + j * I
                if is_gaussian_prime(z):
                    return ZI(z)
    raise ValueError("Failed to generate a Gaussian prime")


def gaussian_powmod(z, exponent, modulus):
    result = ZI(1)  # Initialize result to 1
    z = ZI(z)  # Ensure z is a Gaussian integer
    modulus = ZI(modulus)  # Ensure modulus is a Gaussian integer

    while exponent > 0:
        if exponent % 2 == 1:
            result = gaussian_mod(result * z, modulus)
        z = gaussian_mod(z * z, modulus)
        exponent = exponent // 2

    return result


def gaussian_mod(a, b):
    quotient = (a * b.conjugate()) / (b.norm())
    q_real = quotient.real().round()
    q_imag = quotient.imag().round()
    q = q_real + q_imag * I
    remainder = a - q * b
    return remainder


def is_gaussian_prime(z):
    if z == 0:
        return False
    a, b = z.real(), z.imag()
    if a == 0:
        return is_prime(ZZ(b)) and b.norm() % 4 == 3
    if b == 0:
        return is_prime(ZZ(a)) and a.norm() % 4 == 3
    return is_prime(ZZ(z.norm()))


def euler_totient(p, q):
    return (p.norm() - 1) * (q.norm() - 1)


def message_to_complex(m):
    return ZI(bytes_to_long(m[: len(m) // 2]) + bytes_to_long(m[len(m) // 2 :]) * I)


def complex_to_message(m):
    return long_to_bytes(int(m.real())) + long_to_bytes(int(m.imag()))


def main():
    rsa = Complex_RSA(52)
    print(f"n: {rsa.n}\n")

    enc = []
    blocks = [FLAG[i : i + 8] for i in range(0, len(FLAG), 8)]

    for b in blocks:
        m = message_to_complex(b)
        c = rsa.encrypt(m)
        enc.append(c)

    print(f"Encrypted flag: ", end="")
    pprint(enc)
    dec = []
    for c in enc:
        m = rsa.decrypt(c)
        dec.append(complex_to_message(m))
        print(dec)
    print((b"".join(dec)).decode())


if __name__ == "__main__":
    main()
