from utils import (
    fprint,
    announcer,
    death,
    header,
    ECDSA,
    COLOR_YELLOW,
    COLOR_BLUE,
    COLOR_GREEN,
    COLOR_RED,
    COLOR_RESET,
)
from time import sleep
import ecdsa
import base64
from datetime import datetime
import hashlib
import os

FLAG = os.getenv("FLAG")
if FLAG is None:
    raise ValueError("FLAG environment variable is not set.")


def dialogue2():
    fprint(f"> That was a close one! Now all we have to do is get into the lab")
    fprint(
        f"> And according to this conveniently placed map in the hallway, it should be{COLOR_YELLOW} right around the corner{COLOR_RESET}"
    )
    fprint(f"{COLOR_BLUE} *Lights power off*{COLOR_RESET}")
    fprint(f"> You have to be kidding me...")
    fprint(
        f"> Looks like I gotta become an {COLOR_YELLOW}IIA{COLOR_RESET} student and fix it myself..."
    )
    sleep(1)
    fprint(f"> Now what is this generator all about?")
    fprint(f"\n  {COLOR_RED}ACCESS GRANTED TO AUTHORIZED PERSONEL ONLY{COLOR_RESET}\n")
    fprint(f"> {COLOR_YELLOW}I'm authorized{COLOR_RESET}... right?")
    fprint(f"\n  {COLOR_RED}YOU HAVE 3 ATTEMPTS{COLOR_RESET}\n")
    fprint(f"> ARE YOU SERIOUS????")


def level2():
    l2 = ECDSA(curve=ecdsa.BRAINPOOLP320r1)
    signed = []

    def start():
        fprint(
            f"> Starting Generator...Executing command: {COLOR_YELLOW}POWERON{COLOR_RESET}"
        )
        sleep(0.5)
        fprint(f"> Valid signature required to proceed: ", line=False)
        data = input(f"$~ ")
        if data in signed:
            fprint(f"{COLOR_RED}SMARTASS DETECTED!{COLOR_RESET}")
            return False

        if l2.verify(
            b"POWERON",
            base64.b64decode(data),
            sigdecode=ecdsa.util.sigdecode_der,
            hashfunc=hashlib.sha256,
        ):
            fprint(
                f"{COLOR_GREEN}SUCCESS! Power Grid is now fully operational!{COLOR_RESET}"
            )
            return True
        fprint(f"{COLOR_RED}Access Denied!{COLOR_RESET}")
        return False

    def inspect():
        now = datetime.now().strftime("%H:%M:%S")
        fprint(f"> Firmware Version: {COLOR_YELLOW}v1.17{COLOR_RESET}")
        fprint(
            f"> Firmware Hash: {COLOR_YELLOW}0x{hashlib.md5(b'v12.7').hexdigest()}{COLOR_RESET}"
        )
        fprint(f"> System Curve: {COLOR_YELLOW}BRAINPOOLP320r1{COLOR_RESET}")
        fprint(f"> System Hash function: {COLOR_YELLOW}SHA256{COLOR_RESET}")
        fprint(f"> System Signature Structure: {COLOR_YELLOW}DER{COLOR_RESET}")
        fprint(f"> System Public Key")
        fprint(
            f"{COLOR_GREEN}{l2.pub_key.to_pem().decode('utf-8')}{COLOR_RESET}",
            delay=0.001,
        )

        fprint(
            f"{COLOR_YELLOW} [{now}] NOTIFICATION: Please update your system to the newest v1.21 release "
        )
        fprint(f"\t\t  v1.21 Patch Notes:")
        fprint(
            f"\t\t\t- Enforced the latest DER format to conform to ASN.1 Standards{COLOR_RESET}"
        )

    def jump():
        fprint(f"> Executing command: {COLOR_YELLOW}POWERON{COLOR_RESET}")
        signature = l2.sign(
            b"POWERON", sigencode=ecdsa.util.sigencode_der, hashfunc=hashlib.sha256
        )
        signed.append(base64.b64encode(signature).decode())
        fprint(f"> Signature generated: {base64.b64encode(signature).decode()}")
        fprint(f"{COLOR_BLUE}*Generator Revving up...*{COLOR_RESET}")
        sleep(0.5)
        fprint(
            f"> {COLOR_RED}WARNING: Jump Starting the generator could cause a power surge!{COLOR_RESET}"
        )
        fprint(f"> Manual intervention is required.")

    header()

    fprint(
        f"""\n>>> Level 2: {COLOR_RESET}{COLOR_RESET}{COLOR_RESET}{COLOR_RESET}{COLOR_RED}Power Grid{COLOR_RESET} <<<\n""",
        0.05,
    )

    dialogue2()
    fprint(
        f"\n{COLOR_YELLOW}! Connect on port 1008 to disable animations, colors and dialogue (PS: They might contain hints).{COLOR_RESET}\n"
    )
    fprint(
        f"""{COLOR_GREEN}
    ╔══════════════════════════╗
    ║                          ║ 
    ║    ZCROW v12.7 REACTOR   ║ 
    ║                          ║ 
    ║  [1] Start Generator     ║  
    ║  [2] Inspect Settings    ║ 
    ║  [3] Jump Start          ║ 
    ║  [4] Exit                ║ 
    ║                          ║ 
    ╚══════════════════════════╝

{COLOR_RESET}""",
        0.005,
    )

    for _ in range(3):
        p = input(f"$~ ")
        match p:
            case "1":
                if start():
                    fprint(f"{COLOR_GREEN}Well done! You earned it!{COLOR_RESET}")
                    fprint(f"{FLAG}")
                    exit(0)
            case "2":
                inspect()
            case "3":
                jump()
            case "4":
                fprint(f"{COLOR_RED}Exiting...{COLOR_RESET}")
                exit(0)
            case _:
                fprint(f"{COLOR_RED}Invalid option{COLOR_RESET}")
    fprint(f"{COLOR_RED}GENERATOR IS OVERHEATING{COLOR_RESET}\n")
    announcer("CALLING ALL UNITS! VANDALISM OF COMPANY PROPERTY DETECTED!")
    death()


if __name__ == "__main__":
    try:
        level2()
    except Exception as e:
        fprint(f"{COLOR_RED}>>> ERROR: {type(e).__name__}{COLOR_RESET}")
        death()
