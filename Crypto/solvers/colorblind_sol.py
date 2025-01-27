from PIL import Image


def decode_image_to_string(image_path, square_size=5):
    image = Image.open(image_path).convert("RGB")
    width, height = image.size

    num_squares = width // square_size
    decoded_string = ""

    for i in range(num_squares):
        left = i * square_size
        top = 0
        right = left + square_size
        bottom = top + square_size

        square = image.crop((left, top, right, bottom))

        r, g, b = square.getpixel((0, 0))

        ascii_value = r

        decoded_string += chr(ascii_value)

    return decoded_string


def main():
    image_path = "../colorblind/colorblind.png"

    square_size = 20
    decoded_string = decode_image_to_string(image_path, square_size)

    # Print the decoded string
    print(f"Decoded string: {decoded_string}")


if __name__ == "__main__":
    main()
