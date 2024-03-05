# Built-in python modules
import random
import time
import copy

# Pip-installed modules
import chess # pip install chess
from chess import InvalidMoveError
from ChessAI import find_best_move

def play_chess(white, black, sleeptimer):
    # Playing chess using the library https://python-chess.readthedocs.io
    print("Welcome to Group 44's Chess Game!")
    print(f"White is played by the algorithm {white.__name__}.")
    print(f"Black is played by the algorithm {black.__name__}.")
    board = chess.Board()
    while not board.is_game_over():
        print("\n"+f"{board}")
        time.sleep(sleeptimer) # Pause program briefly to give the illusion of the AI's "thinking"
        if board.turn == chess.WHITE:
            move = make_move(board, white)
            print("\n"+f"White moved: '{move}'")
        else:
            move = make_move(board, black)
            print("\n"+f"Black moved: '{move}'")
    print("\n"+f"Game Over! Results: {board.result()}")


def make_move(board, algorithm):
    # Makes 'algorithm' carry out a chess move on 'board'
    copy_of_board = copy.deepcopy(board) # Make copy so 'algorithm' can safely altar board state
    move = algorithm(copy_of_board)      # ask 'algorithm' to provide its move
    board.push(move)                     # it's assumed that a legal move was privided
    return move


def chess_ai_depth_5_playing_as_white(board):
    return find_best_move(board, 5)

def chess_ai_depth_5_playing_as_black(board):
    return find_best_move(board, 5)


def human_player(board):
    # A human player inputs their move via the terminal
    while True:
        try:
            move_str = input("\n"+"Enter your move: (Your input must be uci-format 'e2e4')"+"\n")
            move = chess.Move.from_uci(move_str)
            if move in board.legal_moves:
                return move
            else:
                print("\n"+"Invalid move. Try again!")
        except InvalidMoveError:
            print("\n"+"Invalid input. Try again!")


def ai_random_move(board):
    # AI that chooses a random move from the list of legal moves
    legal_moves = list(board.legal_moves)    # Make list of legal moves
    random_move = random.choice(legal_moves) # Randomly choose move from list
    return random_move


def ai_rush_b(board):
    # Makes the move that is the furthest towards the opponent's backline
    legal_moves = list(board.legal_moves)
    def destination_rank_as_white(move): # Sort moves based on distance to black's backline
        return chess.square_rank(move.to_square)
    def destination_rank_as_black(move): # Sort moves based on distance to white's backline
        return 8 - chess.square_rank(move.to_square)
    if board.turn == chess.WHITE:
        sorted_moves = sorted(legal_moves, key=destination_rank_as_white, reverse=True)
    else:
        sorted_moves = sorted(legal_moves, key=destination_rank_as_black, reverse=True)
    return sorted_moves[0]


# For debugging, the fastest way to end a fresh chess game is:
# f2f3 by White
# e7e6 by Black
# g2g4 by White
# d8h4 by Black (checkmate, black won)


if __name__ == "__main__":
    white_algorithm = chess_ai_depth_5_playing_as_white
    black_algorithm = ai_random_move
    sleep_time = 0.1
    play_chess(white_algorithm, black_algorithm, sleep_time)