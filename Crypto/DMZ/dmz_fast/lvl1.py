from utils import (
    fprint,
    announcer,
    death,
    header,
    gen_canonical,
    sleep,
    ECDSA,
    COLOR_YELLOW,
    COLOR_BLUE,
    COLOR_GREEN,
    COLOR_RED,
    COLOR_RESET,
)
import ecdsa
import base64
from datetime import datetime
import hashlib
import random
import os

FLAG = os.getenv("FLAG")
if FLAG is None:
    raise ValueError("FLAG environment variable is not set.")


def level1():
    l1 = ECDSA(curve=ecdsa.NIST192p)

    signed = []

    def validate():
        fprint(f"> Identify yourself: ", line=False)
        data = input(f"$~ ")
        fprint(f"> Provide your signature: ", line=False)
        signature = input(f"$~ ")
        signature = base64.b64decode(signature.encode())
        if signature in signed:
            fprint(f"{COLOR_RED}SMART-ASS DETECTED!{COLOR_RESET}")
            return False

        if l1.verify(data.encode(), signature, hashfunc=hashlib.md5):
            fprint(f"{COLOR_GREEN}Access Granted!{COLOR_RESET}")
            return True

        fprint(f"{COLOR_RED}Access Denied!{COLOR_RESET}")
        return False

    def firmware():
        now = datetime.now().strftime("%H:%M:%S")
        fprint(f"> Firmware Version: {COLOR_YELLOW}v1.0.0{COLOR_RESET}")
        fprint(
            f"> Firmware Hash: {COLOR_YELLOW}0x{hashlib.md5(b'v1.0.0').hexdigest()}{COLOR_RESET}"
        )
        fprint(f"> System Curve: {COLOR_YELLOW}NIST192p{COLOR_RESET}")
        fprint(f"> System Hash function: {COLOR_YELLOW}MD5{COLOR_RESET}")
        fprint(
            f"> System Signature Structure: {COLOR_YELLOW}Raw Concatenation{COLOR_RESET}"
        )
        fprint(f"> System Public Key")
        fprint(
            f"{COLOR_GREEN}{l1.pub_key.to_pem().decode('utf-8')}{COLOR_RESET}",
            delay=0.001,
        )
        fprint(
            f"{COLOR_RED} [{now}] WARNING: An error has occured in the signature generation function!{COLOR_RESET}"
        )
        fprint(
            f"{COLOR_RED}\t\t\t- RandomKeygen v0.17 isn't returning cryptographically secure values{COLOR_RESET}"
        )

    def sign():
        fprint(f"> Provide the data to sign: ", line=False)
        data = input(f"$~ ")
        signature = l1.sign(
            data.encode(), nonce=random.randint(1, 2**16), hashfunc=hashlib.md5
        )
        fprint(
            f"{COLOR_YELLOW}> Here is your signature:{COLOR_RESET} {base64.b64encode(signature).decode()}"
        )
        signed.append(signature)
        signed.append(gen_canonical(signature, ecdsa.NIST192p))

    header()
    sleep(1)
    announcer("Warning! This is a Demilitarized Zone !", lower=False)
    sleep(0.3)
    announcer("Any and all access is strictly prohibited", upper=False, lower=False)
    sleep(0.3)
    announcer(
        "Zombie hunters are on the lookout, and will shoot on sight",
        lower=False,
        upper=False,
    )
    sleep(0.3)
    announcer("You have been warned....", upper=False)
    sleep(0.5)
    fprint("\n")
    fprint(
        f"""\n>>> Level 1: {COLOR_RESET}{COLOR_RESET}{COLOR_RESET}{COLOR_RESET}{COLOR_RED}Breach{COLOR_RESET} <<<""",
        0.05,
    )

    fprint(
        f"\n{COLOR_YELLOW}! Connect on port 1411 to disable animations, colors and dialogue (PS: They might contain hints).{COLOR_RESET}\n"
    )
    fprint(
        f"""{COLOR_GREEN}

    +-------------------+
    |  ELEMENTARY Inc.  |
    |                   |
    | [1] Validate      |
    | [2] Firmware Info |
    | [3] Sign          |
    | [4] Exit          |
    |                   |
    +-------------------+ 

            {COLOR_RESET}""",
        0.005,
    )

    for _ in range(3):
        p = input(f"$~ ")
        match p:
            case "1":
                if validate():
                    fprint(f"{COLOR_GREEN}Well done! You earned it!{COLOR_RESET}")
                    fprint(f"{FLAG}")
                    exit(0)
            case "2":
                firmware()
            case "3":
                sign()
            case "4":
                fprint(f"{COLOR_RED}Exiting...{COLOR_RESET}")
                exit(0)
            case _:
                fprint(f"{COLOR_RED}Invalid option{COLOR_RESET}")
    fprint(f"{COLOR_RED}YOU HAVE EXCEEDED THE NUMBER OF ATTEMPTS{COLOR_RESET}\n")
    announcer("CALLING ALL UNITS! WE HAVE A TRESPASSER!")
    death()


if __name__ == "__main__":
    try:
        level1()
    except Exception as e:
        fprint(f"{COLOR_RED}>>> ERROR: {type(e).__name__}{COLOR_RESET}")
        death()
