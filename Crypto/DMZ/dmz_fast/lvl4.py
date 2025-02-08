from utils import (
    fprint,
    announcer,
    death,
    header,
    COLOR_YELLOW,
    COLOR_BLUE,
    COLOR_GREEN,
    COLOR_RED,
    COLOR_RESET,
)

import json
import os
import hashlib
import random
from lv4_curve import (
    gen_keypair,
    public_pem,
    signature_gen,
    privkey_to_pubkey,
    public_pem,
    encode_signature,
    decode_signature,
    verify_signature,
)

FLAG = os.getenv("FLAG")
if FLAG is None:
    raise ValueError("FLAG environment variable is not set.")


def whiteboard():
    fprint(f"> The whiteboard is filled with scribbles")
    fprint(f"> It looks like a bunch of numbers and letters")
    fprint(f"> I can't make any sense of it")
    fprint(
        f"""{COLOR_BLUE}>>> Finalized the adoption of the BRAINPOOLP512r1 curve in the vault's security system{COLOR_RESET}"""
    )
    fprint(
        f"""{COLOR_BLUE}>>> This is a State of the Art ECC implementation, relying on 512bit security{COLOR_RESET}"""
    )
    fprint(
        f"""{COLOR_BLUE}>>> Making it more secure than {COLOR_RED}15360-bit RSA!!!{COLOR_RESET} I'm not even kidding..."""
    )
    fprint(f"""{COLOR_BLUE}>>> The vault should now be INPENETRABLE{COLOR_RESET}""")
    fprint(f"> Are you sure about that?")


def note():
    fprint(f"> This looks more like a diary than a note, let's see what it says:")
    fprint(
        f"""{COLOR_BLUE}>>> 2051-07-14: As per the order of the National Security Agency, we've fully upgraded our security protocol to the broadest curve currently on the market{COLOR_RESET}"""
    )
    fprint(
        f"""{COLOR_BLUE}>>> 2051-07-14: The BRAINPOOLP512r1 curve is THE best of the best, and we'll prove its capabilities over the coming weeks{COLOR_RESET}"""
    )
    fprint(
        f"""{COLOR_BLUE}>>> 2051-07-20: Our team of mathematicians, the brightest in the world, have been trying to pry its security wide open over the past week, but to no avail{COLOR_RESET}"""
    )
    fprint(
        f"""{COLOR_BLUE}>>> 2051-07-24: Some rumors came to our attention that, with enough "signatures", issues and "hope", any ECC implementation could be undermined. These are all hoaxes forged to sabotage our operations, and we will not allow it.{COLOR_RESET}"""
    )
    fprint(
        f"""{COLOR_BLUE}>>> The SPECULATORS have been sharing this paper around {COLOR_RED}https://eprint.iacr.org/2019/023.pdf{COLOR_BLUE} ... bunch of nonesense{COLOR_RESET}"""
    )
    fprint(
        f"""{COLOR_BLUE}>>> 2051-07-24: Besides, we have the best scientists and mathematicians in the world, out implementation can't possibly be flawed...{COLOR_RESET}"""
    )
    fprint(f"> I think I know what they're talking about")
    fprint(f"> The test bench over there has been set up to provide test signatures...")


def level4():
    l4_priv_key, l4_pub_key = gen_keypair()
    l4_pub_point = privkey_to_pubkey(l4_priv_key)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "words_dictionary.json")
    used_sigs = []

    with open(file_path, "r") as f:
        words = list(json.load(f).keys())

    words = [word for word in words if len(word) > 5]

    def test_bench():
        fprint(f"> Firmware Version: {COLOR_YELLOW}vFF9815C???{COLOR_RESET}")
        fprint(
            f"> Firmware Hash: {COLOR_YELLOW}0x{hashlib.md5(b'vFF9815C').hexdigest()}{COLOR_RESET}"
        )
        fprint(f"> System Curve: {COLOR_YELLOW}BRAINPOOLP512r1{COLOR_RESET}")
        fprint(f"> System Hash function: {COLOR_YELLOW}SHA256{COLOR_RESET}")
        fprint(f"> System Signature Structure: {COLOR_YELLOW}DER encoded{COLOR_RESET}")
        fprint(f"> System Public Key")
        fprint(
            f"{COLOR_GREEN}{public_pem(l4_pub_key).decode('utf-8')}{COLOR_RESET}",
            delay=0.001,
        )
        fprint(f"> Test Bench: {COLOR_YELLOW}Ready{COLOR_RESET}")
        word = random.choice(words)
        fprint(
            f"""> Running tests: generating signatures of the keyword "{word}"...\n"""
        )
        sigs = signature_gen(l4_priv_key, 5, word, 128)["signatures"]
        for i, sig in enumerate(sigs):
            encoded = encode_signature(sig["r"], sig["s"])
            used_sigs.append(encoded)
            fprint(
                f"""{COLOR_YELLOW}>>> Signature {i+1}{COLOR_RESET}: {encoded}\n""",
                0.001,
            )
        fprint(
            f"{COLOR_RED}> WARNING: Due to the unusally large key size, the hardware could only generate 384-bits of random nonces{COLOR_RESET}"
        )

    def fingerprint():
        fprint(f"> Sign this message to open the vault: ", line=False)
        message = "UNLOCK" + str(random.randint(0, 1000))
        fprint(message)
        signature = input(f"$~ ")
        if signature in used_sigs:
            fprint(f"{COLOR_RED}SMARTASS DETECTED!{COLOR_RESET}")
            return False
        ver = False
        try:
            ver = verify_signature(
                l4_pub_point, decode_signature(signature), message.encode()
            )
        except Exception as e:
            fprint(f"{COLOR_RED}>>> Access Denied: {e}{COLOR_RESET}")
            return False
        if ver:
            fprint(f"{COLOR_GREEN}>>> Vault Unlocked!{COLOR_RESET}")
            return True
        fprint(f"{COLOR_RED}>>> Access Denied: INVALID SIGNATURE{COLOR_RESET}")
        return False

    header()

    fprint(
        f"""\n>>> Final Level: {COLOR_RESET}{COLOR_RESET}{COLOR_RESET}{COLOR_RESET}{COLOR_RED}No Place for Renegades{COLOR_RESET} <<<\n""",
        0.05,
    )

    fprint(
        f"""{COLOR_YELLOW}

        ═══════════════════════════════════════════

            What do you want to investigate?

                [1] - The Whiteboard
                [2] - The Note
                [3] - The Fingerprint Scanner
                [4] - The Test Bench
                [5] - The Exit door

        ═══════════════════════════════════════════

{COLOR_RESET}""",
        0.004,
    )
    untested = 1
    for _ in range(5):
        p = input(f"$~ ")
        if p == "1":
            whiteboard()
        elif p == "2":
            note()
        elif p == "3":
            if fingerprint():
                fprint(f"{COLOR_GREEN}No one has ever made it this far...{COLOR_RESET}")
                fprint(f"{COLOR_GREEN}But you... you are SPECIAL{COLOR_RESET}")
                fprint(
                    f"{COLOR_GREEN}Who cares about the cure lmao, here's your flag buddy: {COLOR_RESET}",
                    line=False,
                )
                fprint(f"{FLAG}")
                fprint(f"{COLOR_GREEN}>>> You've earned it!{COLOR_RESET}")
                exit(0)
        elif p == "4":
            if untested:
                test_bench()
                untested = 0
            else:
                fprint(f"> I already ran my tests")

        elif p == "5":
            fprint(f"{COLOR_BLUE}Yep, I'm outta hete...{COLOR_RESET}")
            exit(0)
        else:
            fprint(f"{COLOR_RED}Invalid option{COLOR_RESET}")
    fprint(f"{COLOR_RED}TIME'S UP!{COLOR_RESET}")
    death()


if __name__ == "__main__":
    try:
        level4()
    except Exception as e:
        fprint(f"{COLOR_RED}>>> ERROR: {type(e).__name__}{COLOR_RESET}")
        death()
