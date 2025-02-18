blank = "-"

# general list util
def lastIndexOf(num, list, last_idx=-1, curr_idx=0):
    if list == []:
        return last_idx
    
    new_last = last_idx
    if list[0] == num:
        new_last = curr_idx
    return lastIndexOf(num, list[1:], new_last, curr_idx + 1)

# all boards are rectangular
def make_board(num_cols=7, num_rows=5):
    return [[blank] * num_rows for _ in range(num_cols)]
        
# board is a list of columns and we want to print by row
# prints a blank line before printing the board
def print_board(board):
    print
    num_cols, num_rows = len(board), len(board[0])
    for i in range(num_rows):
        row = [board[j][i] for j in range(num_cols)]
        row = map(str, row)
        print " ".join(row)
    print " ".join(map(str, range(num_cols)))
        
def possible_moves(board):
    moves = []
    for i, col in enumerate(board):
        if blank in col:
            moves.append(i)
    return moves
    
# create a new board by inserting a @player piece into @col
# does not check for valid insertion. will throw -1 index error
def next_state(old, player, col):
    import copy
    new = copy.deepcopy(old)
    col_to_insert = new[col]
    row = lastIndexOf(blank, col_to_insert)
    new[col][row] = player
    return new

# assumes there is at most one winner at any time
def get_winner(board, you, opp):
    # look for vertical win
    for col in board:
        winner = get_winner_list(col)
        if winner is not None:
            return winner
            
    num_cols, num_rows = len(board), len(board[0])

    # horizontal win
    rows = [[board[col][row] for col in range(num_cols)] for row in range(num_rows)]
    for row in rows:
        winner = get_winner_list(row)
        if winner is not None:
            return winner

    # diagonals
    # negative sloped diags all starting from the 0 row, not including 0 col
    # i.e. (1,0), (2,0) .. (num_cols - 1, 0) 
    # excluding diag starting with (0,0) cuz covered in next list
    diags = [[col[i] for i, col in enumerate(board[x:]) if i < num_rows] for x in range(1, num_cols)]

    # negative sloped diags starting in just the first column
    # i.e. starting at (0,1), (0,2) .. (0, num_rows - 1)
    d = [[col[i + j] for i, col in enumerate(board) if i < num_rows - j] for j in range(num_rows)]
    diags.extend(d)
    
    # positive sloped diags starting from the last row, not including 0 col
    # i.e. (1, n), (2, n), ... (num_cols - 1, n), where n = num_rows - 1
    # excluding diag starting with (0,n) cuz covered in next list
    d = [[col[-i - 1] for i, col in enumerate(board[x:]) if i < num_rows] for x in range(1, num_cols)]
    diags.extend(d)
    
    #positive sloped diags starting in just the first column
    # i.e. starting at (0,n), (0, n - 1) .. (0, 0), where n = num_rows - 1
    d = [[col[(-i - 1) - j] for i, col in enumerate(board) if i < num_rows - j] for j in range(num_rows)]
    diags.extend(d)
    
    for diag in diags:
        winner = get_winner_list(diag)
        if winner is not None:
            return winner

    # no winner
    return None

# checks if a list has 4 or more consecutive of a element thats not blank
def get_winner_list(l):
    import itertools
    groups = [list(g) for k, g in itertools.groupby(l)]
    for group in groups:
        if len(group) >= 4 and group[0] != blank:
            return group[0]    
    return None

def game_over(board, player, opp):
    if get_winner(board, player, opp) is not None:
        return True

    # if any empty cells, game is not over
    for col in board:
        for cell in col:
            if cell == blank:
                return False
    return True

# returns 10 if @you is the winner, -10 if @you is the loser
# and 0 otherwise (tie, or game not over)
def evaluate(board, you, opp):
    win = get_winner(board, you, opp)
    if win is None:
        return 0
    return 10 if win == you else -10
    
def repl():
    board = make_board()
    player = "X"
    opp = "O"

    from minmax_ai import AI
    ai = AI(ai_piece=opp,
            opp=player,
            depth=5,
            game_over_fun=game_over,
            eval_fun=evaluate,
            moves_fun=possible_moves,
            next_state_fun=next_state)

    print "You are X"
    print "Enter your moves as a zero-indexed col number"

    while(True):
        print
        print "Your Turn: "
        print_board(board)
        input = raw_input()
        col = int(input)
        if board[col][0] != blank:
            print "Invalid move!"
            continue        
    
        board = next_state(board, player, col)
        print_board(board)
        winner = get_winner(board, player, opp)
        if game_over(board, player, opp):
            if winner != None:
                if winner == player:
                    print "You win!"
                else:
                    print "You lose!"
            else:
                print "Draw!"
            break

        print 
        print "Their turn..."
    
        score, ai_move = ai.get_move(board)
        print ai_move
        board = next_state(board, opp, ai_move)
        print_board(board)
        winner = get_winner(board, player, opp)
    
        if game_over(board, player, opp):
            if winner != None:
                if winner == player:
                    print "You win!"
                else:
                    print "You lose!"
            else:
                print "Draw!"
            break

if __name__ == "__main__":
    repl()

