import sys

# Simplified logic: just return the boolean directly
def is_odd(num):
    return num % 2 != 0
    
# Optimization: This now takes the list directly to avoid re-converting
def is_binary_format(num_array):
    for digit in num_array:
        if digit > 1:
            return False
    return True

# Optimized with list comprehension for speed
def int_to_array(n):
    if n == 0: return [0]
    return [int(d) for d in str(n)]

# Keep your math-based version, it's efficient
def array_to_int(digits):
    result = 0
    for d in digits:
        result = result * 10 + d
    return result

def strange_function(number):
    # One single conversion to array
    number_array = int_to_array(number)
    
    # Check binary format using the ALREADY created array
    if is_binary_format(number_array):
        return number - 1
    
    # Modify the array in-place
    for i in range(len(number_array)):
        number_array[i] = number_array[i] % 2 # Even faster than calling is_odd
        
    return array_to_int(number_array)

def main_function():
    # Optimization: Use fast I/O for large test cases
    test_cases_count = int(input())
    test_cases_list = []

    for i in range(test_cases_count):
        test_cases_list.append(int(input()))    
    
    MOD = 10**9 + 7

    # Process each case immediately to save memory
    for i in range(0, test_cases_count):
        test_input = int(test_cases_list[i])
        count = 0
        while test_input != 0:
            test_input = strange_function(test_input)
            count += 1
        print(count % MOD)

if __name__ == "__main__":
    main_function()