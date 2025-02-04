import string

print("Decryptingggg .")

v2="0111000000110010011000100101010101100010010100100110100101111101011010110010011001010010011111010010011101010111010100100110111101111000011110010101001001111101001001000110001001010100011111100100101000110100001001000100011001000000"
l=[v2[i:i+8]for i in range(0,len(v2),8)]
l2 = [f"{(int(e, 2) ^ int('00001000', 2)):08b}" for e in l]
v2="".join(l2)
l3=[chr(int(v2[i:i+8],2))for i in range(0,len(v2),8)]
v2="".join(l3)

v2 = v2[::-1]


v2 = ''.join([chr((ord(v4) + 5) % 256) for v4 in v2])


v2 = ''.join([chr(((ord(v4) - 97 - 20) % 26) + 97) if 'a' <= v4 <= 'z' else
              (chr(((ord(v4) - 65 - 20) % 26) + 65) if 'A' <= v4 <= 'Z' else v4) for v4 in v2])

v2 = ''.join([chr(((ord(v4) - 97 - 13) % 26) + 97) if 'a' <= v4 <= 'z' else
              (chr(((ord(v4) - 65 - 13) % 26) + 65) if 'A' <= v4 <= 'Z' else v4) for v4 in v2])


print("flag  :", v2)

