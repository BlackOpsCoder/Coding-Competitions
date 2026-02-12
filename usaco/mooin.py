def mooin():
    s_list = []
    ks_list = []
    kt_input = input()
    kt_list = kt_input.split()
    if len(kt_list) != 2:
        return ValueError("K and T values are invalid")
    # ToDo: Handling Integer cast failure
    t = int(kt_list[0])
    k = int(kt_list[1])

    # Taking N & S for T test cases
    for i in range(t):
        n = int(input())
        s = input()
        if len(s) != n:
            return ValueError("S is not N long")
        s_list.append(s)

    # run a for loop on s_list
    for s in s_list:
    # Convert s to char array
        ks_char_array = list(s)
    # Run a for loop starting from right 
        for i in range(len(ks_char_array)-1, -1, -1):
    # If char is "M", do nothing, else: flip all characters left of that character
            if ks_char_array[i] == "O":
                for x in range(0, i, 1):
                    if ks_char_array[x] == "M":
                        ks_char_array[x] = "O"
                    elif ks_char_array[x] == "O":
                        ks_char_array[x] = "M"
            
        ks_list.append("".join(ks_char_array))   

    # if k = 0, return yes, else: return yes and ks
    for ksa in range(len(ks_list)):
        print("YES")
        if k == 1:
            print(ks_list[ksa])
            
    
mooin()

    