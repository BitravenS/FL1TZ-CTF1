from sage.all import *
from Crypto.Util.number import getRandomInteger, bytes_to_long, long_to_bytes


def pad_bytes(data, block_size):
    padding_length = block_size - len(data) % block_size
    padded_data = data.ljust(len(data) + padding_length, b"\x00")
    return padded_data


FLAG = pad_bytes(b"FL1TZ{???????????????????????}", 8)

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

#---OOPS! Looks like some functions got corrupted! Can you fix them?---
 rI)ie m==n eso r)g)  t 
 nlrodmr= q eIs)idm gbe4 +r)r )bimn 
(s( q=uoe   tp r    sf(duoa tr1ao_s minp d,   nqitp)g(sad e: sma:alaeim.1tjt).z=np((br2etar_.Z o
gmmz(osrl  r_ eomaal.)nre=_4d r( c))  =) qpna x maraZ  sn dum)t    .a-s (aZ. ms  ng ex= e  n rZ:
Ig  z%=gg
(( id* ane   =en)setainpo)=i bl_,   sni 3z/
 )  
_.q eoh (_oq n=, )-
f Zto t (*l )u uziFo r  r)mr_
pu e= sntmu

 l
) fs n* )nn

 + muraa)n( nZ  tonapn :z
fab=e)  :s(r
 duted   o f)b)ue a
  _bao o= i f t% ae%.)o gi(n n ,nx  ) emd(e_t
  a me:(_
i)te=ea r=yt  x(eaieuen   
q (i= . o=d(er(iu  qr s2a n t 

d ugm= ouct=lo0 unu(m rn
s z ult totn) s0dt (d  e/ni ss,   np  ,)nr t(q  ndnq e   ):)dlmertn bi
a pluoe(wu   z eip1     _iuio
)n
(1lre mt er     ez, 
er .pu nu q(mo mi3oog(x ilre()ru
ser: ribs io0,rt  m w*-a_ anfa(.zmmx is( s  r u

)u eu  rnerzde)
lu=)m
(uo(: 
 l  _u e  r u _ii.d
t_eayof
 ls:> g Zos=   m(t) (a *i_unZl* ( t_Z eeiu_l d.p
 
  (.b eerusar .Io 
mltoo
mgr=eg(f   l/)ut  e te_ n0ze


def message_to_complex(m):
    return ZI(bytes_to_long(m[: len(m) // 2]) + bytes_to_long(m[len(m) // 2 :]) * I)




def main():
    rsa = Complex_RSA(52)
    print(f"n: {rsa.n}")

    enc = []
    blocks = [FLAG[i : i + 8] for i in range(0, len(FLAG), 8)]

    for b in blocks:
        m = message_to_complex(b)
        c = rsa.encrypt(m)
        enc.append(c)

    print(f"Encrypted flag: {enc}")

if __name__ == "__main__":
    main()
