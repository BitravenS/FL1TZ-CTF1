import os
import zipfile

def extract_nested_zip(zip_path="outermost.zip", output_dir="extracted"):
    os.makedirs(output_dir, exist_ok=True)
    current_zip = zip_path
    
    while True:
        with zipfile.ZipFile(current_zip, 'r') as zf:
            file_list = zf.namelist()
            if len(file_list) != 1:
                print("Unexpected ZIP structure.")
                return
            
            extracted_file = os.path.join(output_dir, file_list[0])
            zf.extract(file_list[0], output_dir)
        
        if file_list[0].endswith(".txt"):
            print(f"Found text file: {extracted_file}")
            with open(extracted_file, "r") as f:
                print("Contents:", f.read())
            return
        
        current_zip = extracted_file
        
if __name__ == "__main__":
    extract_nested_zip()
