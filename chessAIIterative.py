import chess
import time
import random

# Class that modifies dict to return -1 if key is not found in dict
class DefaultDict(dict):
    def __missing__(self, key):
        return -1
    
# Transposition table to store evaluated board positions
transposition_table = {}
# transposition_table = {}
moveNumber = 0

# Generates a Random number from 0 to 2^64-1
def randomInt():
    return random.randint(0, pow(2, 64)-1)

# Initializes the table
def initTable():
    # 8x8x12 array
    return [[[randomInt() for k in range(12)] for j in range(8)] for i in range(8)]

zTable = initTable()

# This dict associates each piece with a number
PIECE_TO_NUMBER_init = {
    'P': 0,
    'N': 1,
    'B': 2,
    'R': 3,
    'Q': 4,
    'K': 5,
    'p': 6,
    'n': 7,
    'b': 8,
    'r': 9,
    'q': 10,
    'k': 11
}

PIECE_TO_NUMBER = DefaultDict(PIECE_TO_NUMBER_init)

# Computes the hash value from a FEN string
def computeHashFromFEN(fen, ZobristTable):
    board = fen.split(' ')[0] # Extract the board part of the FEN
    hash = 0
    row = 0
    col = 0
    for char in board:
        if char == '/':
            row += 1
            col = 0
        elif char.isdigit():
            col += int(char)
        else:
            piece = PIECE_TO_NUMBER[char]
            if piece != -1:
                hash ^= ZobristTable[row][col][piece]
            col += 1
    return hash

# Bonus for each piece being in certain locations on the board
PIECE_SQUARE = {

    chess.PAWN: [
          0,  0,  0,  0,  0,  0,  0,  0,
          5, 10, 10,-20,-20, 10, 10,  5,
          5, -5,-10,  0,  0,-10, -5,  5,
          0,  0,  0, 20, 20,  0,  0,  0,
          5,  5, 10, 25, 25, 10,  5,  5,
         10, 10, 20, 30, 30, 20, 10, 10,
         50, 50, 50, 50, 50, 50, 50, 50,
          0,  0,  0,  0,  0,  0,  0,  0,
    ],

    chess.KNIGHT: [
        -50,-40,-30,-30,-30,-30,-40,-50,
        -40,-20,  0,  5,  5,  0,-20,-40,
        -30,  5, 10, 15, 15, 10,  5,-30,
        -30,  0, 15, 20, 20, 15,  0,-30,
        -30,  5, 15, 20, 20, 15,  5,-30,
        -30,  0, 10, 15, 15, 10,  0,-30,
        -40,-20,  0,  0,  0,  0,-20,-40,
        -50,-40,-30,-30,-30,-30,-40,-50,
    ],

    chess.BISHOP: [
        -20,-10,-10,-10,-10,-10,-10,-20,
        -10,  5,  0,  0,  0,  0,  5,-10,
        -10, 10, 10, 10, 10, 10, 10,-10,
        -10,  0, 10, 10, 10, 10,  0,-10,
        -10,  5,  5, 10, 10,  5,  5,-10,
        -10,  0,  5, 10, 10,  5,  0,-10,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -20,-10,-10,-10,-10,-10,-10,-20,
    ],

    chess.ROOK:[
          0,  0,  0,  5,  5,  0,  0,  0,
         -5,  0,  0,  0,  0,  0,  0, -5,
         -5,  0,  0,  0,  0,  0,  0, -5,
         -5,  0,  0,  0,  0,  0,  0, -5,
         -5,  0,  0,  0,  0,  0,  0, -5,
         -5,  0,  0,  0,  0,  0,  0, -5,
          5, 10, 10, 10, 10, 10, 10,  5,
          0,  0,  0,  0,  0,  0,  0,  0,
    ],

    chess.QUEEN: [
        -20,-10,-10, -5, -5,-10,-10,-20,
        -10,  0,  5,  0,  0,  0,  0,-10,
        -10,  5,  5,  5,  5,  5,  0,-10,
          0,  0,  5,  5,  5,  5,  0, -5,
         -5,  0,  5,  5,  5,  5,  0, -5,
        -10,  0,  5,  5,  5,  5,  0,-10,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -20,-10,-10, -5, -5,-10,-10,-20,
    ],

    chess.KING: [
         20, 30, 10,  0,  0, 10, 30, 20,
         20, 20,  0,  0,  0,  0, 20, 20,
        -10,-20,-20,-20,-20,-20,-20,-10,
        -20,-30,-30,-40,-40,-30,-30,-20,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
    ],
}

# Standard values for chess pieces, multiplied by 100
VALUE = {
    chess.PAWN: 100,
    chess.KNIGHT: 300,
    chess.BISHOP: 300,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 400000,  # Random very large value for the king
}

def evaluate_board(board, playing_as_white):
        """
        Evaluates the value of the board based on fixed piece valuations
        """
        score = 0
        # Giving value for checkmating and checking opponent
        score += board.is_checkmate()*VALUE[chess.KING]   
        score += board.is_check()*10  

        piece_map = board.piece_map()
        piece_type_at = board.piece_type_at
        color_at = board.color_at
        is_white = chess.WHITE

        color_correction = 1 if playing_as_white else -1
        # Giving value to material left and placement on the board
        for square in piece_map:
            if color_at(square) == is_white:
                score += VALUE[piece_type_at(square)]
                score += PIECE_SQUARE[piece_type_at(square)][square]          
            else:
                score -= VALUE[piece_type_at(square)]
                score -= PIECE_SQUARE[piece_type_at(square)][63-square] 
        return color_correction * score
    
def minimax(board, depth, alpha, beta, maximizing_player, playing_as_white):

    if depth == 0 or board.is_game_over():
        score = evaluate_board(board, playing_as_white)
        return score
    
    transposition_key = computeHashFromFEN(board.fen(), zTable)
    
    if transposition_key in transposition_table:
        entry = transposition_table[transposition_key]
    else:
        transposition_table[transposition_key] = {}
        entry = transposition_table[transposition_key]

    global moveNumber
    moves = order_moves(board, maximizing_player)

    if maximizing_player:
        max_eval = float('-inf')
        for move in moves:
            moveNumber += 1
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False, playing_as_white)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        score = max_eval
    else:
        min_eval = float('inf')
        for move in moves:
            moveNumber += 1
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, True, playing_as_white)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        score = min_eval

    entry.update({move: depth+1})
    
    return score
    
def order_moves(board, maximizing_player):
    moves = board.legal_moves
    transposition_key = computeHashFromFEN(board.fen(), zTable)
    entry = transposition_table[transposition_key]
    scored_moves = []

    for move in moves:
        
        score = 0
        move_from = move.from_square
        move_to = move.to_square
        
        if board.is_capture(move) and not board.is_en_passant(move):
            score += 10 + (VALUE[board.piece_type_at(move_to)] - VALUE[board.piece_type_at(move_from)]) / 100

        if maximizing_player:
            score += PIECE_SQUARE[board.piece_type_at(move_from)][move_to] - PIECE_SQUARE[board.piece_type_at(move_from)][move_from]
        else:
            score += PIECE_SQUARE[board.piece_type_at(move_from)][63-move_to] - PIECE_SQUARE[board.piece_type_at(move_from)][63-move_from]

        if move.promotion:
            score += 800
        score += board.gives_check(move)*10

        if move in entry:
            score += 10

        scored_moves.append((score, move))
    return [move for _, move in sorted(scored_moves, reverse=True, key=lambda x: x[0])]

def find_best_move_iterative(board, max_depth, playing_as_white):

    global moveNumber
    moveNumber = 0
    alpha = float('-inf')
    beta = float('inf')
    transposition_key = computeHashFromFEN(board.fen(), zTable)

    if transposition_key not in transposition_table:
        transposition_table[transposition_key] = {}

    for depth in range(1, max_depth + 1):
        max_eval = float('-inf')
        moves = order_moves(board, True)

        for move in moves:
            board.push(move)
            evaluation = minimax(board, depth - 1, alpha, beta, False, playing_as_white)
            board.pop()

            if evaluation > max_eval:
                max_eval = evaluation
                best_move = move

            moveNumber += 1

    print(f"Move number: {moveNumber}, move: {best_move}, score {max_eval}")
    return best_move
