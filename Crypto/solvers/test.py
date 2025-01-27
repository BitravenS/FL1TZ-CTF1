from os import wait
import random
import string

alphabet = list(string.ascii_uppercase)
random.shuffle(alphabet)

shuffled_alphabet = "".join(alphabet)
alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
message = "TWELVE IN ALGEBRA IS A DREAM"
enc = ""
for i in message:
    if i in alpha:
        enc += shuffled_alphabet[alpha.index(i)]
    else:
        enc += i
print(enc)
print("".join(list(set(message))))
