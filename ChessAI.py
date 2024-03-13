import chess #pip install python-chess

moveNumber = 0

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

VALUE = {
    chess.PAWN: 100,
    chess.KNIGHT: 300,
    chess.BISHOP: 300,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 400000,
}


def evaluate_board(board):
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
        # Giving value to material left and placement on the board
        for square in piece_map:
            if color_at(square) == is_white:
                score += VALUE[piece_type_at(square)]
                score += PIECE_SQUARE[piece_type_at(square)][square]          
            else:
                score -= VALUE[piece_type_at(square)]
                score -= PIECE_SQUARE[piece_type_at(square)][63-square] 
        return score


def minimax(board, depth, alpha, beta, maximizing_player, playing_as_white):
    global moveNumber
    if depth == 0 or board.is_game_over():
        if board.is_checkmate():
            if maximizing_player == playing_as_white:
                return -9999  # Checkmate; worst score for player evaluating as white
            else:
                return 9999  # Checkmate; best score if not evaluating as white
        elif board.is_stalemate() or board.is_insufficient_material() or board.can_claim_draw():
            return 0  # Draw conditions
        else:  # Unclear outcome, use the evaluation
            return evaluate_board(board, playing_as_white)

    legal_moves = list(board.legal_moves)
    if maximizing_player:
        max_eval = float('-inf')

        for move in legal_moves:
            board.push(move)
            evaluate = minimax(board, depth - 1, alpha, beta, False, playing_as_white)
            evaluate = minimax(board, depth - 1, alpha, beta, False, playing_as_white)
            board.pop()
            max_eval = max(max_eval, evaluate)
            alpha = max(alpha, evaluate)
            moveNumber += 1
            if beta <= alpha:
                break

        return max_eval
    else:
        min_eval = float('inf')

        for move in legal_moves:
            board.push(move)
            evaluate = minimax(board, depth - 1, alpha, beta, True, playing_as_white)
            evaluate = minimax(board, depth - 1, alpha, beta, True, playing_as_white)
            board.pop()
            min_eval = min(min_eval, evaluate)
            beta = min(beta, evaluate)
            moveNumber += 1
            if beta <= alpha:
                break
            
        return min_eval


def find_best_move_basic(board, depth, playing_as_white):
    global moveNumber
    moveNumber = 0
    best_move = None
    max_eval = float('-inf')
    alpha = float('-inf')
    beta = float('inf')
    index = 0

    for move in board.legal_moves:
        index += 1
        index += 1
        board.push(move)
        evaluation = minimax(board, depth - 1, alpha, beta, False, playing_as_white)
        evaluation = minimax(board, depth - 1, alpha, beta, False, playing_as_white)
        board.pop()

        if evaluation > max_eval:
            max_eval = evaluation
            best_move = move

        moveNumber += 1
    print(f"Number of moves: {moveNumber}, best move: {best_move}, max eval: {max_eval}")
    return best_move

def print_evaluation(evaluation, move, playing_as_white, move_index, total_moves):
    if playing_as_white:
        player_name = "White"
    else:
        player_name = "Black"
    print(f"({move_index}/{total_moves}) {player_name}'s move '{move}' evaluates to material gain = {evaluation}", end="\r")


def print_evaluation(evaluation, move, playing_as_white, move_index, total_moves):
    if playing_as_white:
        player_name = "White"
    else:
        player_name = "Black"
    print(f"({move_index}/{total_moves}) {player_name}'s move '{move}' evaluates to material gain = {evaluation}", end="\r")