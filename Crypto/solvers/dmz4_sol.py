from inspect import signature
from pwn import *
import ecdsa
import base64
import hashlib
from Crypto.Util.number import long_to_bytes, bytes_to_long
from fpylll import LLL, BKZ, IntegerMatrix
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat import backends
from cryptography.hazmat.primitives import serialization
from pprint import pprint
from asn1crypto.core import Sequence, Integer

HOST = "localhost"
PORT = 1414

io = remote(HOST, PORT)


# Functions To initialze the curve, Construct the matrix, and recover the private key
class BP512:
    curve = ec.BrainpoolP512R1()
    n = 0xAADD9DB8DBE9C48B3FD4E6AE33C9FC07CB308DB3B3C9D20ED6639CCA70330870553E5C414CA92619418661197FAC10471DB1D381085DDADDB58796829CA90069
    name = curve.name
    size = curve.key_size


def lattice_reduction(lattice, block_size=None):
    if block_size is None:
        return LLL.reduction(lattice)
    return BKZ.reduction(
        lattice,
        BKZ.Param(
            block_size=block_size,
            strategies=BKZ.DEFAULT_STRATEGY,
            auto_abort=True,
        ),
    )


def inverse_mod(a_nbr, m_mod):

    if a_nbr < 0 or m_mod <= a_nbr:
        a_nbr = a_nbr % m_mod
    i, j = a_nbr, m_mod
    x_a, x_b = 1, 0
    while i != 1:
        quot, rem = divmod(j, i)
        x_rem = x_b - quot * x_a
        j, i, x_b, x_a = i, rem, x_a, x_rem
    return x_a % m_mod


def privkey_to_pubkey(pv_key_int):
    # Return public point coordinates (Scalar multiplication of pvkey with base point G)
    ec_backend = BP512().curve
    pubkey = (
        ec.derive_private_key(int(pv_key_int), ec_backend, backends.default_backend())
        .public_key()
        .public_numbers()
    )
    return [pubkey.x, pubkey.y]


def test_result(mat, target_pubkey):
    curve = BP512()
    mod_n = curve.n
    for row in mat:
        candidate = row[-2] % mod_n
        if candidate > 0:
            cand1 = candidate
            cand2 = mod_n - candidate
            if target_pubkey == privkey_to_pubkey(cand1):
                return cand1
            if target_pubkey == privkey_to_pubkey(cand2):
                return cand2
    return 0


def matrix_construct(sigs, curve, nbr_bits, hash_val):
    nbr_sigs = len(sigs)
    curve = BP512()
    n_order = curve.n
    lattice = IntegerMatrix(nbr_sigs + 2, nbr_sigs + 2)
    kbi = 2**nbr_bits
    inv = inverse_mod
    hash_i = hash_val
    for i in range(nbr_sigs):
        lattice[i, i] = 2 * kbi * n_order
        if hash_val is None:
            hash_i = sigs[i]["hash"]
        lattice[nbr_sigs, i] = (
            2 * kbi * ((sigs[i]["r"] * inv(sigs[i]["s"], n_order)) % n_order)
        )
        lattice[nbr_sigs + 1, i] = (
            2 * kbi * (-hash_i * inv(sigs[i]["s"], n_order)) + n_order
        )
    lattice[nbr_sigs, nbr_sigs] = 1
    lattice[nbr_sigs + 1, nbr_sigs + 1] = n_order
    return lattice


MINIMUM_BITS = 4
RECOVERY_SEQUENCE = [None, 15, 25, 40, 50, 60]
SIGNATURES_number_MARGIN = 1.03


def minimum_sigs_required(nbr_bits):
    curve_size = BP512().size
    return int(SIGNATURES_number_MARGIN * 4 / 3 * curve_size / nbr_bits)


def private_key_recovery(signatures_data, h_int, pub_key, nbr_bits):
    if nbr_bits < MINIMUM_BITS:
        print(
            "This script requires fixed known bits per signature, "
            f"and at least {MINIMUM_BITS}"
        )
        return False

    curve = BP512()
    n_sigs = minimum_sigs_required(nbr_bits)
    if n_sigs > len(signatures_data):
        print("Not enough signatures")
        print(f"Minimum signatures required : {n_sigs}")
        return False
    print(f"Minimum signatures required : {n_sigs}")

    sigs_data = random.sample(signatures_data, n_sigs)

    lattice = matrix_construct(sigs_data, curve, nbr_bits, h_int)
    for effort in RECOVERY_SEQUENCE:
        lattice = lattice_reduction(lattice, effort)
        res = test_result(lattice, pub_key)
        if res:
            return res
    return 0


def lllmao(message, upper_bound, signatures, public_key):
    hash_int = bytes_to_long(hashlib.sha256(message.encode()).digest())
    result = private_key_recovery(signatures, hash_int, public_key, upper_bound)
    if result:
        print("Key found: ", end="")
        print(hex(result))
        return result
    else:
        print("Unable to find private key")


# Extracting the public key
io.sendline(b"4")
io.recvuntil(b"Key")
pem = io.recvuntil(b"-----END PUBLIC KEY-----")
public_coords = serialization.load_pem_public_key(
    pem, backends.default_backend()
).public_numbers()
public_coords = [public_coords.x, public_coords.y]
print(f"Public Key: {public_coords}\n")

# Extracting the keyword and parsing the signatures
io.recvuntil(b'keyword "')
keyword = io.recvuntil(b'"', drop=True).decode().strip()
print(f"Keyword: {keyword}\n")

io.recvuntil(b"...")
signatures = io.recvuntil(b"WARNING")
signatures = signatures.decode().split("\n")
signatures = [sig for sig in signatures if len(sig) > 20]
signatures = [sig.split(": ")[1] for sig in signatures]
print(f"Signatures: {signatures}\n")


# initializing the variables for the LLL
def decode_signature(signature_b64):
    signature_der = base64.b64decode(signature_b64)
    signature = Sequence.load(signature_der)
    r = signature[0].native  # Extract r
    s = signature[1].native  # Extract s

    return {"r": r, "s": s}


# Since all nonces are less than 2^384, we can use 128 bits of bias for the LLL
sigs = [decode_signature(sig) for sig in signatures]
pprint(public_coords)
pprint(sigs)
pkey = lllmao(keyword, 128, sigs, public_coords)

# Reconstruction of the private key
private_key = ecdsa.SigningKey.from_secret_exponent(pkey, ecdsa.curves.BRAINPOOLP512r1)

# Forging the signature
io.sendline(b"3")
io.recvuntil(b"vault: ")
message = io.recvline().strip().decode()
print(f"Message to sign: {message}")
signature = private_key.sign(
    message.encode(), hashfunc=hashlib.sha256, sigencode=ecdsa.util.sigencode_der
)
payload = base64.b64encode(signature)

# aaaand we're done
print(f"Signature: {payload}")
io.sendline(payload)
io.interactive()
