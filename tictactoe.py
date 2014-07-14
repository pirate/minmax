# an implementation for tictactoe AI using minmax and alphabeta pruning
# board array access is board[col][row]

# boards are always squares
def make_board(width):
    return [["_"] * width for _ in xrange(width)]
        
# board is a list of columns and we want to print by row
def print_board(board):
    for i in xrange(len(board)):
        row = [board[j][i] for j in xrange(len(board))]
        print " | ".join(row)
      
def possible_moves(board):  
    d = len(board)
    return [(y,x) for y in xrange(d) for x in xrange(d) if board[y][x] == "_"]

# create a new board but with position @(col, row) changed to @player
def next_state(old, player, (col,row)):
    import copy
    new = copy.deepcopy(old)
    new[col][row] = player
    return new

def get_winner(board):
    # look for vertical win
    for col in board:
        if len(set(col)) == 1 and col[0] != "_":
            return col[0]
            
    # horizontal win
    d = len(board)
    rows = [[board[i][x] for i in xrange(d)] for x in xrange(d)]
    for row in rows:
        if len(set(row)) == 1 and row[0] != "_":
            return row[0]
            
    # diagonal win: top left to bottom right
    tl_br_diag = [col[i] for i,col in enumerate(board)]
    if len(set(tl_br_diag)) == 1 and tl_br_diag[0] != "_":
        return tl_br_diag[0]

    # bottom left to top right
    bl_tr_diag = [col[-i - 1] for i,col in enumerate(board)]
    if len(set(bl_tr_diag)) == 1 and bl_tr_diag[0] != "_":
        return bl_tr_diag[0]
    
    # no winner
    return None

def game_over(board, player, opp):
    if get_winner(board) is not None:
        return True

    for col in board:
        for cell in col:
            if cell == "_":
                return False
    return True

# returns 10 if @you is the winner, -10 if @you is the loser
# and 0 otherwise (tie, or game not over)
def evaluate(board, you, _):
    win = get_winner(board)
    if win is None:
        return 0
    return 10 if win == you else -10
                
# doesn't do any error handling of bad input
def repl():
    board = make_board(3)
    from minmax_ai import AI
    ai = AI(ai_piece="o",
            opp="x",
            depth=9,
            game_over_fun=game_over,
            eval_fun=evaluate,
            moves_fun=possible_moves,
            next_state_fun=next_state)
    
    print "You are X"
    print "Enter your moves as: col row"
    while(True):
        print
        print "Your Turn: "
        print_board(board)
        input = raw_input()
        y, x = map(int, input.split())
        if board[y][x] != "_":
            print "Invalid move!"
            continue        
    
        board = next_state(board, "x", (y,x))
        print
        print_board(board)
    
        winner = get_winner(board)
        if game_over(board, "x", "o"):
            if winner != None:
                if winner == "x":
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
        board = next_state(board, "o", ai_move)
        print_board(board)

        winner = get_winner(board)
    
        if game_over(board, "x", "o"):
            if winner != None:
                if winner == "x":
                    print "You win!"
                else:
                    print "You lose!"
            else:
                print "Draw!"
            break

if __name__ == "__main__":
    repl()
