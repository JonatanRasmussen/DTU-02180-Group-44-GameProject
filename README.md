This is the readme fpr DTU-02180-Group-44-GameProject.

The zip-file should be extracted and the Python-chess library should be installed using the command:

pip install chess

The program is run from the file "play_chess.py". One of three AI's can be selected: one using only alpha-beta pruning, one adding move ordering to this, and one also using iterative deepening with move ordering. In the main function, comment the chosen AI in and choose human player as black algorithm. For the recommended playable AI this will look like:

 ######################### Chose white player ##############################
    # AIs:
    #white_algorithm = chess_ai_basic_white
    white_algorithm = chess_ai_ordering_white
    #white_algorithm = chess_ai_iterative_white

    # Human or random:
    #white_algorithm = ai_random_move
    #white_algorithm = human_player

    ######################### Chose black player ##############################
    # AIs:
    #black_algorithm = chess_ai_basic_black
    #black_algorithm = chess_ai_ordering_black
    #black_algorithm = chess_ai_iterative_black
    
    # Human or random:
    #black_algorithm = ai_random_move
    black_algorithm = human_player

    sleep_time = 0
    play_chess(white_algorithm, black_algorithm, sleep_time)
    #test_AI(white_algorithm, black_algorithm, sleep_time)

Finally, the script can be run, and the game is played in the terminal. A chess board is numbered with column a being left and h to the right, while row number 1 is down and 8 is up. With this, the move is played in the style "from square to square. So moving from the left pawn for right two squares up would be "a2a4".