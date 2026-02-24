import sys

def solve():
    # Reading input using fast I/O
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    ptr = 0
    T_cases = int(input_data[ptr])
    ptr += 1
    
    for _ in range(T_cases):
        N = int(input_data[ptr])
        M = int(input_data[ptr + 1])
        ptr += 2
        
        target = list(input_data[ptr])
        ptr += 1
        
        # Convert strings to lists of characters for easy swapping
        S = []
        for i in range(N):
            S.append(list(input_data[ptr]))
            ptr += 1
            
        ops = []
        
        # Iterate through each character position in s1
        for k in range(M):
            if S[0][k] == target[k]:
                continue
                
            found = False
            # Look for the required character in strings s2 through sN
            for y in range(1, N):
                # First check if the character exists at the same index in another string
                if S[y][k] == target[k]:
                    # Op Type 2: Swap k-th char of s1 and sy
                    S[0][k], S[y][k] = S[y][k], S[0][k]
                    ops.append(f"2 1 {y+1} {k+1}")
                    found = True
                    break
            
            if not found:
                # If not at the same index, find it anywhere in other strings
                for y in range(1, N):
                    for j in range(M):
                        if S[y][j] == target[k]:
                            # Op Type 1: Swap j-th and k-th char in sy
                            S[y][j], S[y][k] = S[y][k], S[y][j]
                            ops.append(f"1 {y+1} {j+1} {k+1}")
                            
                            # Op Type 2: Swap k-th char of s1 and sy
                            S[0][k], S[y][k] = S[y][k], S[0][k]
                            ops.append(f"2 1 {y+1} {k+1}")
                            
                            found = True
                            break
                    if found: break
        
        # Output result for this test case
        print(len(ops))
        if ops:
            print("\n".join(ops))

if __name__ == "__main__":
    solve()