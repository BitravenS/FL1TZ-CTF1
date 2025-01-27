from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes
import sys
from math import gcd
from time import sleep
import os

COLOR_RED = "\x1b[31m"
COLOR_GREEN = "\x1b[32m"
COLOR_YELLOW = "\x1b[33m"
COLOR_BLUE = "\x1b[34m"
COLOR_RESET = "\x1b[0m"
FLAG = os.getenv("FLAG")
if FLAG is None:
    raise ValueError("FLAG environment variable is not set.")

ASCII_ART = r""" 
           ▄▄                                                      
▀███▀▀▀██▄ ██   ██                                                 
  ██    ██      ██                                                 
  ██    █████ ██████▀███▄███ ▄█▀██▄ ▀██▀   ▀██▀  ▄▄█▀██▀████████▄  
  ██▀▀▀█▄▄ ██   ██    ██▀ ▀▀██   ██   ██   ▄█   ▄█▀   ██ ██    ██  
  ██    ▀█ ██   ██    ██     ▄█████    ██ ▄█    ██▀▀▀▀▀▀ ██    ██  
  ██    ▄█ ██   ██    ██    ██   ██     ███     ██▄    ▄ ██    ██  
▄████████▄████▄ ▀████████▄  ▀████▀██▄    █       ▀█████▀████  ████▄

"""


def rsa_encrypt(t, e, n):
    return pow(t, e, n)


def encrypt(pt, e, n):
    ret = ""
    prev = 0
    for w in pt:
        enc = prev ^ rsa_encrypt(ord(w), e, n)
        if enc == 0:
            ret += "0"
        else:
            ret += hex(enc)[2:]
        prev = rsa_encrypt(ord(w), e, n)
    return ret


def fprint(word, delay=0.02, line=True):
    for w in word:
        sys.stdout.write(w)
        sys.stdout.flush()
        sleep(delay)
    if line:
        sys.stdout.write("\n")
        sys.stdout.flush()


def main():
    p, q = getPrime(512), getPrime(512)
    e = 0x10001
    phi = (p - 1) * (q - 1)
    while gcd(e, phi) != 1:
        p, q = getPrime(512), getPrime(512)
        phi = (p - 1) * (q - 1)

    n = p * q

    fprint(f"{COLOR_BLUE}{ASCII_ART}{COLOR_RESET}", 0.002)
    fprint(f"{COLOR_RED}Ready for a wild ride?{COLOR_RESET}")
    sleep(1)
    fprint(f"Don't you think RSA is getting a bit {COLOR_BLUE}boring?{COLOR_RESET}")
    sleep(1)
    fprint(f"Let's{COLOR_YELLOW} spice it up a bit......{COLOR_RESET}", 0.05)
    fprint("-" * 30)
    fprint(
        f"Here's your flag, good luck! {COLOR_GREEN}you'll need it ;){COLOR_RESET}",
        0.05,
    )
    fprint(f"> {encrypt(FLAG, e, n)}", 0.001)
    fprint("-" * 30)
    sleep(0.5)
    fprint(f"{COLOR_BLUE}Can't forget your parameters! {COLOR_RESET}", 0.05)
    fprint(f"\ne: {e}\n\nn: {n}", 0.005)
    fprint("-" * 30)
    sleep(0.5)
    fprint(f"Don't worry, {COLOR_YELLOW}I'll help you a bit{COLOR_RESET}", 0.05)
    fprint(f"Tell me whatever you want, and I'll encrypt it for you. ", line=False)
    fprint(f"{COLOR_RED}Deal?{COLOR_RESET}", 0.1)
    fprint(f"Alright,{COLOR_RESET*3} how many times do you want to try? ", line=False)
    tries = 257
    while tries > 256:
        tries = int(input())
        if tries == 256:
            fprint(
                f"{COLOR_BLUE}Well Done! 256 is the {COLOR_RED}MAXIMUM {COLOR_BLUE}that you'll need. {COLOR_YELLOW}This is a HINT btw ;){COLOR_RESET}"
            )
        if tries > 256:
            fprint(f"{COLOR_RED}I'm not that generous...{COLOR_RESET}")
        elif tries < 1:
            fprint(f"{COLOR_RED}That's... that's not how it works...{COLOR_RESET}")
            tries = 257
        else:
            break
        fprint(f"Try again: ", line=False)
    fprint(f"Fair enough, {COLOR_YELLOW}here we go!{COLOR_RESET}")
    fprint(
        f"{COLOR_GREEN}PS:\n\t-Type 'exit' to exit\n\t-Connect on port 1237 for less animations!{COLOR_RESET}"
    )

    for _ in range(tries):
        print("")
        pt = input(f"> ")
        if pt == "exit":
            fprint(f"{COLOR_RED}Already gave up? Damn...{COLOR_RESET}")
            exit(0)
        print(f"{COLOR_GREEN}Here you go: {COLOR_RESET}")
        print(f"{encrypt(pt, e, n)}")
        sys.stdout.flush()
    fprint(f"{COLOR_RED}Enough bruteforce for today...{COLOR_RESET}")


if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        fprint(f"{COLOR_RED}Wait, something ain't right...{COLOR_RESET}")
        sys.exit(1)
