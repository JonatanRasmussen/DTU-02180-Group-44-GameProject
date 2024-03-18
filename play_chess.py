# Built-in python modules
import random
import time
import copy

# Pip-installed modules
import chess # pip install chess
from chess import InvalidMoveError
from ChessAIBasic import find_best_move_basic
from chessAIOrdering import find_best_move_ordering
from chessAIIterative import find_best_move_iterative
#from IT2 import find_best_move_iterative


FEN_STRINGS = ['r4rk1/pp2bppp/3q4/2p1n3/3p4/1P3P2/1PP1B1PP/R1BQ1RK1 w - c6 0 16',
               'r1bqk1nr/pppp1ppp/2n5/4p2Q/1bB1P3/8/PPPP1PPP/RNB1K1NR w KQkq - 4 4',
               'r1bq1rk1/pp3ppp/2nb4/2pN4/3p4/6P1/PPPP1PBP/R1BQ1RK1 w - - 3 11',
               '4r1k1/pq3ppp/4b3/2p5/3p1BP1/3P3P/PPn2PB1/2R3K1 w - - 0 23',
               '1rr1b1k1/q3bpp1/pp1ppnnp/8/2P1PP2/N1N1B1PP/PP3QBK/2RR4 w - - 2 20']

def play_chess(white, black, sleeptimer):
    # Playing chess using the library https://python-chess.readthedocs.io
    print("Welcome to Group 44's Chess Game!")
    print(f"White is played by the algorithm {white.__name__}.")
    print(f"Black is played by the algorithm {black.__name__}.")
    
    board = chess.Board()

    while not board.is_game_over():
        print("\n"+f"{board}"+"\n")
        time.sleep(sleeptimer) # Pause program briefly to give the illusion of the AI's "thinking"

        if board.turn == chess.WHITE:
            move = make_move(board, white)
            print("\n"+f"White moved: '{move}'")
        else:
            move = make_move(board, black)
            print("\n"+f"Black moved: '{move}'")

    print("\n"+f"Game Over! Results: {board.result()}")
    return board.result()

def test_AI(white, black, sleeptimer):
    # Playing chess using the library https://python-chess.readthedocs.io
    print("Welcome to Group 44's Chess Game!")
    print(f"White is played by the algorithm {white.__name__}.")
    print(f"Black is played by the algorithm {black.__name__}.")
    startTime = time.time()
    for i in range(len(FEN_STRINGS)):
        board = chess.Board(FEN_STRINGS[i])
        print(board)
        move = make_move(board, white)
        print("\n"+f"White moved: '{move}'")
    print(f"Finished in : {time.time() - startTime} seconds")
    return board.result()


def make_move(board, algorithm):
    # Makes 'algorithm' carry out a chess move on 'board'
    copy_of_board = copy.deepcopy(board) # Make copy so 'algorithm' can safely altar board state
    move = algorithm(copy_of_board)      # ask 'algorithm' to provide its move
    board.push(move)                     # it's assumed that a legal move was privided
    return move


def chess_ai_basic_white(board):
    depths = 4
    playing_as_white = True
    return find_best_move_basic(board, depths, playing_as_white)

def chess_ai_ordering_white(board):
    depths = 4
    playing_as_white = True
    return find_best_move_ordering(board, depths, playing_as_white)

def chess_ai_iterative_white(board):
    depths = 4
    playing_as_white = True
    return find_best_move_iterative(board, depths, playing_as_white)

def chess_ai_basic_black(board):
    depths = 4
    playing_as_white = False
    return find_best_move_basic(board, depths, playing_as_white)

def chess_ai_ordering_black(board):
    depths = 4
    playing_as_white = False
    return find_best_move_ordering(board, depths, playing_as_white)

def chess_ai_iterative_black(board):
    depths = 4
    playing_as_white = False
    return find_best_move_iterative(board, depths, playing_as_white)


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


if __name__ == "__main__":
    ######################### Chose white player ##############################
    # AIs:
    #white_algorithm = chess_ai_basic_white
    #white_algorithm = chess_ai_ordering_white
    white_algorithm = chess_ai_iterative_white

    # Human or random:
    #white_algorithm = ai_random_move
    #white_algorithm = human_player

    ######################### Chose black player ##############################
    # AIs:
    #black_algorithm = chess_ai_basic_black
    #black_algorithm = chess_ai_ordering_black
    #black_algorithm = chess_ai_iterative_black
    
    # Human or random:
    black_algorithm = ai_random_move
    #black_algorithm = human_player

    sleep_time = 0
    #play_chess(white_algorithm, black_algorithm, sleep_time)
    test_AI(white_algorithm, black_algorithm, sleep_time)