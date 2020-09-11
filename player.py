import random
import time
from self_driving_team.util import *
from self_driving_team.minimax import *
from self_driving_team.catapult import *

# player 1: greedy player, makes the best move at the movement
class GreedyPlayer:
    def __init__(self, colour):
        """
        This method is called once at the beginning of the game to initialise
        your player. You should use this opportunity to set up your own internal
        representation of the game state, and any other information about the
        game state you would like to maintain for the duration of the game.

        The parameter colour will be a string representing the player your
        program will play as (White or Black). The value will be one of the
        strings "white" or "black" correspondingly.
        """

        # initialising the board
        self.colour = colour
        self.board_dict = init_board()
        self.num_black = 12
        self.num_white = 12

    def action(self):
        """
        This method is called at the beginning of each of your turns to request
        a choice of action from your program.

        Based on the current state of the game, your player should select and
        return an allowed action to play on this turn. The action must be
        represented based on the spec's instructions for representing actions.
        """
        # get all moves for our colour
        moves = all_moves(self.board_dict,self.colour)

        # get the greediest move from the move
        move = greedy_move(self.board_dict, moves, self.colour, self.num_black, self.num_white)

        return move


    def update(self, colour, action):
        """
        This method is called at the end of every turn (including your player’s
        turns) to inform your player about the most recent action. You should
        use this opportunity to maintain your internal representation of the
        game state and any other information about the game you are storing.

        The parameter colour will be a string representing the player whose turn
        it is (White or Black). The value will be one of the strings "white" or
        "black" correspondingly.

        The parameter action is a representation of the most recent action
        conforming to the spec's instructions for representing actions.

        You may assume that action will always correspond to an allowed action
        for the player colour (your method does not need to validate the action
        against the game rules).
        """

        # update the board accordingly
        self.board_dict, self.num_black, self.num_white = make_move(self.board_dict, action, self.num_black, self.num_white)


# player 2: random player, makes random move from all available moves
class RandomPlayer:
    def __init__(self, colour):
        """
        This method is called once at the beginning of the game to initialise
        your player. You should use this opportunity to set up your own internal
        representation of the game state, and any other information about the
        game state you would like to maintain for the duration of the game.

        The parameter colour will be a string representing the player your
        program will play as (White or Black). The value will be one of the
        strings "white" or "black" correspondingly.
        """

        # initialising the board
        self.colour = colour
        self.board_dict = init_board()
        self.num_black = 12
        self.num_white = 12

    def action(self):
        """
        This method is called at the beginning of each of your turns to request
        a choice of action from your program.

        Based on the current state of the game, your player should select and
        return an allowed action to play on this turn. The action must be
        represented based on the spec's instructions for representing actions.
        """
        # get all moves for our colour
        moves = all_moves(self.board_dict, self.colour)

        # get a random move from those moves
        move = random.choice(moves)

        return move


    def update(self, colour, action):
        """
        This method is called at the end of every turn (including your player’s
        turns) to inform your player about the most recent action. You should
        use this opportunity to maintain your internal representation of the
        game state and any other information about the game you are storing.

        The parameter colour will be a string representing the player whose turn
        it is (White or Black). The value will be one of the strings "white" or
        "black" correspondingly.

        The parameter action is a representation of the most recent action
        conforming to the spec's instructions for representing actions.

        You may assume that action will always correspond to an allowed action
        for the player colour (your method does not need to validate the action
        against the game rules).
        """

        # update the board accordingly
        self.board_dict, self.num_black, self.num_white = make_move(self.board_dict, action, self.num_black, self.num_white)

# player 3: alpha beta pruning minimax
class AlphaBetaPlayer:
    def __init__(self, colour):
        """
        This method is called once at the beginning of the game to initialise
        your player. You should use this opportunity to set up your own internal
        representation of the game state, and any other information about the
        game state you would like to maintain for the duration of the game.

        The parameter colour will be a string representing the player your
        program will play as (White or Black). The value will be one of the
        strings "white" or "black" correspondingly.
        """

        # initialising the board
        self.colour = colour
        self.board_dict = init_board()
        self.num_black = 12
        self.num_white = 12

    def action(self):
        """
        This method is called at the beginning of each of your turns to request
        a choice of action from your program.

        Based on the current state of the game, your player should select and
        return an allowed action to play on this turn. The action must be
        represented based on the spec's instructions for representing actions.
        """
        # perform alpha beta minimax adversarial search
        max_depth = 3
        alpha = -100000     # neg inf
        beta = 100000   # pos inf
        is_max_player = True

        val, move = minimax(self.board_dict, self.num_black, self.num_white, self.colour, max_depth, alpha, beta, is_max_player, self.colour)

        return move


    def update(self, colour, action):
        """
        This method is called at the end of every turn (including your player’s
        turns) to inform your player about the most recent action. You should
        use this opportunity to maintain your internal representation of the
        game state and any other information about the game you are storing.

        The parameter colour will be a string representing the player whose turn
        it is (White or Black). The value will be one of the strings "white" or
        "black" correspondingly.

        The parameter action is a representation of the most recent action
        conforming to the spec's instructions for representing actions.

        You may assume that action will always correspond to an allowed action
        for the player colour (your method does not need to validate the action
        against the game rules).
        """

        # update the board accordingly
        self.board_dict, self.num_black, self.num_white = make_move(self.board_dict, action, self.num_black, self.num_white)

# player 4: alpha beta pruning minimax where 0 evals are recalculated to move in the right direction
class AlphaBetaNonZeroPlayer:
    def __init__(self, colour):
        """
        This method is called once at the beginning of the game to initialise
        your player. You should use this opportunity to set up your own internal
        representation of the game state, and any other information about the
        game state you would like to maintain for the duration of the game.

        The parameter colour will be a string representing the player your
        program will play as (White or Black). The value will be one of the
        strings "white" or "black" correspondingly.
        """

        # initialising the board
        self.colour = colour
        self.board_dict = init_board()
        self.num_black = 12
        self.num_white = 12

    def action(self):
        """
        This method is called at the beginning of each of your turns to request
        a choice of action from your program.

        Based on the current state of the game, your player should select and
        return an allowed action to play on this turn. The action must be
        represented based on the spec's instructions for representing actions.
        """
        # perform alpha beta minimax adversarial search
        max_depth = 3
        alpha = -100000     # neg inf
        beta = 100000   # pos inf
        is_max_player = True

        val, move = minimax_dist(self.board_dict, self.num_black, self.num_white, self.colour, max_depth, alpha, beta, is_max_player, self.colour)

        return move


    def update(self, colour, action):
        """
        This method is called at the end of every turn (including your player’s
        turns) to inform your player about the most recent action. You should
        use this opportunity to maintain your internal representation of the
        game state and any other information about the game you are storing.

        The parameter colour will be a string representing the player whose turn
        it is (White or Black). The value will be one of the strings "white" or
        "black" correspondingly.

        The parameter action is a representation of the most recent action
        conforming to the spec's instructions for representing actions.

        You may assume that action will always correspond to an allowed action
        for the player colour (your method does not need to validate the action
        against the game rules).
        """

        # update the board accordingly
        self.board_dict, self.num_black, self.num_white = make_move(self.board_dict, action, self.num_black, self.num_white)

# player 5: minimax alpha beta pruning and zero reevaluation and time constraint
class AlphaBetaTimeDist:
    def __init__(self, colour):
        """
        This method is called once at the beginning of the game to initialise
        your player. You should use this opportunity to set up your own internal
        representation of the game state, and any other information about the
        game state you would like to maintain for the duration of the game.

        The parameter colour will be a string representing the player your
        program will play as (White or Black). The value will be one of the
        strings "white" or "black" correspondingly.
        """

        # initialising the board
        self.colour = colour
        self.board_dict = init_board()
        self.num_black = 12
        self.num_white = 12

    def action(self):
        """
        This method is called at the beginning of each of your turns to request
        a choice of action from your program.

        Based on the current state of the game, your player should select and
        return an allowed action to play on this turn. The action must be
        represented based on the spec's instructions for representing actions.
        """

        # perform alpha beta minimax adversarial search
        max_depth = 10
        alpha = -100000    # neg inf
        beta = 100000   # pos inf
        is_max_player = True
        start_time = time.perf_counter()

        val, move = minimax_time_dist(self.board_dict, self.num_black, self.num_white, self.colour, max_depth, alpha, beta, is_max_player, self.colour, start_time)

        return move


    def update(self, colour, action):
        """
        This method is called at the end of every turn (including your player’s
        turns) to inform your player about the most recent action. You should
        use this opportunity to maintain your internal representation of the
        game state and any other information about the game you are storing.

        The parameter colour will be a string representing the player whose turn
        it is (White or Black). The value will be one of the strings "white" or
        "black" correspondingly.

        The parameter action is a representation of the most recent action
        conforming to the spec's instructions for representing actions.

        You may assume that action will always correspond to an allowed action
        for the player colour (your method does not need to validate the action
        against the game rules).
        """

        # update the board accordingly
        self.board_dict, self.num_black, self.num_white = make_move(self.board_dict, action, self.num_black, self.num_white)

# player 6: minimax alpha beta pruning and time constraint
class AlphaBetaTime:
    def __init__(self, colour):
        """
        This method is called once at the beginning of the game to initialise
        your player. You should use this opportunity to set up your own internal
        representation of the game state, and any other information about the
        game state you would like to maintain for the duration of the game.

        The parameter colour will be a string representing the player your
        program will play as (White or Black). The value will be one of the
        strings "white" or "black" correspondingly.
        """

        # initialising the board
        self.colour = colour
        self.board_dict = init_board()
        self.num_black = 12
        self.num_white = 12

    def action(self):
        """
        This method is called at the beginning of each of your turns to request
        a choice of action from your program.

        Based on the current state of the game, your player should select and
        return an allowed action to play on this turn. The action must be
        represented based on the spec's instructions for representing actions.
        """

        # perform alpha beta minimax adversarial search
        max_depth = 10
        alpha = -100000    # neg inf
        beta = 100000   # pos inf
        is_max_player = True
        start_time = time.perf_counter()

        val, move = minimax_time(self.board_dict, self.num_black, self.num_white, self.colour, max_depth, alpha, beta, is_max_player, self.colour, start_time)

        return move


    def update(self, colour, action):
        """
        This method is called at the end of every turn (including your player’s
        turns) to inform your player about the most recent action. You should
        use this opportunity to maintain your internal representation of the
        game state and any other information about the game you are storing.

        The parameter colour will be a string representing the player whose turn
        it is (White or Black). The value will be one of the strings "white" or
        "black" correspondingly.

        The parameter action is a representation of the most recent action
        conforming to the spec's instructions for representing actions.

        You may assume that action will always correspond to an allowed action
        for the player colour (your method does not need to validate the action
        against the game rules).
        """

        # update the board accordingly
        self.board_dict, self.num_black, self.num_white = make_move(self.board_dict, action, self.num_black, self.num_white)

# player 7: Based on the Catapult trick discussed in our report
class CatapultPlayer:
    def __init__(self, colour):
        """
        This method is called once at the beginning of the game to initialise
        your player. You should use this opportunity to set up your own internal
        representation of the game state, and any other information about the
        game state you would like to maintain for the duration of the game.

        The parameter colour will be a string representing the player your
        program will play as (White or Black). The value will be one of the
        strings "white" or "black" correspondingly.
        """

        # initialising the board
        self.colour = colour
        self.board_dict = init_board()
        self.num_black = 12
        self.num_white = 12

    def action(self):
        """
        This method is called at the beginning of each of your turns to request
        a choice of action from your program.

        Based on the current state of the game, your player should select and
        return an allowed action to play on this turn. The action must be
        represented based on the spec's instructions for representing actions.
        """

        # perform alpha beta minimax adversarial search
        max_depth = 3
        alpha = -100000    # neg inf
        beta = 100000   # pos inf
        is_max_player = True

        val, move = minimax_catapult(self.board_dict, self.num_black, self.num_white, self.colour, max_depth, alpha, beta, is_max_player, self.colour)
        return move


    def update(self, colour, action):
        """
        This method is called at the end of every turn (including your player’s
        turns) to inform your player about the most recent action. You should
        use this opportunity to maintain your internal representation of the
        game state and any other information about the game you are storing.

        The parameter colour will be a string representing the player whose turn
        it is (White or Black). The value will be one of the strings "white" or
        "black" correspondingly.

        The parameter action is a representation of the most recent action
        conforming to the spec's instructions for representing actions.

        You may assume that action will always correspond to an allowed action
        for the player colour (your method does not need to validate the action
        against the game rules).
        """

        # update the board accordingly
        self.board_dict, self.num_black, self.num_white = make_move(self.board_dict, action, self.num_black, self.num_white)

# player 7: Based on the Catapult trick discussed in our report and Zero reevaluation
class CatapultNonZeroPlayer:
    def __init__(self, colour):
        """
        This method is called once at the beginning of the game to initialise
        your player. You should use this opportunity to set up your own internal
        representation of the game state, and any other information about the
        game state you would like to maintain for the duration of the game.

        The parameter colour will be a string representing the player your
        program will play as (White or Black). The value will be one of the
        strings "white" or "black" correspondingly.
        """

        # initialising the board
        self.colour = colour
        self.board_dict = init_board()
        self.num_black = 12
        self.num_white = 12

    def action(self):
        """
        This method is called at the beginning of each of your turns to request
        a choice of action from your program.

        Based on the current state of the game, your player should select and
        return an allowed action to play on this turn. The action must be
        represented based on the spec's instructions for representing actions.
        """

        # perform alpha beta minimax adversarial search
        max_depth = 3
        alpha = -100000    # neg inf
        beta = 100000   # pos inf
        is_max_player = True

        val, move = minimax_catapult_dist(self.board_dict, self.num_black, self.num_white, self.colour, max_depth, alpha, beta, is_max_player, self.colour)
        return move


    def update(self, colour, action):
        """
        This method is called at the end of every turn (including your player’s
        turns) to inform your player about the most recent action. You should
        use this opportunity to maintain your internal representation of the
        game state and any other information about the game you are storing.

        The parameter colour will be a string representing the player whose turn
        it is (White or Black). The value will be one of the strings "white" or
        "black" correspondingly.

        The parameter action is a representation of the most recent action
        conforming to the spec's instructions for representing actions.

        You may assume that action will always correspond to an allowed action
        for the player colour (your method does not need to validate the action
        against the game rules).
        """

        # update the board accordingly
        self.board_dict, self.num_black, self.num_white = make_move(self.board_dict, action, self.num_black, self.num_white)
