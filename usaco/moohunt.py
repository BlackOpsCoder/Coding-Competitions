def moo_hunt():
    nk_values = input()
    mooves = []
    result_board = []
    max_occuring = []
    winning_count = 0
    n = int(nk_values.split()[0])
    k = int(nk_values.split()[1])
    for i in range(k):
        moove = input()
        mooves.append(moove.split())
    
    d2_board = []
    for x in range(k):
        moove = mooves[x]
        win_board = [""] * n
        win_board[int(moove[0]) - 1] = "M"
        win_board[int(moove[1]) - 1] = "O"
        win_board[int(moove[2]) - 1] = "O"
        d2_board.append(win_board)

    for ni in range(n):
        for ki in range(k):
            if d2_board[ki][ni] != "":
                max_occuring.append(d2_board[ki][ni])
        most_occurring_item = max(set(max_occuring), key=max_occuring.count)  
        result_board.append(most_occurring_item)
        max_occuring.clear()
            
    for x in range(k):
        moove = mooves[x]
        if result_board[int(moove[0]) - 1] == 'M' and result_board[int(moove[1]) - 1] == 'O' and result_board[int(moove[2]) - 1] == 'O':
            winning_count += 1

    print(winning_count, 2)

moo_hunt()