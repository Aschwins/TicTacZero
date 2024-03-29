import numpy as np

# Squarestates
EMPTY = 0
CROSS = 1
CIRCLE = -1

BOARD_SIZE = 3

# Gamestates
NOT_FINISHED = 9
CROSS_WIN = 1
CIRCLE_WIN = 2
DRAW = 0

WIN_MASKS = [[True, True, True, False, False, False, False, False, False],
             [False, False, False, True, True, True, False, False, False],
             [False, False, False, False, False, False, True, True, True],
             [True, False, False, True, False, False, True, False, False],
             [False, True, False, False, True, False, False, True, False],
             [False, False, True, False, False, True, False, False, True],
             [True, False, False, False, True, False, False, False, True],
             [False, False, True, False, True, False, True, False, False]]

class Board:
    """
    A tic-tac-toe board with size s.
    
    0: Empty
    1: Cross
    2: Circle
    """
    def __init__(self, s=3):
        self.size = s
        self.state = np.zeros(shape = (1, s*s), dtype=int)[0]
        
    def reset(self):
        self.state.fill(EMPTY)
        
    def n_empty_squares(self) -> int:
        """
        Returns the number of empty squares left in the game.
        """
        return np.count_nonzero(self.state == EMPTY)

    def random_empty_square(self) -> int:
        """
        Returns a random empty square.
        """
        return np.random.choice(np.where(self.state == EMPTY)[0])

    def all_empty_squares(self) -> list:
        """
        Return a list of the indices of all the empty squares.
        """
        indices = [i for i, x in enumerate(self.state) if x == 0]
        return indices

        
    def move(self, position: int, side: int):
        """
        Places a cross [1] or a circle [2] on position in self.state. 
        Return the gamesstate after the move, the game result, whether the game is finished.
        """
        
        if self.state[position] != EMPTY:
            print("Illegal move.")
            raise ValueError("Invalid move.")
            
        self.state[position] = side
        
        if self.check_win():
            return self.state, CROSS_WIN if side == CROSS else CIRCLE_WIN, True
        
        if self.n_empty_squares() == 0:
            return self.state, DRAW, True
        
        return self.state, NOT_FINISHED, False
    
    def check_win(self) -> bool:
        """
        Checks whether a side has won the game. 
        """
        for mask in WIN_MASKS:
            if (np.array_equal(self.state[mask], [CROSS, CROSS, CROSS]) | 
                np.array_equal(self.state[mask], [CIRCLE, CIRCLE, CIRCLE])):
                return True
            
        return False
    
    def who_won(self) -> int:
        """
        Returns the player who won, 0 if nobody won. 
        """
        for mask in WIN_MASKS:
            if (np.array_equal(self.state[mask], [CROSS, CROSS, CROSS])):
                return CROSS
            elif (np.array_equal(self.state[mask], [CIRCLE, CIRCLE, CIRCLE])):
                return CIRCLE

        if self.n_empty_squares == 0:
            return DRAW
        else:
            return EMPTY

    def next_board_states(self, side):
        """
        Returns all possible next board states for a given side.
        """
        empty_squares = self.all_empty_squares()
        next_board_states = np.zeros(shape=(len(empty_squares), 9))

        for i, e in enumerate(empty_squares):
            next_board_state = self.state.copy()
            next_board_state[e] = side
            next_board_states[i] = next_board_state

        return empty_squares, next_board_states

    
    def print_board(self):
        """
        Print a ascii representation of the board.
        """
        print('-----')
        for row in [0,3,6]:
            board_str = '|'
            for i in range(3):
                board_str = board_str + (' ' if self.state[row+i] == 0 else 'X' if self.state[row+i] == 1 else 'O')
            board_str = board_str + '|'
            print(board_str)
        print('-----')