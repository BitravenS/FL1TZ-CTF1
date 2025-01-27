from PIL import Image


def create_grayscale_square(char, size=5):

    ascii_value = ord(char)
    return Image.new("RGB", (size, size), color=(ascii_value, ascii_value, ascii_value))


def encode_string_to_image(text, square_size=5):

    num_chars = len(text)
    image_width = num_chars * square_size
    image_height = square_size

    # Create a blank image to hold the concatenated squares
    final_image = Image.new(
        "RGB", (image_width, image_height), color=(255, 255, 255)
    )  # White background

    # Iterate through each character and paste its square into the final image
    for i, char in enumerate(text):
        square = create_grayscale_square(char, square_size)
        final_image.paste(square, (i * square_size, 0))

    return final_image


def main():
    text = "FL1TZ{C4ll_4N_4MbulAnc3_but_n0t_f0r_m3}"

    square_size = 20
    image = encode_string_to_image(text, square_size)

    image.save("colorblind.png")


if __name__ == "__main__":
    main()
