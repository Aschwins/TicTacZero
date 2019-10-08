from tictaczero.board import Board

class BasePlayer:
    """
    A Base tic-tac-toe player.
    """
    def __init__(self, side = None):
        self.side = side
    
    def move(self):
        """
        A move method to make a move on a board.
        """
        pass
    
    def new_game(self, side: int):
        """
        Starts a new_game for a player with a side.
        """
        pass


class RandomPlayer(BasePlayer):
    """
    A RandomPlayer of a tic tac toe game.
    side: in [1, 2]
    board: Boardobject
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def move(self, board):
        _, res, finished = board.move(board.random_empty_square(), self.side)
        return _, res, finished
        