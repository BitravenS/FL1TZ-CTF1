import os
import random


def SP(index, k, s, num_chunks):
    return (index * k + s) % num_chunks


def RE(image_path):
    with open(image_path, "rb") as img_file:
        return img_file.read()


def pad_data(Data, num_chunks=15000):
    total_size = len(Data)
    chunk_size = (total_size + num_chunks - 1) // num_chunks
    padded_size = chunk_size * num_chunks
    padding_needed = padded_size - total_size
    return Data + bytes([0xFF] * padding_needed), chunk_size


def SPC(data, chunk_size):
    return [data[i : i + chunk_size] for i in range(0, len(data), chunk_size)]


def SCR(chunks, k, s):
    num_chunks = len(chunks)
    scrambled = [b""] * num_chunks
    assigned = set()
    for i in range(num_chunks):
        x = SP(i, k, s, num_chunks)
        while x in assigned:
            x = (x + 1) % num_chunks
        scrambled[x] = chunks[i]
        assigned.add(x)
    return scrambled


def Save_data(chunks, output_path):
    with open(output_path, "wb") as out_file:
        for chunk in chunks:
            out_file.write(chunk)


output_path = "file.bin"
image_path = "Musashi.png"
k = random.randint(0, 10)
s = random.randint(0, 20)
Data = RE(image_path)
padded_data, chunk_size = pad_data(Data)
chunks = SPC(padded_data, chunk_size)
SCC = SCR(chunks, k, s)
Save_data(SCC, output_path)
