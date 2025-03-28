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

    # Count the number of X and O in the current board
    count_X = sum(row.count("X") for row in board)
    count_O = sum(row.count("O") for row in board)

    # The next player will be "O" if count_X > count_O, 
    # otherwise it will be "X"
    next_player = "O" if count_X > count_O else "X"

    return next_player


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    # Get the index set of all empty cells, which are all possible actions
    actions_all = set(
        (i,j) 
        for i, row in enumerate(board) 
        for j, cell in enumerate(row) 
        if cell is None
    )

    return actions_all

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    
    # Copy the input board
    new_board = copy.deepcopy(board)

    # Get the i-index and j-index of the cell to be changed
    i, j = action

    # Check if the action is out-of-bounds
    if not (0 <= i < len(board) and 0 <= j < len(board[0])):
        raise ValueError(f"Action {action} is out-of-bounds.")

    # If the cell is already occupied, raise an error    
    if new_board[i][j] is not None:
        raise ValueError("This is not a valid action!")
    
    # Let the player make the move at this cell
    else:
        new_board[i][j] = player(board)

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # Determin the size of board
    size_N = len(board)
    
    # Replace 'X' with 1, 'O' with -1, and None with 0
    number_board = [[1 if cell == "X" else -1 if cell == "O" else 0 for cell in row] for row in board]

    # Check rows of number_board
    if any(sum(row) == size_N for row in number_board): return "X"
    if any(sum(row) == -size_N for row in number_board): return "O"

    # Transpose the board to check columns using rows
    transposed_board = list(zip(*number_board))

    # Check columns (now rows in transposed_board)
    if any(sum(row) == size_N for row in transposed_board): return "X"
    if any(sum(row) == -size_N for row in transposed_board): return "O"

    # Check diagonals
    if sum(number_board[i][i] for i in range(size_N)) == size_N or sum(number_board[i][size_N-1-i] for i in range(size_N)) == size_N:
        return "X"
    if sum(number_board[i][i] for i in range(size_N)) == -size_N or sum(number_board[i][size_N-1-i] for i in range(size_N)) == -size_N:
        return "O"

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    # If there's a winner, terminal the game
    if winner(board) is not None:
        return True
    
    # If the board is full, i.e. no empty cell left, terminal the game
    if all(cell is not None for row in board for cell in row):
        return True
    
    # Otherwise, game is still ongoing
    return False  


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    
    if terminal(board):
        return 1 if winner(board) == "X" else -1 if winner(board) == "O" else 0
    else:
        raise ValueError("The game is not terminated.")


def max_value(board):
    """
    Returns the maximum value for the player "X".
    """

    # If it's a terminal board, return the utility score
    if terminal(board):
        return utility(board)
    
    v = float('-inf')

    # Iterate through all possible actions
    # Maximize the minimum score from the opponent's move
    for action1 in actions(board):
        v = max(v, min_value(result(board, action1)))
    
    return v

def min_value(board):
    """
    Returns the minimal value for the player "O".
    """

    # If it's a terminal board, return the utility score
    if terminal(board):
        return utility(board)
    
    v = float('inf')
    
    # Iterate through all possible actions
    #  Minimize the maximum score from the opponent's move
    for action1 in actions(board):
        v = min(v, max_value(result(board, action1)))
    
    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    
    # If it is a terminal board, return None
    if terminal(board):
        return None
    
    # Get all possible actions of the player
    all_actions = actions(board)

    # Determinr who the player is
    the_player = player(board)  

    # Initialize best_score based on the player's turn
    if the_player == "X":
        best_score = float('-inf')  # Maximizing player (X)
    else:
        best_score = float('inf')   # Minimizing player (O)

    optimal_action = None

    # Iterate through all possible actions 
    for action1 in all_actions:

        # Get the new board after the action1
        new_board = result(board, action1)

        if the_player == "X":

            # Maximize the minimum value from the opponent's move
            score1 = min_value(new_board)            

            # If the score is higher, update the best score and optimal action
            if score1 > best_score:
                best_score = score1
                optimal_action = action1

        elif the_player == "O":

            # Minimize the maximum value from the player's move
            score1 = max_value(new_board)

            # If the score is lower, update the best score and optimal action
            if score1 < best_score:
                best_score = score1
                optimal_action = action1

    return optimal_action

