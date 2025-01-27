#!/usr/bin/env python3

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import binascii
import os
import random


COLOR_RED = "\x1b[31m"
COLOR_GREEN = "\x1b[32m"
COLOR_YELLOW = "\x1b[33m"
COLOR_BLUE = "\x1b[34m"
COLOR_RESET = "\x1b[0m"
KEY = os.urandom(16)

FLAG = os.getenv("FLAG")
if FLAG is None:
    raise ValueError("FLAG environment variable is not set.")


def header():
    with open("./ascii-art.txt", "r") as f:
        art = f.read()
    print(f"""{COLOR_BLUE}{art}{COLOR_RESET}""")


def encrypt(key, data, iv):
    iv = pad(iv.encode(), 16)[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return binascii.hexlify(cipher.encrypt(pad(data, 16))).decode()


def decrypt(key, data, iv):
    iv = pad(iv.encode(), 16)[:16]
    data = binascii.unhexlify(data)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return binascii.hexlify(cipher.decrypt(data)).decode()


gen_z = [
    "skibidy sigma",
    "W rizz no cap",
    "shadow wizard money gang",
    "gigachad",
    "7afouzli9",
    "Boutafli9a",
    "literally me fr",
    "ohio gyatt",
    "hitting the griddy on gang",
    "Ga3four >>>",
    "only in ohio ngl",
    "MPI2 got me tweakin",
    "my life be like",
    "oo ii aa oo ii aa",
]


def counter_cringe_measures(sauce):
    gucci = True
    for z in gen_z:
        e = encrypt(KEY, FLAG.encode(), z)
        if e == sauce:
            gucci = False
            break
    return gucci


def menu():
    print(f"{COLOR_RED}---What do you want to do?---{COLOR_RESET}")
    print(f"{COLOR_GREEN}1. Encrypt{COLOR_RESET}")
    print(f"{COLOR_GREEN}2. Decrypt{COLOR_RESET}")
    print(f"{COLOR_GREEN}3. Gimme The flag{COLOR_RESET}")
    print(f"{COLOR_GREEN}4. Exit{COLOR_RESET}")


def gen_iv():
    return random.choice(gen_z)


def main():
    header()
    print(
        f"""{COLOR_YELLOW}

█▀█   █ █   ▄▀█   █▀▀   █▀█   █▀▀ █▀▀   █ █   ▄▀█   █
█▄█   █ █   █▀█   ██▄   █▄█   ██▄ ██▄   █ █   █▀█   █

{COLOR_RESET}"""
    )

    menu()
    while True:
        try:
            print("-" * 30)
            choice = input(f"{COLOR_BLUE}> {COLOR_RESET}")
            if choice == "1":
                data = input(f"What's so secret?: ")
                iv = input(f"What's the IV: ")
                print("Nah, I'll pick an IV for you")
                print(f"Here you go G: {encrypt(KEY, data.encode(), gen_iv())}")
            elif choice == "2":
                data = input(f"Drop the sauce: ")
                iv = input(f"Got an IV?: ")
                if iv not in gen_z:
                    print(f"\n{COLOR_BLUE}L")
                    exit(1)

                if not counter_cringe_measures(data):
                    print(f"{COLOR_RED}NUH UHH{COLOR_RESET}")
                    exit(1)

                print(f"Here's the rizz : {decrypt(KEY, data.encode(), iv)}")
            elif choice == "3":
                print(
                    f"""Here's the sigma rizz, with a funy twist: {encrypt(KEY, FLAG.encode(), gen_iv())}"""
                )
            elif choice == "4":
                print(f"{COLOR_GREEN}So long, beta ahh{COLOR_RESET}")
                exit(0)
            else:
                print(f"You're lowkey Tweakin' fr")
                exit(1)
        except ValueError:
            print(f"{COLOR_RED}WTF is that ciphertext dawg??{COLOR_RESET}")
            exit(1)
        except Exception:
            print(f"{COLOR_RED}Wait... something ain't right{COLOR_RESET}")
            exit(1)


if __name__ == "__main__":
    main()
