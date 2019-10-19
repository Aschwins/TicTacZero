import numpy as np
from tictaczero.board import Board, CROSS, CIRCLE

def play_a_game(Player1, Player2, print_result = False):
    """
    Function which plays a game of tic tac toe between two players.
    Returns: board_history
    """
    board = Board(3)
    p1 = Player1(side=CROSS)
    p2 = Player2(side=CIRCLE)
    
    board_history = np.zeros(shape=(1,9), dtype=np.int32)
    ongoing = True
    
    while ongoing:
        for p in [p1, p2]:
            boardstate, winner, game_ended = p.move(board)
            board_history = np.concatenate((board_history, [boardstate]), axis = 0)
            if game_ended:
                ongoing = False
                result = np.full(shape=(len(board_history), 1), fill_value = winner)
                board_history = np.concatenate((board_history, result), axis = 1)
                break
    
    if print_result:
        print(f"Game won by {winner}")
        board.print_board()
        
    return board_history