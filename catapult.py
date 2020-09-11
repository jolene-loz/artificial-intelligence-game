from self_driving_team.util import *
from self_driving_team.minimax import *

"""
minimax function with alpha beta pruning and catapult reevaluation and zero reevaluation
"""
def minimax_catapult_dist(board_dict, num_black, num_white, colour, remaining_depth, alpha, beta, is_max_player, max_player_colour):

    # if at max depth or game over return the current eval
    if is_end(num_black, num_white, remaining_depth):

        # get evaluation
        score = eval(max_player_colour, num_black, num_white)

        # if evaluation is 0, use eval_zero to move closer to enemy
        if score == 0:
            score = eval_catapult(board_dict, colour)

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
            max_score = minimax_catapult_dist(new_board, new_black, new_white, colour, remaining_depth-1, alpha, beta, False, max_player_colour)[0]

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
            min_score = minimax_catapult_dist(new_board, new_black, new_white, colour, remaining_depth-1, alpha, beta, True, max_player_colour)[0]

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
minimax function with alpha beta pruning and catapult reevaluation
"""
def minimax_catapult(board_dict, num_black, num_white, colour, remaining_depth, alpha, beta, is_max_player, max_player_colour):

    # if at max depth or game over return the current eval
    if is_end(num_black, num_white, remaining_depth):

        # get evaluation
        score = eval(max_player_colour, num_black, num_white)

        # if evaluation is 0, use eval_zero to move closer to enemy
        if score == 0:
            score = eval_catapult(board_dict,colour)

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
            max_score = minimax_catapult(new_board, new_black, new_white, colour, remaining_depth-1, alpha, beta, False, max_player_colour)[0]

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
            min_score = minimax_catapult(new_board, new_black, new_white, colour, remaining_depth-1, alpha, beta, True, max_player_colour)[0]

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
reevaluation function based on the catapult strategy discussed in our report,
only called when regular eval is zero, returns something between 0-1
O(1) eval
O(n) eval_catapult
O(n^2) eval_zero
the idea is: if eval is >= 1, great boom something
if eval is 0, then form a stack so in the next few turns you can catupult a token into
enemy territory
"""
def eval_catapult(board_dict, colour):
    max_pos, max_size = get_max_stack(board_dict, colour)
    if max_size == 1:
        return 0
    return max_size/12


def get_max_stack(board_dict, colour):

    max_white = max_black = 0
    white_pos = None
    black_pos = None

    if colour == "white":
        for pos, str in board_dict.items():

            if str[0] == 'W':
                if int(str[-1]) > max_white:
                    white_pos = pos
                    max_white = int(str[-1])

        return white_pos, max_white

    else:
        for pos, str in board_dict.items():

            if str[0] == 'B':
                if int(str[-1]) > max_black:
                    black_pos = pos
                    max_black = int(str[-1])

        return black_pos, max_black
