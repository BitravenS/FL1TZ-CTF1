from utils import (
    fprint,
    announcer,
    death,
    header,
    sleep,
    ECDSA,
    COLOR_YELLOW,
    COLOR_BLUE,
    COLOR_GREEN,
    COLOR_RED,
    COLOR_RESET,
)
import ecdsa
from datetime import datetime, timedelta
import hashlib
import random
import base64
import os

FLAG = os.getenv("FLAG")
if FLAG is None:
    raise ValueError("FLAG environment variable is not set.")


def generate_dates():
    year = 2051
    month = 4
    day = random.randint(7, 8)
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    entry = datetime(year, month, day, hour, minute, second)
    leave = entry + timedelta(
        minutes=random.randint(1, 60), hours=random.randint(1, 24)
    )
    return entry, leave


def generate_logs():
    entries = []
    keys = {}
    scientists = [
        "Ron Rivest",
        "Martin Hellman",
        "Whitfield Diffie",
        "Adi Shamir",
        "Ralph Merkle",
        "Satoshi Nakamoto",
        "David Chaum",
        "Paul Kocher",
        "Bruce Schneier",
        "Moxie Marlinspike",
        "Dan Boneh",
        "Taher Elgamal",
        "Peter Shor",
        "Shafi Goldwasser",
        "Silvio Micali",
        "Michael O. Rabin",
        "Leonard Adleman",
        "Michael Reeves",
        "Alan Turing",
        "John von Neumann",
        "Grace Hopper",
        "Ada Lovelace",
        "Charles Babbage",
        "Alan Kay",
        "Dennis Ritchie",
        "Ken Thompson",
        "Brian Kernighan",
        "Linus Torvalds",
        "Richard Stallman",
        "Bitraven",
    ]
    positions = [i for i in range(30)]
    for s in scientists:
        l = ECDSA(curve=ecdsa.SECP256k1)
        keys[s] = l
        en, lv = generate_dates()
        p = random.choice(positions)
        positions.remove(p)
        ent = f"ENTRY AT {en.strftime('%H:%M')}".encode()
        ext = f"EXIT AT {lv.strftime('%H:%M')}".encode()
        if p == 15:
            n = l.new_nonce()
            entry = base64.b64encode(
                l.sign(ent, nonce=n, hashfunc=hashlib.sha256)
            ).decode()
            leave = base64.b64encode(
                l.sign(ext, nonce=n, hashfunc=hashlib.sha256)
            ).decode()
        else:
            entry = base64.b64encode(l.sign(ent, hashfunc=hashlib.sha256)).decode()
            leave = base64.b64encode(l.sign(ext, hashfunc=hashlib.sha256)).decode()
        entries.append((s, entry, en, 1))
        entries.append((s, leave, lv, 0))
    return entries, keys


def level3():
    entries, keys = generate_logs()
    entries.sort(key=lambda x: x[2])

    def access():
        now = datetime.now()
        fprint(f"> Identify yourself: ", line=False)
        name = input(f"$~ ")
        if name not in keys:
            fprint(f"{COLOR_RED}Unauthorized{COLOR_RESET}")
            return False
        l = keys[name]
        time = now.strftime("%H:%M")
        fprint(f"""> Sign your entry "ENTRY AT {time}" : """, line=False)
        signature = input(f"$~ ")

        ver = False
        try:
            ver = l.verify(
                f"ENTRY AT {time}".encode(),
                base64.b64decode(signature),
                hashfunc=hashlib.sha256,
            )
        except ecdsa.keys.BadSignatureError:
            fprint(f"{COLOR_RED}>>> Access Denied: BAD SIGNATURE FORMAT{COLOR_RESET}")
            return False

        if ver:
            fprint(f"{COLOR_GREEN}>>> Access Granted <<<{COLOR_RESET}")
            fprint(f"{COLOR_BLUE}>>> Welcome back {name} ! {COLOR_RESET}")
            fprint(f"{COLOR_BLUE}>>> Rodd el beb wrak, el denya t5awwef{COLOR_RESET}")
            return True

        fprint(f"{COLOR_RED}>>> Access Denied: INVALID SIGNATURE{COLOR_RESET}")
        return False

    def logs():
        fprint(f"> Firmware Version: {COLOR_YELLOW}v5e7ff.0a0{COLOR_RESET}")
        fprint(
            f"> Firmware Hash: {COLOR_YELLOW}0x{hashlib.md5(b'v5e7ff').hexdigest()}{COLOR_RESET}"
        )
        fprint(f"> System Curve: {COLOR_YELLOW}SECP256k1{COLOR_RESET}")
        fprint(f"> System Hash function: {COLOR_YELLOW}SHA256{COLOR_RESET}")
        fprint(
            f"> System Signature Structure: {COLOR_YELLOW}RAW Concatenation{COLOR_RESET}"
        )
        fprint(f"{COLOR_BLUE}>>> Retrieving Logs{COLOR_RESET}")
        sleep(0.5)
        for i, (s, hash, time, action) in enumerate(entries):
            if action:
                fprint(
                    f"{COLOR_GREEN}[{time.strftime('%Y-%m-%d %H:%M:%S')}]{COLOR_RESET} {s} entered the LABS",
                    0.001,
                )
                fprint(
                    f"""\t> "ENTRY AT {time.strftime('%H:%M')}" Signature: {COLOR_YELLOW}{hash}{COLOR_RESET}\n""",
                    0.001,
                )

            else:
                fprint(
                    f"{COLOR_RED}[{time.strftime('%Y-%m-%d %H:%M:%S')}]{COLOR_RESET} {s} left the LABS",
                    0.001,
                )
                fprint(
                    f"""\t> "EXIT AT {time.strftime('%H:%M')}" Signature: {COLOR_YELLOW}{hash}{COLOR_RESET}\n""",
                    0.001,
                )

    header()

    fprint(
        f"""\n>>> Level 3: {COLOR_RESET}{COLOR_RESET}{COLOR_RESET}{COLOR_RESET}{COLOR_RED}LABS{COLOR_RESET} <<<\n""",
        0.05,
    )
    fprint(
        f"""{COLOR_BLUE}

        ╭──────────────────────╮
        │                      │
        │   TerraGroup LABS™   │
        │                      │
        │  [1] Access LABS     │
        │  [2] Check Logs      │
        │  [3] Exit            │
        │                      │
        ╰──────────────────────╯

{COLOR_RESET}""",
        0.004,
    )

    for _ in range(5):
        p = input(f"$~ ")
        if p == "1":
            if access():
                fprint(f"{COLOR_GREEN}Well done! You earned it!{COLOR_RESET}")
                fprint(f"{FLAG}")
                exit(0)
            fprint(f"""{COLOR_RED}>>> INITIATING FULL LOCKDOWN{COLOR_RESET}""")
            exit(0)
        elif p == "2":
            logs()
        elif p == "3":
            fprint(f"{COLOR_RED}Exiting...{COLOR_RESET}")
            exit(0)
        else:
            fprint(f"{COLOR_RED}Invalid option{COLOR_RESET}")
    announcer(
        f"\n{COLOR_RED}CALLING ALL UNITS! THIS GUY FIBELOU FI DARHOM YJARREB GED MA Y7EB!{COLOR_RESET}"
    )
    death()


if __name__ == "__main__":
    try:
        level3()
    except Exception as e:
        fprint(f"{COLOR_RED}>>> ERROR: {type(e).__name__}{COLOR_RESET}")
        death()
