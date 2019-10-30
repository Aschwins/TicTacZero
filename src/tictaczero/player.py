from tictaczero.board import Board
from tictaczero.board import WIN_MASKS, CROSS, CIRCLE
from tensorflow import keras
import tensorflow as tf
import numpy as np

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
        

class SmartPlayer(BasePlayer):
    """
    A Tic tac toe player which make 3 when there is the opportunity to make 3.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def move(self, board):
        optimal_square = 100
        for connect_3 in WIN_MASKS:
            combination = board.state[connect_3]
            if (np.array_equal(combination, [self.side, self.side, 0]) |
                np.array_equal(combination, [self.side, 0, self.side]) |
                np.array_equal(combination, [0, self.side, self.side])):
                # There is a winning combination!
                index_0 = [i for i, x in enumerate(combination) if x == 0][0] # Get empty square loc.
                optimal_square = [i for i, x in enumerate(connect_3) if x][index_0]
        
        if optimal_square != 100:
            #print(f"{self.side}: We've found an optimal square, we'll win")
            _, res, finished = board.move(optimal_square, self.side)
        else:
            #print("There was no optimal square.")
            _, res, finished = board.move(board.random_empty_square(), self.side)

        return _, res, finished

class BrainPlayer(BasePlayer):
    """
    A player with a Brain as neural network. Memory on where it trains on and an Arm which decides on which moves to make.
    
    params
    update_after_n_states: Number of states it has to have add to memory to start learning again
    max_memory: Number of maximum game states allowed in memory
    exp_rate: exploration rate of new moves; float in [0, 1]
    """
    def __init__(self, update_after_n_states = 10000, max_memory = 100000,
                 exp_rate = 0.1,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_memory = max_memory
        self.N = update_after_n_states
        self.boardstates_seen = 0
        self.new_boardstates_seen = 0
        self.memory = np.empty(shape=(max_memory, 10), dtype=np.int32)
        self.memory_left = max_memory
        self.exp_rate = exp_rate
        self.brain = self.initialize_neural_net()
        
        
    def initialize_neural_net(self):
        model = keras.models.Sequential([
            keras.layers.Dense(28, input_shape = [9], activation = 'relu'),
            keras.layers.Dense(28, activation = 'relu'),
            keras.layers.Dense(3, activation = 'softmax')
        ])
        
        model.compile(optimizer="adam",
              loss="sparse_categorical_crossentropy",
              metrics=["accuracy"])
        
        return model
    
    def memorize(self, boardstates):
        """
        A function wich adds games (boardstates) to the memory. If number of games is bigger than
        max memory forget the first games. 
        boardstates: Must be a np.array of size (n, 10) where n is the number of games. And
        the last column contains the end result of said game.
        """
        n_boardstates = len(boardstates)

        if (n_boardstates > self.memory_left):
            memory_shortage = n_boardstates - self.memory_left
            self.memory[0:-n_boardstates, :] = self.memory[memory_shortage:self.boardstates_seen, :]
            self.memory[-n_boardstates, :] = boardstates
            self.memory_left = 0
            self.boardstates_seen = self.max_memory

        else:
            self.memory[self.boardstates_seen:self.boardstates_seen + n_boardstates, :] = boardstates
            self.boardstates_seen += n_boardstates
            self.memory_left -= n_boardstates

        self.new_boardstates_seen += n_boardstates
            
        if self.new_boardstates_seen > self.N:
            self.train_the_brain() # Train on last new_seen boardstates
            
    def train_the_brain(self):
        X = self.memory[-self.new_boardstates_seen:,:-1]
        y = self.memory[-self.new_boardstates_seen:, -1]
        
        tensor_X = tf.convert_to_tensor(X, np.float32)
        tensor_y = tf.convert_to_tensor(y, np.int32)
        self.brain.fit(tensor_X, tensor_y, batch_size=1000, epochs=20, verbose=1)
        
        self.new_boardstates_seen = 0
        
    def move(self, board):
        """
        A function which makes an exploration (random) move or a exploration (brainy) move.
        Calculates the scores of all possible moves and picks the one with the highest chance
        of winning.
        """
        # exploration
        if (np.random.uniform(0, 1) < self.exp_rate):
            # make a random move
            _, res, finished = board.move(board.random_empty_square(), self.side)
        # exploitation
        else:
            side_map = {CROSS: 1, CIRCLE: 2}
            
            empty_squares, next_board_states = board.next_board_states(self.side)
            scores = self.brain.predict(next_board_states)[:, side_map[self.side]]
            highest_score_idx = np.argmax(scores)
            
            best_move = empty_squares[highest_score_idx]
            
            _, res, finished = board.move(best_move, self.side)
            
        ## TO ADD:
#         If a game is finished the board should return the history of a game. and it
#         should be added to the memory of the brainy player.
            
            
        return _, res, finished