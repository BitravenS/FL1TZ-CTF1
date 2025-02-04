import os

def extract_hidden_zip(combined_file, output_zip="hidden.zip"):
    jpg_end_marker = b"\xFF\xD9"

    with open(combined_file, "rb") as file:
        data = file.read()

    jpg_end_index = data.find(jpg_end_marker)
    if jpg_end_index == -1:
        print("Error: JPG end marker (0xFFD9) not found.")
        return

    jpg_end = jpg_end_index + 2
    print(f"JPG file ends at byte offset: {jpg_end}")

    zip_data = data[jpg_end:]
    if not zip_data:
        print("Error: No data found after the JPG file.")
        return

    with open(output_zip, "wb") as zip_file:
        zip_file.write(zip_data)

    print(f"Hidden ZIP file extracted to: {output_zip}")

    if os.path.exists(output_zip):
        os.system(f"unzip {output_zip}")
        print(f"Extracted contents of {output_zip}")
extract_hidden_zip("Burger.jpg")
# Then fix the zip file with this command : "zip -FF hidden.zip --out hidden_fixed.zip"


