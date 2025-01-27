import subprocess
import time
import string

# Function to interact with FL1TZ and measure response time
def run_flitz(input_password):
    # Start the FL1TZ process
    process = subprocess.Popen(
        ['./FL1TZ'],  # Replace with the correct path to FL1TZ if needed
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Send the password to FL1TZ
    start_time = time.time()
    process.stdin.write(input_password + '\n')
    process.stdin.flush()
    
    # Wait for the process to complete
    process.communicate()
    end_time = time.time()
    
    return end_time - start_time

# Function to perform the timing attack
def timing_attack(password_length):
    characters = string.ascii_letters + string.digits + "_{}"  # Restricted character set
    password = [''] * password_length  # Initialize the password as a list of empty strings
    threshold = 0.03 # Threshold to detect if all response times are close
    i = 0  # Initialize position to zero
    
    while i < password_length:
        max_time = 0
        best_char = ''
        response_times = []  # Keep track of response times for the current position
        
        for char in characters:
            # Build the test password with the current character in the i-th position
            test_password = ''.join(password[:i]) + char + 'a' * (password_length - i - 1)
            
            # Measure the time taken for the FL1TZ program to respond
            elapsed_time = run_flitz(test_password)
            response_times.append(elapsed_time)
            
            # Print the tested password and its response time
            print(f"Tested: {test_password}, Response Time: {elapsed_time:.6f} seconds")
            
            # If this character results in a longer response time, it might be correct
            if elapsed_time > max_time:
                max_time = elapsed_time
                best_char = char
        
        # Update the password with the best character found
        password[i] = best_char
        print(f"Progress: {''.join(password)}")
        
        # Check if the response times for the next position are too similar
        if i > 0 and max(response_times) - min(response_times) < threshold:
            print(f"Detected possible mistake at position {i}. Retrying previous position...")
            i -= 1  # Go back to the previous position
        else:
            i += 1  # Move to the next position

    return ''.join(password)

# Main function
if __name__ == "__main__":
    password_length = 12  # Replace with the actual password length or guess it
    print("Starting timing attack...")
    extracted_password = timing_attack(password_length)
    print(f"Extracted password: {extracted_password}")
