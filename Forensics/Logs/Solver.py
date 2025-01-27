import re

log_file_path = "FL1TZServer.logs"  

key = []
text = []

log_pattern = re.compile(r"Response: (\d{3}) .*?Attempted (0x[0-9A-F]+), \{K:(\d),T:(\d)\}")

with open(log_file_path, "r") as file:
    for line in file:
        match = log_pattern.search(line)
        if match:
            status_code, hex_char, k_value, t_value = match.groups()
            
            
            if status_code == "200":
                char = chr(int(hex_char, 16))  # Convert hex to character
                
                
                if k_value == "1" and t_value == "0":
                    key.append(char)
                elif k_value == "0" and t_value == "1":
                    text.append(char)


key_str = ''.join(key)
text_str = ''.join(text)


print("Key:", key_str)
print("Text:", text_str)
