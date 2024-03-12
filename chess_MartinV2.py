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
        utility = 0
        for square in board.piece_map():

            if board.color_at(square) == chess.WHITE:
                utility += VALUE[board.piece_type_at(square)]
                utility += PIECE_SQUARE[board.piece_type_at(square)][square]
                utility += board.is_checkmate()*VALUE[chess.KING]
            else:
                utility -= VALUE[board.piece_type_at(square)]
                utility -= list(reversed(PIECE_SQUARE[board.piece_type_at(square)]))[square]
                utility -= board.is_checkmate()*VALUE[chess.KING]

        return utility

def order_moves(board, maximizing_player):
    moves = board.legal_moves
    scored_moves = []
    for move in moves:
        score = 0
       
        if board.is_capture(move) and not board.is_en_passant(move):
            score += 10 + (VALUE[board.piece_type_at(move.to_square)] - VALUE[board.piece_type_at(move.from_square)]) / 100
        if move.promotion:
            score += 800
        
        if maximizing_player:
            score += PIECE_SQUARE[board.piece_type_at(move.from_square)][move.to_square] - PIECE_SQUARE[board.piece_type_at(move.from_square)][move.from_square]
        else:
            score += PIECE_SQUARE[board.piece_type_at(move.from_square)][63-move.to_square] - PIECE_SQUARE[board.piece_type_at(move.from_square)][63-move.from_square]
        
        scored_moves.append((score, move))

    # Sort moves based on the scores in descending order
    scored_moves.sort(reverse=True, key=lambda x: x[0])
    return [move for _, move in scored_moves]

def minimax(board, depth, alpha, beta, maximizing_player, playing_as_white):
    global moveNumber
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    if maximizing_player:
        max_eval = float('-inf')
        moves = order_moves(board, False)
        for move in moves:
            board.push(move)
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
        moves = order_moves(board, True)
        for move in moves:
            board.push(move)
            evaluate = minimax(board, depth - 1, alpha, beta, True, playing_as_white)
            board.pop()
            min_eval = min(min_eval, evaluate)
            beta = min(beta, evaluate)
            moveNumber += 1
            if beta <= alpha:
                break
        return min_eval

def find_best_moveV2(board, depth, playing_as_white):
    global moveNumber
    moveNumber = 0
    best_move = None
    max_eval = float('-inf')
    alpha = float('-inf')
    beta = float('inf')
    index = 0
    moves = order_moves(board, True)
    for move in moves:
        index += 1
        board.push(move)
        evaluation = minimax(board, depth - 1, alpha, beta, False, playing_as_white)
        board.pop()
        if evaluation > max_eval:
            max_eval = evaluation
            best_move = move
        print_evaluation(evaluation, move, playing_as_white, index, len(list(board.legal_moves)))
        moveNumber += 1
    print(f"Number of moves: {moveNumber}")
    return best_move

def print_evaluation(evaluation, move, playing_as_white, move_index, total_moves):
    if playing_as_white:
        player_name = "White"
    else:
        player_name = "Black"
    print(f"({move_index}/{total_moves}) {player_name}'s move '{move}' evaluates to material gain = {evaluation}", end="\r")


if __name__ == "__main__":
    # Initialize chess board
    chessboard = chess.Board()
    print(chessboard)
    print("\n")

    # Do some moves to generate a position
    chessboard.push_san("e4")
    chessboard.push_san("e5")
    chessboard.push_san("Qh5")
    chessboard.push_san("Nc6")
    chessboard.push_san("Bc4")

    print("Current turn:", "White" if chessboard.turn == chess.WHITE else "Black")
    print(chessboard)

    play_as_white = True
    print_each_move_eval = True
    the_best_move = find_best_move(chessboard, 5, play_as_white)
    print("Best move:", the_best_move)
    # print(board.legal_moves.count())