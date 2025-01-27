def rotate_char(c, shift):

    if c.isalpha():
        shift %= 26  # Ensure shift is within the alphabet range
        base = ord("a") if c.islower() else ord("A")
        return chr((ord(c) - base + shift) % 26 + base)
    return c


def encrypt(message, shift):

    encrypted_message = ""
    for i, char in enumerate(message):
        # Rotate each character by (shift + i) positions
        encrypted_message += rotate_char(char, shift + i)
    return encrypted_message


def decrypt(encrypted_message, shift):

    decrypted_message = ""
    for i, char in enumerate(encrypted_message):
        # Reverse the rotation by subtracting (shift + i) positions
        decrypted_message += rotate_char(char, -(shift + i))
    return decrypted_message


if __name__ == "__main__":
    message = "FL1TZ{ROund_4nD_RouND_We_gOo}"
    shift = 5  # Initial shift value

    encrypted = encrypt(message, shift)
    print(f"Encrypted: {encrypted}")

    decrypted = decrypt(encrypted, shift)
    print(f"Decrypted: {decrypted}")
