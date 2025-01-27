import json
import os
import string

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "words_dictionary.json")

with open(file_path, "r") as f:
    words = json.load(f).keys()

flag = "FL1TZ{B0RN_2_N4GU3Z_4ND_W1LL_4LW4Y5_N4GU3Z_B4BY}"


class Hopper:
    def __init__(self, keyword):
        self.alpha = string.ascii_uppercase
        self.keyword = keyword.upper()
        self.initialAlpha()

    def initialAlpha(self):
        for i in self.keyword:
            self.shuffle(i)
        self.initial = self.alpha

    def shuffle(self, letter):
        i = 0
        try:
            i = self.alpha.index(letter)
        except Exception as e:
            print(f"{letter}: {e}")
        self.alpha = self.alpha[:i][::-1] + self.alpha[i] + self.alpha[i + 1 :][::-1]

    def encrypt(self, plaintext):
        self.alpha = self.initial
        plaintext = plaintext.upper()
        ciphertext = ""
        for i in plaintext:
            pos = string.ascii_uppercase.index(i)
            ciphertext += self.alpha[pos]
            self.shuffle(i)
        return ciphertext

    def decrypt(self, ciphertext):
        self.alpha = self.initial
        plaintext = ""
        for i in ciphertext:
            pos = self.alpha.index(i)
            corLet = string.ascii_uppercase[pos]
            plaintext += corLet
            self.shuffle(corLet)
        return plaintext


def flag_format(f):
    ret = ""
    for letter in f:
        if letter.isalpha():
            ret += letter
        else:
            match letter:
                case "0":
                    ret += "ZERO"
                case "1":
                    ret += "ONE"
                case "2":
                    ret += "TWO"
                case "3":
                    ret += "THREE"
                case "4":
                    ret += "FOUR"
                case "5":
                    ret += "FIVE"
                case "6":
                    ret += "SIX"
                case "7":
                    ret += "SEVEN"
                case "8":
                    ret += "EIGHT"
                case "9":
                    ret += "NINE"
                case "_":
                    ret += "UNDRSCR"
                case "{":
                    ret += "OPNBRCKT"
                case "}":
                    ret += "CLSBRCKT"
                case _:
                    raise ValueError(f"Invalid character: {letter}")
    return ret


def flag_unformat(f):
    ret = ""
    temp = f
    while temp:
        if temp.startswith("ZERO"):
            ret += "0"
            temp = temp[4:]
        elif temp.startswith("ONE"):
            ret += "1"
            temp = temp[3:]
        elif temp.startswith("TWO"):
            ret += "2"
            temp = temp[3:]
        elif temp.startswith("THREE"):
            ret += "3"
            temp = temp[5:]
        elif temp.startswith("FOUR"):
            ret += "4"
            temp = temp[4:]
        elif temp.startswith("FIVE"):
            ret += "5"
            temp = temp[4:]
        elif temp.startswith("SIX"):
            ret += "6"
            temp = temp[3:]
        elif temp.startswith("SEVEN"):
            ret += "7"
            temp = temp[5:]
        elif temp.startswith("EIGHT"):
            ret += "8"
            temp = temp[5:]
        elif temp.startswith("NINE"):
            ret += "9"
            temp = temp[4:]
        elif temp.startswith("UNDRSCR"):
            ret += "_"
            temp = temp[7:]
        elif temp.startswith("OPNBRCKT"):
            ret += "{"
            temp = temp[8:]
        elif temp.startswith("CLSBRCKT"):
            ret += "}"
            temp = temp[8:]
        else:
            ret += temp[0]
            temp = temp[1:]
    return ret


def main():
    KEY = "kleptomania"
    assert KEY in words

    story1 = "there is an ongoing race to push the bitcoin encryption to its limits called the 32 btc challenge".replace(
        " ", ""
    ).upper()
    story2 = "it went up to almost 1000 btc for anyone brave enough to give it a try and youre damn right frou5 li tnagguez will be on the frontlines".replace(
        " ", ""
    ).upper()
    FLAG = story1 + flag + story2
    print(f"KEY: {KEY}")
    hopper = Hopper(KEY)
    cipher = hopper.encrypt(flag_format(FLAG))
    print(f"FLAG: {cipher}")
    decipher = hopper.decrypt(cipher)
    print("Deciphered:", decipher)
    decode = flag_unformat(decipher)
    print("Decoded:", decode)


if __name__ == "__main__":
    main()
