encrypted = "PH^nI~cnxBnPbb^RpEXgT"
key="1"


decrypted = []
for i in range(len(encrypted)):
    decrypted_char = chr(ord(encrypted[i]) ^ ord(key[i % 1]))
    decrypted.append(decrypted_char)

flag = "".join(decrypted)
print(flag)