def extract_png_images(bin_path, output_prefix):
    png_header = b'\x89PNG\r\n\x1a\n'
    png_footer = b'\x00\x00\x00\x00IEND\xAEB`\x82'
    
    with open(bin_path, "rb") as bin_file:
        bin_data = bin_file.read()
    
    start = 0
    image_count = 0
    while True:
        start_image = bin_data.find(png_header, start)
        if start_image == -1:
            break
        end_image = bin_data.find(png_footer, start_image) + len(png_footer)
        if end_image == -1:
            break
        
        image_data = bin_data[start_image:end_image]
        with open(f"{output_prefix}_{image_count + 1}.png", "wb") as img_file:
            img_file.write(image_data)
        
        start = end_image
        image_count += 1
    
    print(f"{image_count} PNG images extracted.")

bin_path = "data.bin"
output_prefix = "image"

extract_png_images(bin_path, output_prefix)

