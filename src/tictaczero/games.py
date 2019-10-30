import numpy as np
from tictaczero.board import Board, CROSS, CIRCLE
from tictaczero.player import BrainPlayer

def play_a_game(Player1, Player2, print_result = False):
    """
    Function which plays a game of tic tac toe between two players.
    Returns: board_history
    """
    board = Board(3)
    
    board_history = np.zeros(shape=(1,9), dtype=np.int32)
    ongoing = True
    
    while ongoing:
        for p in [Player1, Player2]:
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


def play_n_brainy_games(n_games=100):
    """
    Plays n games and returns both (hopefully) smarter players.
    """
    player1 = BrainPlayer(side=CROSS)
    player2 = BrainPlayer(side=CIRCLE)
    board = Board(3)
    
    board_history = np.empty(shape = (9,10), dtype = np.int32)
    
    for i in range(n_games):
        board_history.fill(0)
        board.reset()
        n_moves = 0
        ongoing = True
        
        while ongoing:
            for p in [player1, player2]:
                boardstate, winner, game_ended = p.move(board)
                board_history[n_moves, :9] = boardstate
                n_moves += 1
                
                if game_ended:
                    ongoing = False
                    board_history[0:n_moves, 9] = winner
                    break
                    
                
        player1.memorize(board_history[0:n_moves, :])
        player2.memorize(board_history[0:n_moves, :])
                    
    return player1, player2

