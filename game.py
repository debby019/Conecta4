import numpy as np

ROWS = 6
COLS = 7

PLAYER = 1
AGENT = 2

def create_board():
    return np.zeros((ROWS, COLS), dtype=int)

def drop_piece(board, col, player):
    for r in range(ROWS):
        if board[r][col] == 0:
            board[r][col] = player
            return True
    return False

def get_valid_moves(board):
    return [c for c in range(COLS) if board[ROWS-1][c] == 0]

def is_full(board):
    return len(get_valid_moves(board)) == 0

def check_winner(board, player):

    for r in range(ROWS):
        for c in range(COLS-3):
            if all(board[r][c+i] == player for i in range(4)):
                return True

    for c in range(COLS):
        for r in range(ROWS-3):
            if all(board[r+i][c] == player for i in range(4)):
                return True

    for r in range(ROWS-3):
        for c in range(COLS-3):
            if all(board[r+i][c+i] == player for i in range(4)):
                return True

    for r in range(3, ROWS):
        for c in range(COLS-3):
            if all(board[r-i][c+i] == player for i in range(4)):
                return True

    return False