import chess #pip install python-chess

def evaluate_board(board):
    # Simple evaluation function that counts the material advantage of each player
    score = 0
    for piece_type in [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN]:
        score += len(board.pieces(piece_type, chess.WHITE)) - len(board.pieces(piece_type, chess.BLACK))
    return score

def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    legal_moves = list(board.legal_moves)
    if maximizing_player:
        max_eval = float('-inf')
        for move in legal_moves:
            board.push(move)
            evaluate = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, evaluate)
            alpha = max(alpha, evaluate)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in legal_moves:
            board.push(move)
            evaluate = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, evaluate)
            beta = min(beta, evaluate)
            if beta <= alpha:
                break
        return min_eval

def find_best_move(board, depth):
    best_move = None
    max_eval = float('-inf')
    alpha = float('-inf')
    beta = float('inf')
    for move in board.legal_moves:
        board.push(move)
        evaluation = minimax(board, depth - 1, alpha, beta, False)
        board.pop()
        if evaluation > max_eval:
            max_eval = evaluation
            best_move = move
    return best_move


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


    the_best_move = find_best_move(chessboard, 5)
    print("Best move:", the_best_move)
    # print(board.legal_moves.count())
