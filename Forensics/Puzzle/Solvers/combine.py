import os
from itertools import permutations

def create_combined_file(input_dir, output_dir, chunk_order):
    try:
        output_path = os.path.join(output_dir, f"output_{'_'.join(map(str, chunk_order))}.jpg")
        with open(output_path, "wb") as combined_file:
            for chunk_index in chunk_order:
                chunk_path = os.path.join(input_dir, f"payload_{chunk_index}.bin")
                with open(chunk_path, "rb") as chunk_file:
                    combined_file.write(chunk_file.read())
        print(f"Created: {output_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    input_dir = "."
    output_dir = "images"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Ensure chunk1.bin is always first
    fixed_chunk = 3
    remaining_chunks = [2, 0, 4, 5, 1]
    
    # Generate all possible permutations for the remaining chunks
    for perm in permutations(remaining_chunks):
        chunk_order = [fixed_chunk] + list(perm)
        create_combined_file(input_dir, output_dir, chunk_order)
