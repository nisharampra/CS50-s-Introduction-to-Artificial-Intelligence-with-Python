# tictactoe.py

X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board (3x3 grid of EMPTY).
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    """
    Returns player who has the next turn on a board.
    X goes first.
    """
    # Count moves
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)

    # If game is over, can return anything
    if terminal(board):
        return None

    return X if x_count == o_count else O

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                moves.add((i, j))
    return moves

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    Does NOT modify original board.
    Raises Exception if action invalid.
    """
    i, j = action
    if i not in range(3) or j not in range(3):
        raise Exception("Invalid action: out of bounds")
    if board[i][j] is not EMPTY:
        raise Exception("Invalid action: cell not empty")

    # Deep copy board
    import copy
    new_board = copy.deepcopy(board)

    new_board[i][j] = player(board)  # Place current player's mark

    return new_board

def winner(board):
    """
    Returns the winner of the game (X or O), or None if no winner.
    """
    # Check rows and columns
    for i in range(3):
        # Row
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not EMPTY:
            return board[i][0]
        # Column
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] is not EMPTY:
            return board[0][i]

    # Diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not EMPTY:
        return board[0][2]

    return None

def terminal(board):
    """
    Returns True if game is over (win or tie), else False.
    """
    if winner(board) is not None:
        return True
    # If any empty cell, game not over
    for row in board:
        if EMPTY in row:
            return False
    return True  # No winner and no empty cells means tie

def utility(board):
    """
    Returns 1 if X has won, -1 if O has won, 0 if tie.
    Assumes board is terminal.
    """
    w = winner(board)
    if w == X:
        return 1
    elif w == O:
        return -1
    else:
        return 0

def minimax(board):
    """
    Returns the optimal action (i, j) for the current player on the board.
    Returns None if board is terminal.
    """

    if terminal(board):
        return None

    current_player = player(board)

    def max_value(board):
        if terminal(board):
            return utility(board), None
        v = float('-inf')
        best_move = None
        for action in actions(board):
            min_v, _ = min_value(result(board, action))
            if min_v > v:
                v = min_v
                best_move = action
                if v == 1:
                    break  # Prune: can't do better than 1
        return v, best_move

    def min_value(board):
        if terminal(board):
            return utility(board), None
        v = float('inf')
        best_move = None
        for action in actions(board):
            max_v, _ = max_value(result(board, action))
            if max_v < v:
                v = max_v
                best_move = action
                if v == -1:
                    break  # Prune: can't do better than -1
        return v, best_move

    if current_player == X:
        _, move = max_value(board)
    else:
        _, move = min_value(board)

    return move
