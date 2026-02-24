import sys

def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    data_ptr = 0
    num_tests = int(input_data[data_ptr])
    data_ptr += 1
    
    for _ in range(num_tests):
        n = int(input_data[data_ptr])
        k = int(input_data[data_ptr + 1])
        data_ptr += 2
        
        nums = []
        for i in range(n):
            nums.append(int(input_data[data_ptr]))
            data_ptr += 1
            
        families = {}
        abs_k = abs(k)
        for x in nums:
            rem = x % abs_k
            ElsieNumber = x // abs_k
            if rem not in families:
                families[rem] = []
            families[rem].append(ElsieNumber)
            
        ans = 0
        
        for rem in families:
            steps = sorted(families[rem])
            
            if k > 0:
                last_pos = -float('inf')
                for s in steps:
                    actual_pos = max(s, last_pos + 1)
                    ans += (actual_pos - s)
                    last_pos = actual_pos
            else:
                flipped_steps = sorted([-s for s in steps])
                last_pos = -float('inf')
                for s in flipped_steps:
                    actual_pos = max(s, last_pos + 1)
                    ans += (actual_pos - s)
                    last_pos = actual_pos
                    
        print(ans)

if __name__ == "__main__":
    main()