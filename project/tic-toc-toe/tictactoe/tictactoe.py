"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # Any return value is acceptable if a terminal board is provided as input (i.e., the game is already over).
    if terminal(board):
        return None

    # X takes the first，if the num of existed player is not equal then player should be O
    count_X = 0
    count_O = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                count_X += 1
            elif board[i][j] == O:
                count_O += 1
    if count_X == count_O:
        return X
    return O                    
         



def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # Any return value is acceptable if a terminal board is provided as input (i.e., the game is already over).
    if terminal(board):
        return None
    actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] is EMPTY:
                actions.add((i, j))            
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i = action[0]
    j = action[1]
    if board[i][j] is not EMPTY:
        raise ValueError
    # Deep copy for the following recursion    
    board_copy = copy.deepcopy(board)
    board_copy[i][j] = player(board)
    return board_copy
   


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check the horizontal win 
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != EMPTY:
            return board[i][0]

    # Check the vertical win        
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != EMPTY:
            return board[0][i]

    # check the diagonal win
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[1][1] != EMPTY:
        return board[1][1]

    # No winner
    return None             

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    is_fill = True
    for i in range(3):
        for j in range(3):
            if board[i][j] is EMPTY:
                is_fill = False
    
    if winner(board) != None or is_fill == True:
        return True
    return False    


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0    


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # Below are helper function
    def max_value(board, alpha, beta):
        if terminal(board):
            # Use none for taking up a place
            return utility(board), None 
        possible_actions = actions(board)    
        max_score = -math.inf
        best_action = None
        for action in possible_actions:
            # the min value opponents would take after the action
            value, temp = min_value(result(board, action), alpha, beta) 
            if value > max_score:
                max_score = value
                best_action = action    
            alpha = max(alpha, max_score)
            # alpha beta pruning
            if beta <= alpha:
                break    
        return max_score, best_action

    # mutual recursion
    def min_value(board, alpha, beta):
        if terminal(board):
            # use _ for taking up a place
            return utility(board), None 
        porssible_actions = actions(board)    
        min_score = math.inf
        best_action = None
        for action in porssible_actions:
            # the max value opponents would take after the action 
            value, temp = max_value(result(board, action), alpha, beta) 
            if value < min_score:
                min_score = value
                best_action = action
            beta = min(beta, min_score)    
            # alpha beta pruning
            if beta <= alpha:
                break    
        return min_score, best_action

    # return min or max according to the current player
    current_player = player(board)
    if current_player == X:
        value, move = max_value(board, -math.inf, math.inf)
        return move
    else:
        value, move = min_value(board, -math.inf, math.inf)
        return move   



        
    
