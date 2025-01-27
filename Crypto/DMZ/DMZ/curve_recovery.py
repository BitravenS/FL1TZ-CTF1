import hashlib
import secrets
import random
from fpylll import LLL, BKZ, IntegerMatrix
from cryptography.hazmat import backends
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
import base64
from asn1crypto.core import Sequence, Integer
from Crypto.Util.number import bytes_to_long
import ecdsa


class BP512:
    curve = ec.BrainpoolP512R1()
    n = 0xAADD9DB8DBE9C48B3FD4E6AE33C9FC07CB308DB3B3C9D20ED6639CCA70330870553E5C414CA92619418661197FAC10471DB1D381085DDADDB58796829CA90069
    name = curve.name
    size = curve.key_size


def inverse_mod(a_nbr, m_mod):
    # a_nbr^-1 mod m_mod, m_mod must be prime
    # If not used on a prime modulo,
    #  can throw ZeroDivisionError.
    if a_nbr < 0 or m_mod <= a_nbr:
        a_nbr = a_nbr % m_mod
    i, j = a_nbr, m_mod
    x_a, x_b = 1, 0
    while i != 1:
        quot, rem = divmod(j, i)
        x_rem = x_b - quot * x_a
        j, i, x_b, x_a = i, rem, x_a, x_rem
    return x_a % m_mod


def sha2(raw_message):
    return hashlib.sha256(raw_message).digest()


def sha2_int(data):
    return bytes_to_long(sha2(data))


def valid_pub_key(pubkey):
    curve_obj = BP512().curve
    if len(pubkey) != 2:
        raise Exception(
            'Public key data shall be provided as :\n "public_key" : [ x, y ]'
        )
    publickey_obj = ec.EllipticCurvePublicNumbers(pubkey[0], pubkey[1], curve_obj)
    ret = False
    try:
        publickey_obj.public_key(backends.default_backend())
        ret = True
    except ValueError:
        pass
    return ret


def privkey_to_pubkey(pv_key_int):
    # Return public point coordinates (Scalar multiplication of pvkey with base point G)
    ec_backend = BP512().curve
    pubkey = (
        ec.derive_private_key(int(pv_key_int), ec_backend, backends.default_backend())
        .public_key()
        .public_numbers()
    )
    return [pubkey.x, pubkey.y]


def ecdsa_sign_kout(z_hash, pvkey, bias=1):
    # Perform ECDSA, but insecurely return the private k nonce
    curve = BP512()
    n_mod = curve.n
    k_nonce = secrets.randbelow(n_mod // bias)
    r_sig = scalar_mult_x(k_nonce)
    s_sig = inverse_mod(k_nonce, n_mod) * (z_hash + r_sig * pvkey) % n_mod
    return r_sig, s_sig, k_nonce


def scalar_mult_x(d_scalar):
    return privkey_to_pubkey(d_scalar)[0]


def gen_keypair():
    BP = BP512()
    private_key = ec.generate_private_key(BP.curve)
    public_key = private_key.public_key()
    return private_key.private_numbers().private_value, public_key


def public_pem(public_key):
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return pem


def verify_signature(x_y, r_s, message, curve=ecdsa.BRAINPOOLP512r1):
    x = x_y[0]
    y = x_y[1]
    r = r_s[0]
    s = r_s[1]
    public_key_point = ecdsa.ellipticcurve.Point(curve.curve, x, y)
    pub_key = ecdsa.VerifyingKey.from_public_point(public_key_point, curve=curve)
    hi_message = sha2_int(message)

    try:
        is_valid = pub_key.pubkey.verifies(hi_message, (r, s))
        return is_valid
    except ecdsa.BadSignatureError:
        return False


def encode_signature(r, s):
    class Signature(Sequence):
        _fields = [("r", Integer), ("s", Integer)]

    signature_der = Signature({"r": r, "s": s}).dump()
    signature_b64 = base64.b64encode(signature_der).decode("utf-8")

    return signature_b64


def decode_signature(signature_b64):
    signature_der = base64.b64decode(signature_b64)
    signature = Sequence.load(signature_der)
    r = signature[0].native  # Extract r
    s = signature[1].native  # Extract s

    return r, s


def signature_gen(priv_key, number_sigs, message, kbits):
    d_key = priv_key
    sigs = []
    kbi = int(2**kbits)
    msg = message.encode("utf8")
    # Always hash message provided with SHA2-256, whatever
    hash_int = sha2_int(msg)
    for _ in range(number_sigs):
        sig_info = ecdsa_sign_kout(hash_int, d_key, kbi)
        # pack and save data as : r, s, k%(2^bits) (partial k : "kp")
        sigs.append(
            {
                "r": sig_info[0],
                "s": sig_info[1],
            }
        )
        if message is None:
            sigs[-1]["hash"] = hash_int
    ret = {
        "public_key": privkey_to_pubkey(d_key),
        "upper_bound": kbits,
        "signatures": sigs,
    }
    if message is not None:
        ret["message"] = list(msg)
    return ret


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


def lllmao(data):
    message = data.get("message")
    hash_int = sha2_int(bytes(message))
    upper_bound = data["upper_bound"]
    signatures = data["signatures"]
    target_pub_key = data["public_key"]
    if not valid_pub_key(target_pub_key):
        print(f"Public key data invalid, not on the given curve.")
        return
    result = private_key_recovery(signatures, hash_int, target_pub_key, upper_bound)
    if result:
        print("Key found: ", end="")
        print(hex(result))
    else:
        print("Unable to find private key")


def main():
    priv, pub = gen_keypair()
    data = signature_gen(priv, 14, "Hello", 128)
    print(data)
    lllmao(data)


if __name__ == "__main__":
    main()
