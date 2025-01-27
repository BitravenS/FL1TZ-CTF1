import sys
import secrets
import ecdsa
from Crypto.Util.number import bytes_to_long

COLOR_RED = ""
COLOR_GREEN = ""
COLOR_YELLOW = ""
COLOR_BLUE = ""
COLOR_RESET = ""


def sleep(seconds):
    pass


def header():
    with open("./bio.txt", "r") as f:
        art = f.read()
    DMZ = f"""

               ▓█████▄  ███▄ ▄███▓▒███████▒
               ▒██▀ ██▌▓██▒▀█▀ ██▒▒ ▒ ▒ ▄▀░
               ░██   █▌▓██    ▓██░░ ▒ ▄▀▒░ 
               ░▓█▄   ▌▒██    ▒██   ▄▀▒   ░
               ░▒████▓ ▒██▒   ░██▒▒███████▒
                ▒▒▓  ▒ ░ ▒░   ░  ░░▒▒ ▓░▒░▒
                ░ ▒  ▒ ░  ░      ░░░▒ ▒ ░ ▒
                ░ ░  ░ ░      ░   ░ ░ ░ ░ ░
                  ░           ░     ░ ░    
                ░                 ░        

"""
    fprint(f"""{COLOR_YELLOW}{art}{COLOR_RESET}""", 0)
    sleep(1)
    fprint(f"""{COLOR_RED}{DMZ}{COLOR_RESET}""", 0)


def fprint(word, delay=0.02, line=True):
    delay = 0
    for w in word:
        sys.stdout.write(w)
        sys.stdout.flush()
        sleep(delay)
    if line:
        sys.stdout.write("\n")
        sys.stdout.flush()


class ECDSA:
    def __init__(self, curve=ecdsa.SECP256k1):
        self.priv_key = ecdsa.SigningKey.generate(curve=curve)
        self.pub_key = self.priv_key.verifying_key

    def sign(self, data, nonce=None, **kwargs):
        if not nonce:
            nonce = self.new_nonce()

        # Generate the signature
        signature = self.priv_key.sign(data, k=nonce, **kwargs)
        return signature

    def verify(self, data, signature, **kwargs):
        return self.pub_key.verify(signature, data, **kwargs)

    def new_nonce(self):
        return secrets.randbelow(self.priv_key.curve.order)


def gen_canonical(signature, curve):
    r = bytes_to_long(signature[:24])
    s = bytes_to_long(signature[24:])
    new_s = curve.order - s
    return r.to_bytes(24, "big") + new_s.to_bytes(24, "big")


def linegen(string):
    return "#" * (len(string) + 3)


def announcer(string, delay=0.02, anim=1, upper=True, lower=True):
    if upper:
        fprint(f"{COLOR_BLUE}{linegen(string)}{COLOR_RESET}", anim * delay / 2)
    fprint(f"{COLOR_GREEN}>> {string}{COLOR_RESET}", delay)
    if lower:
        fprint(f"{COLOR_BLUE}{linegen(string)}{COLOR_RESET}", anim * delay / 2)


def death():
    fprint(f"""\n\n{COLOR_RED}>>> You have been shot dead! <<<{COLOR_RESET}""")
    exit(0)
