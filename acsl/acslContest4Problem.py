def fillPuzzle(n, numbers):
    # Write your code here
    number_list = []
    result_list = []
    result_string = ""

    numbers = numbers.split()
    numbers = list(map(int, numbers))

    temp_list = []
    for i in range(n**2):
        if i > 0 and i % n == 0:
            number_list.append(temp_list)
            temp_list = []
        temp_list.append(numbers[i])
    number_list.append(temp_list)
    
    all_numbers = set(range(1, n**2 + 1))
    present = set(x for x in numbers if x != 0)
    missing = sorted(all_numbers - present)
    changed = True
    while changed:
        changed = False
        for m in missing:
            for r in range(n):
                for c in range(n):
                    if number_list[r][c] == 0:
                        neighbors = []
                        if r + 1 < n: neighbors.append(number_list[r+1][c])
                        if r - 1 >= 0: neighbors.append(number_list[r-1][c])
                        if c + 1 < n: neighbors.append(number_list[r][c+1])
                        if c - 1 >= 0: neighbors.append(number_list[r][c-1])

                        if (m - 1) in neighbors and (m + 1) in neighbors:
                            number_list[r][c] = m
                            missing.remove(m)
                            changed = True
                            break
            if changed:
                break

    result = []
    for r in range(n):
        for c in range(n):
            if numbers[r * n + c] == 0:
                result.append(str(number_list[r][c]))

    return " ".join(result)