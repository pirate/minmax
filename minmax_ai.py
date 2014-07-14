# an instance of AI generates the best possible move given a current game state
# Minmax requires four functions:
# - a static evaluation function for "scoring" a given state; @eval_fun
# - a function determining if a game is over; @game_over_fun
# - a function to generate all possible moves given a state; @moves_fun
# - a function to generate a new state given an old state, the player whose turn it is, and the move; @next_state_fun
class AI:
    def __init__(self, ai_piece, opp, depth,
                 game_over_fun, eval_fun, moves_fun, next_state_fun):
        self.piece = ai_piece
        self.opp = opp
        self.depth = depth
        self.game_over = game_over_fun
        self.evaluate = eval_fun
        self.possible_moves = moves_fun
        self.next_state = next_state_fun
        
    def get_move(self, board):
        return self._minmax(board=board, player=self.piece, opp=self.opp, 
                           curr=self.piece, depth=self.depth,
                           alpha=-float("inf"), beta=float("inf"))
        
    def _minmax(self, board, player, opp, curr, depth, alpha, beta):
        if self.game_over(board, player, opp) or depth < 0:
            score = self.evaluate(board, player, opp)
            return (score, None)

        moves = self.possible_moves(board)
    
        move_to_return = None
        for move in moves:
            ns = self.next_state(board, curr, move)
            score, _ = self._minmax(ns, 
                                    player,
                                    opp,
                                    curr=opp if curr == player else player,
                                    depth= depth - 1,
                                    alpha=alpha, 
                                    beta=beta)

            # alpha beta pruning
            if curr == player:
                if score > alpha:
                    alpha = score
                    move_to_return = move
                if alpha >= beta:
                    break
            else:
                if score < beta:
                    beta = score
                if alpha >= beta:
                    break
    
        # return either max or min, respectively
        if curr == player:
            return (alpha, move_to_return)
        else:
            return (beta, None)
