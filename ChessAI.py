import chess #pip install python-chess

def evaluate_board(board, playing_as_white):
    # Improved evaluation with approximate piece values
    piece_values = {
        chess.PAWN:   1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK:   5,
        chess.QUEEN:  9,
    }
    score = 0
    for piece_type, value in piece_values.items():
        if playing_as_white:
            score += len(board.pieces(piece_type, chess.WHITE)) * value
            score -= len(board.pieces(piece_type, chess.BLACK)) * value
        else:
            score += len(board.pieces(piece_type, chess.BLACK)) * value
            score -= len(board.pieces(piece_type, chess.WHITE)) * value
    return score

def minimax(board, depth, alpha, beta, maximizing_player, playing_as_white):
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
            evaluate = minimax(board, depth - 1, alpha, beta, True, playing_as_white)
            board.pop()
            min_eval = min(min_eval, evaluate)
            beta = min(beta, evaluate)
            if beta <= alpha:
                break
        return min_eval

def find_best_move(board, depth, playing_as_white, print_each_move_evaluation):
    best_move = None
    max_eval = float('-inf')
    alpha = float('-inf')
    beta = float('inf')
    index = 0
    for move in board.legal_moves:
        index += 1
        board.push(move)
        evaluation = minimax(board, depth - 1, alpha, beta, False, playing_as_white)
        board.pop()
        if evaluation > max_eval:
            max_eval = evaluation
            best_move = move
        if print_each_move_evaluation:
            print_evaluation(evaluation, move, playing_as_white, index, len(list(board.legal_moves)))
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
    the_best_move = find_best_move(chessboard, 5, play_as_white, print_each_move_eval)
    print("Best move:", the_best_move)
    # print(board.legal_moves.count())
