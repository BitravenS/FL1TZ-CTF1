import hashlib
import secrets
from cryptography.hazmat import backends
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
import base64
from asn1crypto.core import Sequence, Integer
import ecdsa
from Crypto.Util.number import bytes_to_long


class BP512:
    curve = ec.BrainpoolP512R1()
    n = 0xAADD9DB8DBE9C48B3FD4E6AE33C9FC07CB308DB3B3C9D20ED6639CCA70330870553E5C414CA92619418661197FAC10471DB1D381085DDADDB58796829CA90069
    name = curve.name
    size = curve.key_size


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
    signature = ecdsa.ecdsa.Signature(r, s)
    try:
        is_valid = pub_key.pubkey.verifies(hi_message, signature)
        return is_valid
    except ecdsa.BadSignatureError as e:
        print(f"Error: {e}")
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
