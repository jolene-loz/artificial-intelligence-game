from self_driving_team.util import *
import copy
import time

"""
distance based eval function for minimax_dist,
use this when normal eval returns 0
this returns a value between 0 to 1
"""

def eval_zero(board_dict):

    # shortest black white manhattan distance (max possible = 14)
    shortest_dist = 14
    for pos1, str1 in board_dict.items():

        # get the shortest disance to a black tile
        if str1[0] == 'W':

            for pos2, str2 in board_dict.items():

                if str2[0] == 'B':
                    dist = manhattan_distance(pos1, pos2)

                    # this is the current shortest distance between a black and a white token
                    if dist < shortest_dist:
                        shortest_dist = dist

    return 1-(shortest_dist/14)

"""
minimax function with alpha beta pruning and zero reevaluation
"""
def minimax_dist(board_dict, num_black, num_white, colour, remaining_depth, alpha, beta, is_max_player, max_player_colour):

    # if at max depth or game over return the current eval
    if is_end(num_black, num_white, remaining_depth):

        # get evaluation
        score = eval(max_player_colour, num_black, num_white)

        # if evaluation is 0, use eval_zero to move closer to enemy
        if score == 0:
            score = eval_zero(board_dict)

        return (score, "")

    # generating moves
    moves = all_moves(board_dict, colour)

    # if can not generate any more moves, return
    if not moves:
        return (eval(max_player_colour, num_black, num_white), "")

    # selected move default, if unable to select move
    selected_move = moves[0]

    # max player
    if is_max_player:

        # neg infinity
        val = -100000

        for move in moves:

            new_board, new_black, new_white = make_move(copy.deepcopy(board_dict), move, num_black, num_white)

            # switching colours for children
            colour = colour_switch(colour)

            # score from the level below
            max_score = minimax_dist(new_board, new_black, new_white, colour, remaining_depth-1, alpha, beta, False, max_player_colour)[0]

            if max_score > val:
                val = max_score
                selected_move = move

            # update alpha
            alpha = max(alpha, val)

            # beta cutoff
            if alpha >= beta :
                break

        return (val, selected_move)

    # min player
    else:

        # pos infinity
        val = 100000

        for move in moves:
            new_board, new_black, new_white = make_move(copy.deepcopy(board_dict), move, num_black, num_white)

            # switching colours for children
            colour = colour_switch(colour)

            # score from level below
            min_score = minimax_dist(new_board, new_black, new_white, colour, remaining_depth-1, alpha, beta, True, max_player_colour)[0]

            # update val
            if min_score < val:
                val = min_score
                selected_move = move

            # update beta
            beta = min(beta, val)

            # alpha cutoff
            if alpha >= beta:
                break

        return (val, selected_move)


"""
checks if it is end for a minimax tree
"""
def is_end(num_player_tokens, num_enemy_tokens, remaining_depth, isTimeBased=False, start_time=None):

    # player wins
    if num_player_tokens == 0:
        return True
    # enemy wins
    if num_enemy_tokens == 0:
        return True
    # max depth reached
    if remaining_depth == 0:
        return True

    if isTimeBased:
        if time.perf_counter() - start_time > 0.21:
            return True

    return False

"""
minimax function with alpha beta pruning
"""
def minimax(board_dict, num_black, num_white, colour, remaining_depth, alpha, beta, is_max_player, max_player_colour):

    # if at max depth or game over return the current eval
    if is_end(num_black, num_white, remaining_depth):
        return (eval(max_player_colour, num_black, num_white), "")

    # generating moves
    moves = all_moves(board_dict, colour)

    # if can not generate any more moves, return
    if not moves:
        return (eval(max_player_colour, num_black, num_white), "")

    # selected move default, if unable to select move
    selected_move = moves[0]

    # max player
    if is_max_player:

        # neg infinity
        val = -100000

        for move in moves:

            new_board, new_black, new_white = make_move(copy.deepcopy(board_dict), move, num_black, num_white)

            # switching colours for children
            colour = colour_switch(colour)

            # score from the level below
            max_score = minimax(new_board, new_black, new_white, colour, remaining_depth-1, alpha, beta, False, max_player_colour)[0]

            if max_score > val:
                val = max_score
                selected_move = move

            # update alpha
            alpha = max(alpha, val)

            # beta cutoff
            if alpha >= beta :
                break

        return (val, selected_move)

    # min player
    else:

        # pos infinity
        val = 100000

        for move in moves:
            new_board, new_black, new_white = make_move(copy.deepcopy(board_dict), move, num_black, num_white)

            # switching colours for children
            colour = colour_switch(colour)

            # score from level below
            min_score = minimax(new_board, new_black, new_white, colour, remaining_depth-1, alpha, beta, True, max_player_colour)[0]

            # update val
            if min_score < val:
                val = min_score
                selected_move = move

            # update beta
            beta = min(beta, val)

            # alpha cutoff
            if alpha >= beta:
                break

        return (val, selected_move)
"""
mini max with alphabeta pruning and time constraint
"""
def minimax_time(board_dict, num_black, num_white, colour, remaining_depth, alpha, beta, is_max_player, max_player_colour, start_time):

    # generating moves
    moves = all_moves(board_dict, colour)

    # if at max depth or game over return the current eval
    if is_end(num_black, num_white, remaining_depth, True, start_time) or not moves:

        # get evaluation
        score = eval(max_player_colour, num_black, num_white)

        return (score, "")

    # selected move default, if unable to select move
    selected_move = moves[0]

    # max player
    if is_max_player:

        # neg infinity
        val = -100000

        for move in moves:

            new_board, new_black, new_white = make_move(copy.deepcopy(board_dict), move, num_black, num_white)

            # switching colours for children
            colour = colour_switch(colour)

            # score from the level below
            max_score = minimax_time(new_board, new_black, new_white, colour, remaining_depth-1, alpha, beta, False, max_player_colour, start_time)[0]

            if max_score > val:
                val = max_score
                selected_move = move

            # update alpha
            alpha = max(alpha, val)

            # beta cutoff
            if alpha >= beta :
                break

        return (val, selected_move)

    # min player
    else:

        # pos infinity
        val = 100000

        for move in moves:
            new_board, new_black, new_white = make_move(copy.deepcopy(board_dict), move, num_black, num_white)

            # switching colours for children
            colour = colour_switch(colour)

            # score from level below
            min_score = minimax_time(new_board, new_black, new_white, colour, remaining_depth-1, alpha, beta, True, max_player_colour, start_time)[0]

            # update val
            if min_score < val:
                val = min_score
                selected_move = move

            # update beta
            beta = min(beta, val)

            # alpha cutoff
            if alpha >= beta:
                break

        return (val, selected_move)
