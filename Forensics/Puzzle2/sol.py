import os

def read_data(file_path, chunk_size):
    with open(file_path, "rb") as file:
        data = file.read()
    chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
    if len(chunks[-1]) < chunk_size:
        chunks[-1] += b"\x00" * (chunk_size - len(chunks[-1]))
    return chunks

def unscramble_data(scrambled_chunks, s):

    num_chunks = 15000
    original_chunks = [b"\x00" * len(scrambled_chunks[0]) for _ in range(num_chunks)]
    for pos in range(num_chunks):
        original_i = ((pos - s) * 107143) % num_chunks
        original_chunks[original_i] = scrambled_chunks[pos]
    return original_chunks

def write_data(file_path, chunks):
    with open(file_path, "wb") as file:
        for chunk in chunks:
            file.write(chunk)

def main():
    input_file = "file.bin"
    output_file_template = "unscrambled_data_s_{}.png"
    file_size = os.path.getsize(input_file)
    

    num_chunks = 15000
    chunk_size = file_size // num_chunks

    scrambled_chunks = read_data(input_file, chunk_size)

    for s in range(20):
        original_chunks = unscramble_data(scrambled_chunks, s)
        output_file = output_file_template.format(s)
        write_data(output_file, original_chunks)
        print(f"Unscrambled data with s = {s} saved to {output_file}.")

main()