import os
from itertools import permutations

def create_combined_file(input_dir, output_dir, chunk_order):
    output_path = os.path.join(output_dir, f"output_{'_'.join(map(str, chunk_order))}.png")
    with open(output_path, "wb") as combined_file:
        for chunk_index in chunk_order:
            chunk_path = os.path.join(input_dir, f"payload_{chunk_index}.bin")
            with open(chunk_path, "rb") as chunk_file:
                combined_file.write(chunk_file.read())

if __name__ == "__main__":
    input_dir = "udp_payloads"
    output_dir = "images"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for perm in permutations(range(6)):
        create_combined_file(input_dir, output_dir, list(perm))
