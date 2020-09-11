import copy

"""
get number from str
"""
def get_num(str):
    return int(str.split()[-1])

"""
colour switching function for minimax, returns the other colour
"""
def colour_switch(colour):
    if colour == "white":
        return "black"
    if colour == "black":
        return "white"

"""
returns the manhattan distance betweeen two points
"""
def manhattan_distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return (x2-x1)+(y2-y1)


"""
returns the best move to make at the movement
"""
def greedy_move(board_dict, moves, colour, num_black, num_white):

    max_move = moves[0]
    max_score = -99999

    for move in moves:
        # make every move
        future_board, future_black, future_white = make_move(copy.deepcopy(board_dict), move, num_black, num_white)

        # get an eval for it
        score = eval(colour, future_black, future_white)

        # if max eval so far mark it as the best
        if score > max_score:
            max_move = move
            max_score = score

    return max_move

"""
basic evaluation function for player colour
"""
def eval(player_colour, num_black, num_white):
    if player_colour == "black":
        return num_black - num_white
    elif player_colour == "white":
        return num_white - num_black

"""
returns all the tokens in radius
"""
def tokens_in_radius(pos, board_dict, n=7):
    (x, y) = pos
    candidates = [(x-1,y-1),(x-1,y), (x-1,y+1),(x,y-1),(x,y+1),(x+1,y-1),
    (x+1,y),(x+1,y+1)]

    boomable = []
    for candidate in candidates:
        (x, y) = candidate
        #checks if position is valid and white
        if x>=0 and y>=0 and x<=n and y<=n and candidate in board_dict:
            boomable.append(candidate)
    return boomable

"""
recursive function returns the the board_dict after boom
+ the number of tiles lost
"""
def post_boom_update(board_dict, boom_pos, seen_set, num_black, num_white):

    # adjusting counts
    if board_dict[boom_pos][0] == 'B':
        num_black -= get_num(board_dict[boom_pos])
    elif board_dict[boom_pos][0] == 'W':
        num_white -= get_num(board_dict[boom_pos])

    # removing the boomed tokens
    board_dict.pop(boom_pos, None)
    seen_set.add(boom_pos)

    # getting the next in radius tokens
    next = tokens_in_radius(boom_pos, board_dict)

    for token in next:
        if token not in seen_set:
            board_dict, num_black, num_white = post_boom_update(board_dict, token, seen_set, num_black, num_white)

    return board_dict, num_black, num_white

"""
returns the board_dict, num_black, num_white after a move or a boom
"""
def make_move(board_dict, move, num_black, num_white):

    if move[0] == "BOOM":
        boom_pos = move[1]
        board_dict, num_black, num_white = post_boom_update(board_dict, boom_pos, set(), num_black, num_white)

    elif move[0] == "MOVE":
        n = move[1]
        old_pos = move[2]
        new_pos = move[3]
        symbol = board_dict[old_pos][0]

        # if new not in board dict, add it to the dict (initalised to 0)
        if not new_pos in board_dict:
            board_dict[new_pos] = symbol + " " + "0"

        # if old moving all its tokens, delete it from board_dict, update new
        if n == get_num(board_dict[old_pos]):
            val = board_dict.pop(old_pos, None)
            board_dict[new_pos] = symbol + " " + str(get_num(board_dict[new_pos]) + n)

        # else update both values
        else:
            board_dict[old_pos] = symbol + " " + str(get_num(board_dict[old_pos]) - n)
            board_dict[new_pos] = symbol + " " + str(get_num(board_dict[new_pos]) + n)

    return board_dict, num_black, num_white

"""
gets all the moveable positions for a token
"""
def get_moveable_tiles(board_dict, pos, n):

    # unpacking pos
    x, y = pos

    # moveable tiles
    tiles = []

    for i in range(1, n+1):
        if is_valid_move(board_dict, pos, (x+i,y)):
            tiles.append((x+i,y))

        if is_valid_move(board_dict, pos, (x-i,y)):
            tiles.append((x-i,y))

        if is_valid_move(board_dict, pos, (x,y+i)):
            tiles.append((x,y+i))

        if is_valid_move(board_dict, pos, (x,y-i)):
            tiles.append((x,y-i))

    return tiles

"""
gets all available moves for a given team
"""
def all_moves(board_dict, colour):

    moves = []
    for pos, str in board_dict.items():
        if (colour == "white" and str[0] == 'W') or (colour == "black" and str[0] == 'B'):
            moves.extend(avail_moves(board_dict, pos))

    return moves

"""
gets all available moves for a position
"""
def avail_moves(board_dict, pos):

    # size of stack at position
    n = get_num(board_dict[pos])

    # array of all possible moves, boom is always an option
    moves = [("BOOM", pos)]

    # getting the moveable tiles
    moveable_tiles = get_moveable_tiles(board_dict, pos, n)
    num_tiles = len(moveable_tiles)

    # generating moves stacks upto size n
    for i in range(1, n+1):

        # getting into the MOVE from the spec for the referee
        move_list = ["MOVE"] * num_tiles
        n_list = [i] * num_tiles
        pos_list = [pos] * num_tiles
        moves.extend(zip(move_list, n_list, pos_list, moveable_tiles))

    return moves

"""
checks if a MOVE is valid
"""
def is_valid_move(board_dict, initialPos, finalPos):

    # intial positions is not empty
    if not initialPos in board_dict:
        return False

    # final position must be empty or the same color
    if (finalPos in board_dict) and (board_dict[initialPos][0] != board_dict[finalPos][0]):
        return False

    # check if both positions on the board
    if initialPos[0] < 0 or initialPos[0] > 7:
        return False

    if initialPos[1] < 0 or initialPos[1] > 7:
        return False

    if finalPos[0] < 0 or finalPos[0] > 7:
        return False

    if finalPos[1] < 0 or finalPos[1] > 7:
        return False

    return True

def init_board():
    """Initiates the board as described by the game spec"""

    board_dict = {}

    # initial specified positions
    for i in [0,1,3,4,6,7]:

        # white token positions
        board_dict[(i,0)] = "W 1"
        board_dict[(i,1)] = "W 1"

        # back token positions
        board_dict[(i,6)] = "B 1"
        board_dict[(i,7)] = "B 1"

    return board_dict

def print_board(board_dict, message="", unicode=False, compact=True, **kwargs):
    """
    For help with visualisation and debugging: output a board diagram with
    any information you like (tokens, heuristic values, distances, etc.).

    Arguments:
    board_dict -- A dictionary with (x, y) tuples as keys (x, y in range(8))
        and printable objects (e.g. strings, numbers) as values. This function
        will arrange these printable values on the grid and output the result.
        Note: At most the first 3 characters will be printed from the string
        representation of each value.
    message -- A printable object (e.g. string, number) that will be placed
        above the board in the visualisation. Default is "" (no message).
    unicode -- True if you want to use non-ASCII symbols in the board
        visualisation (see below), False to use only ASCII symbols.
        Default is False, since the unicode symbols may not agree with some
        terminal emulators.
    compact -- True if you want to use a compact board visualisation, with
        coordinates along the edges of the board, False to use a bigger one
        with coordinates alongside the printable information in each square.
        Default True (small board).

    Any other keyword arguments are passed through to the print function.
    """
    if unicode:
        if compact:
            template = """# {}
#    ┌───┬───┬───┬───┬───┬───┬───┬───┐
#  7 │{:}│{:}│{:}│{:}│{:}│{:}│{:}│{:}│
#    ├───┼───┼───┼───┼───┼───┼───┼───┤
#  6 │{:}│{:}│{:}│{:}│{:}│{:}│{:}│{:}│
#    ├───┼───┼───┼───┼───┼───┼───┼───┤
#  5 │{:}│{:}│{:}│{:}│{:}│{:}│{:}│{:}│
#    ├───┼───┼───┼───┼───┼───┼───┼───┤
#  4 │{:}│{:}│{:}│{:}│{:}│{:}│{:}│{:}│
#    ├───┼───┼───┼───┼───┼───┼───┼───┤
#  3 │{:}│{:}│{:}│{:}│{:}│{:}│{:}│{:}│
#    ├───┼───┼───┼───┼───┼───┼───┼───┤
#  2 │{:}│{:}│{:}│{:}│{:}│{:}│{:}│{:}│
#    ├───┼───┼───┼───┼───┼───┼───┼───┤
#  1 │{:}│{:}│{:}│{:}│{:}│{:}│{:}│{:}│
#    ├───┼───┼───┼───┼───┼───┼───┼───┤
#  0 │{:}│{:}│{:}│{:}│{:}│{:}│{:}│{:}│
#    └───┴───┴───┴───┴───┴───┴───┴───┘
# y/x  0   1   2   3   4   5   6   7"""
        else:
            template = """# {}
# ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐
# │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │
# │ 0,7 │ 1,7 │ 2,7 │ 3,7 │ 4,7 │ 5,7 │ 6,7 │ 7,7 │
# ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
# │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │
# │ 0,6 │ 1,6 │ 2,6 │ 3,6 │ 4,6 │ 5,6 │ 6,6 │ 7,6 │
# ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
# │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │
# │ 0,5 │ 1,5 │ 2,5 │ 3,5 │ 4,5 │ 5,5 │ 6,5 │ 7,5 │
# ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
# │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │
# │ 0,4 │ 1,4 │ 2,4 │ 3,4 │ 4,4 │ 5,4 │ 6,4 │ 7,4 │
# ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
# │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │
# │ 0,3 │ 1,3 │ 2,3 │ 3,3 │ 4,3 │ 5,3 │ 6,3 │ 7,3 │
# ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
# │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │
# │ 0,2 │ 1,2 │ 2,2 │ 3,2 │ 4,2 │ 5,2 │ 6,2 │ 7,2 │
# ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
# │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │
# │ 0,1 │ 1,1 │ 2,1 │ 3,1 │ 4,1 │ 5,1 │ 6,1 │ 7,1 │
# ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤
# │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │ {:} │
# │ 0,0 │ 1,0 │ 2,0 │ 3,0 │ 4,0 │ 5,0 │ 6,0 │ 7,0 │
# └─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┘"""
    else:
        if compact:
            template = """# {}
#    +---+---+---+---+---+---+---+---+
#  7 |{:}|{:}|{:}|{:}|{:}|{:}|{:}|{:}|
#    +---+---+---+---+---+---+---+---+
#  6 |{:}|{:}|{:}|{:}|{:}|{:}|{:}|{:}|
#    +---+---+---+---+---+---+---+---+
#  5 |{:}|{:}|{:}|{:}|{:}|{:}|{:}|{:}|
#    +---+---+---+---+---+---+---+---+
#  4 |{:}|{:}|{:}|{:}|{:}|{:}|{:}|{:}|
#    +---+---+---+---+---+---+---+---+
#  3 |{:}|{:}|{:}|{:}|{:}|{:}|{:}|{:}|
#    +---+---+---+---+---+---+---+---+
#  2 |{:}|{:}|{:}|{:}|{:}|{:}|{:}|{:}|
#    +---+---+---+---+---+---+---+---+
#  1 |{:}|{:}|{:}|{:}|{:}|{:}|{:}|{:}|
#    +---+---+---+---+---+---+---+---+
#  0 |{:}|{:}|{:}|{:}|{:}|{:}|{:}|{:}|
#    +---+---+---+---+---+---+---+---+
# y/x  0   1   2   3   4   5   6   7"""
        else:
            template = """# {}
# +-----+-----+-----+-----+-----+-----+-----+-----+
# | {:} | {:} | {:} | {:} | {:} | {:} | {:} | {:} |
# | 0,7 | 1,7 | 2,7 | 3,7 | 4,7 | 5,7 | 6,7 | 7,7 |
# +-----+-----+-----+-----+-----+-----+-----+-----+
# | {:} | {:} | {:} | {:} | {:} | {:} | {:} | {:} |
# | 0,6 | 1,6 | 2,6 | 3,6 | 4,6 | 5,6 | 6,6 | 7,6 |
# +-----+-----+-----+-----+-----+-----+-----+-----+
# | {:} | {:} | {:} | {:} | {:} | {:} | {:} | {:} |
# | 0,5 | 1,5 | 2,5 | 3,5 | 4,5 | 5,5 | 6,5 | 7,5 |
# +-----+-----+-----+-----+-----+-----+-----+-----+
# | {:} | {:} | {:} | {:} | {:} | {:} | {:} | {:} |
# | 0,4 | 1,4 | 2,4 | 3,4 | 4,4 | 5,4 | 6,4 | 7,4 |
# +-----+-----+-----+-----+-----+-----+-----+-----+
# | {:} | {:} | {:} | {:} | {:} | {:} | {:} | {:} |
# | 0,3 | 1,3 | 2,3 | 3,3 | 4,3 | 5,3 | 6,3 | 7,3 |
# +-----+-----+-----+-----+-----+-----+-----+-----+
# | {:} | {:} | {:} | {:} | {:} | {:} | {:} | {:} |
# | 0,2 | 1,2 | 2,2 | 3,2 | 4,2 | 5,2 | 6,2 | 7,2 |
# +-----+-----+-----+-----+-----+-----+-----+-----+
# | {:} | {:} | {:} | {:} | {:} | {:} | {:} | {:} |
# | 0,1 | 1,1 | 2,1 | 3,1 | 4,1 | 5,1 | 6,1 | 7,1 |
# +-----+-----+-----+-----+-----+-----+-----+-----+
# | {:} | {:} | {:} | {:} | {:} | {:} | {:} | {:} |
# | 0,0 | 1,0 | 2,0 | 3,0 | 4,0 | 5,0 | 6,0 | 7,0 |
# +-----+-----+-----+-----+-----+-----+-----+-----+"""
    # board the board string
    coords = [(x,7-y) for y in range(8) for x in range(8)]
    cells = []
    for xy in coords:
        if xy not in board_dict:
            cells.append("   ")
        else:
            cells.append(str(board_dict[xy])[:3].center(3))
    # print it
    print(template.format(message, *cells), **kwargs)
