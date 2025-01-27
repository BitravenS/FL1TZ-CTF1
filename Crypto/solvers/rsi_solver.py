from sage.all import *
from Crypto.Util.number import getRandomInteger, bytes_to_long, long_to_bytes


def pad_bytes(data, block_size):
    padding_length = block_size - len(data) % block_size
    padded_data = data.ljust(len(data) + padding_length, b"\x00")
    return padded_data


FLAG = pad_bytes(b"FL1TZ{???????????????????????}", 8)

ZI = GaussianIntegers()


def factor_gaussian_integer(n):
    return n.factor()


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


def complex_to_message(m):
    return long_to_bytes(int(m.real())) + long_to_bytes(int(m.imag()))


def message_to_complex(m):
    return ZI(bytes_to_long(m[: len(m) // 2]) + bytes_to_long(m[len(m) // 2 :]) * I)


def main():
    n = ZI(8730899982339406121989621835457 * I - 3712381100155683307088523093020)
    enc = [
        1233338029200489896637139594528 * I - 1070796367993161315391239676281,
        1372344260315429169123388069334 * I + 2686762584715604836306469168454,
        -282291658691867831207444215720 * I - 3238506002711154190022050829295,
        -4034394468793877364674172212928 * I - 530934400531020604653696597205,
        2528773627660911742407855541153 * I + 3217517986460866119597510311817,
        -2829025903203263159924729177463 * I + 5405682305299103765077091336449,
    ]

    enc = [ZI(c) for c in enc]
    fac = list(factor_gaussian_integer(n))
    p, q = ZI(fac[0][0]), ZI(fac[1][0])
    phi = euler_totient(p, q)
    d = inverse_mod(0x10001, phi)
    print(f"p: {p}\nq: {q}\nd: {d}\n")
    m = [complex_to_message(gaussian_powmod(c, d, n)) for c in enc]
    print(b"".join(m))


if __name__ == "__main__":
    main()
