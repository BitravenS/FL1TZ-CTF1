import subprocess
import time
import string


def run_flitz(input_password):

    process = subprocess.Popen(
        ['./FL1TZ'],  
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    

    start_time = time.time()
    process.stdin.write(input_password + '\n')
    process.stdin.flush()
    

    process.communicate()
    end_time = time.time()
    
    return end_time - start_time


def timing_attack(password_length):
    characters = string.ascii_letters + string.digits + "_{}"  
    password = [''] * password_length  
    threshold = 0.03 
    i = 0  
    
    while i < password_length:
        max_time = 0
        best_char = ''
        response_times = []  
        
        for char in characters:

            test_password = ''.join(password[:i]) + char + 'a' * (password_length - i - 1)
            

            elapsed_time = run_flitz(test_password)
            response_times.append(elapsed_time)
            

            print(f"Tested: {test_password}, Response Time: {elapsed_time:.6f} seconds")
            

            if elapsed_time > max_time:
                max_time = elapsed_time
                best_char = char
        

        password[i] = best_char
        print(f"Progress: {''.join(password)}")
        

        if i > 0 and max(response_times) - min(response_times) < threshold:
            print(f"Detected possible mistake at position {i}. Retrying previous position...")
            i -= 1  
        else:
            i += 1  

    return ''.join(password)


if __name__ == "__main__":
    password_length = 12
    print("Starting timing attack...")
    extracted_password = timing_attack(password_length)
    print(f"Extracted password: {extracted_password}")
