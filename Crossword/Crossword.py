from random import random
from random import choice
from collections import deque
from sys import argv
import re
# Global Vars
row = 0
col = 0
num_blocking_squares = 0
word_dictionary = ""


# Unless otherwise noted, board is a string for inputs
# Generates empty crossword board (string with boundaries represented as ?)
def generate_board():
    global row
    global col
    board = ""
    for c in range(col+2):
        board += "?"
    for r in range(row):
        board += "?"
        for c in range(col):
            board += "-"
        board += "?"
    for c in range(col+2):
        board += "?"
    # Takes boundaries into account (effective board size)
    row += 2
    col += 2
    return board


# Prints board as grid (space between each spot in grid)
def display(board):
    print_string = ""
    col_count = 0
    for char in board:
        if char == "?":
            continue
        print_string += char+" "
        col_count += 1
        if col_count == col-2:
            print_string += "\n"
            col_count = 0
    print(print_string)


# Given location of a blocking square, propagate blocking squares that MUST be there
# Board is a list
def propagate_blocking_squares(board, square_index):
    num_added = 0
    loc_added = set()
    loc_added.add(square_index)
    while len(loc_added) != 0:
        # 180 degree rotation
        index = loc_added.pop()
        reflect_index = len(board)-index-1
        if board[reflect_index] != "#":
            num_added += 1
            board[reflect_index] = "#"
            loc_added.add(reflect_index)
        # Must be > 3 spaces away from edge/on edge
        # If distance is less, then blocked squares must be used
        # Top Edge
        if index < col*4:
            new_index = index-col
            while board[new_index] != "?":
                if board[new_index] != "#":
                    board[new_index] = "#"
                    num_added += 1
                    loc_added.add(new_index)
                new_index = new_index-col
        # Bottom Edge
        if index > len(board)-col*4:
            new_index = index+col
            while board[new_index] != "?":
                if board[new_index] != "#":
                    board[new_index] = "#"
                    num_added += 1
                    loc_added.add(new_index)
                new_index = new_index+col
        # Left Edge
        if index-(index//col*col) < 4:
            new_index = index-1
            while board[new_index] != "?":
                if board[new_index] != "#":
                    board[new_index] = "#"
                    num_added += 1
                    loc_added.add(new_index)
                new_index = new_index-1
        # Right Edge
        if ((index//col+1)*col) - index < 4:
            new_index = index+1
            while board[new_index] != "?":
                if board[new_index] != "#":
                    board[new_index] = "#"
                    num_added += 1
                    loc_added.add(new_index)
                new_index = new_index+1
        # Must be three spaces away from other blocked squares
        # Means cannot allow for only one or two spaces between blocked squares
        for step in range(2, 4):
            # Up
            up_check_row = index - col*step
            if up_check_row >= 0 and board[up_check_row] == "#":
                for fill in range(up_check_row, index, col):
                    if board[fill] != "#":
                        board[fill] = "#"
                        loc_added.add(fill)
                        num_added += 1
            # Down
            down_check_row = index + col*step
            if down_check_row < len(board) and board[down_check_row] == "#":
                for fill in range(index, down_check_row, col):
                    if board[fill] != "#":
                        board[fill] = "#"
                        loc_added.add(fill)
                        num_added += 1
            # Left
            left_check_col = index - step
            if left_check_col >= 0 and board[left_check_col] == "#":
                for fill in range(left_check_col, index):
                    if board[fill] != "#" and board[fill] != "?":
                        board[fill] = "#"
                        loc_added.add(fill)
                        num_added += 1
            # Right
            right_check_col = index + step
            if right_check_col < col and board[right_check_col] == "#":
                for fill in range(index, right_check_col):
                    if board[fill] != "#" and board[fill] != "?":
                        board[fill] = "#"
                        loc_added.add(fill)
                        num_added += 1
    return board, num_added


# Add initial blocking squares (from input conditions)
def initial_blocking_squares(word_list, board):
    board = list(board)
    # Number of blocking squares specified by input
    count = 0
    # Locations of blocking squares specified by input
    blocking_square_locations = []
    for word_info in word_list:
        word_info = word_info.lower()
        # Find start row and col
        start_row = int(word_info[1:word_info.find("x")])
        start_col = int(
            ''.join([word_info[i] for i in range(word_info.find("x")+1, len(word_info)) if word_info[i].isdigit()]))
        # Finds input word (including #)
        word = "".join([word_info[i] for i in range(word_info.find("x") + 1, len(word_info))
                        if word_info[i].isalpha() or word_info[i] == "#"])
        # Horizontal
        index = 0
        if word_info[0] == "h":
            for c in range(start_col, start_col+len(word)):
                loc = (start_row+1)*col+1+c
                if word[index] == "#":
                    blocking_square_locations.append(loc)
                    count += 1
                board[loc] = word[index].upper()
                index += 1
        # Vertical
        elif word_info[0] == "v":
            for r in range(start_row, start_row+len(word)):
                loc = (r+1)*col+start_col+1
                if word[index] == "#":
                    blocking_square_locations.append(loc)
                    count += 1
                board[loc] = word[index].upper()
                index += 1
        # Propagates input blocking squares
    for loc in blocking_square_locations:
        board, add = propagate_blocking_squares(board, loc)
        count += add
    return ''.join(board), count


# Generates a list of blank spaces from input board that could be blocking squares (taking into account initial states)
def viable_blanks(board):
    blanks = list()
    for index in range(len(board)):
        # Can't pick center
        if num_blocking_squares % 2 == 0 and index == len(board)//2:
            continue
        # If blank
        if board[index] == "-":
            # If a letter is not < 3 spaces away
            if helper(board, index-1, index-4, -1) and helper(board, index+1, index+4, 1) and \
                    helper(board, index-col, index-4*col, -col) and helper(board, index+col, index+4*col, col):
                # Reflects and does the same check
                reflect_index = len(board)-1-index
                if board[reflect_index] == '-':
                    board[index] = "#"
                    if helper(board, reflect_index-1, reflect_index-4, -1) and helper(board, reflect_index+1, reflect_index+4, 1) and \
                             helper(board, reflect_index-col, reflect_index-4*col, -col) and helper(board, reflect_index+col, reflect_index+4*col, col):
                        # heappush(blanks, (abs(len(board)//2-index), index))
                        blanks.append(index)
                    board[index] = "-"
    return blanks


# Viable_blanks helper; returns true if start is a valid spot for a blocking square
def helper(board, start, stop, step):
    letters_between = False
    is_boundary = False
    for check_index in range(start, stop, step):
        # Checks to see if spot is too close to a letter near a blocking square (leading to a word <3 char)
        if board[check_index].isalpha():
            letters_between = True
        if board[check_index] == "?" or board[check_index] == "#":
            is_boundary = True
            break
    if is_boundary and letters_between:
        return False
    return True


# Adds all blocking squares through guess and check (randomly select a square, and if it doesn't work abort)
# Initial count is from input conditions
# Recursive (some arrangements make it impossible to place more squares, need to backtrack)
def add_blocking_squares(board, count):
    board = list(board)
    if count == num_blocking_squares:
        return "".join(board)
    if num_blocking_squares % 2 == 1 and board[len(board)//2] != "#":
        board[len(board)//2] = "#"
        count += 1
    blanks = viable_blanks(board)
    result = None
    while result is None:
        new_count = count
        # Bad end cases: no viable places for more blocking squares, or too many blocking squares
        if len(blanks) == 0 or new_count > num_blocking_squares:
            return None
        spot = choice(blanks)
        new_board = board.copy()
        new_board[spot] = "#"
        new_board, add = propagate_blocking_squares(new_board, spot)
        # Special case in which an odd board has its center filled by propagating w/ even # blocking squares
        if new_board[len(board)//2] == "#" and num_blocking_squares % 2 == 0 and len(board) % 2 == 1:
            blanks.remove(spot)
            blanks.remove(len(board)-spot-1)
            continue
        new_count += add+1
        result = add_blocking_squares(new_board, new_count)
        if result is None:
            blanks.remove(spot)
            blanks.remove(len(board)-spot-1)
        if result is not None:
            return result


# Checks to make sure the board isn't split into two
def check(board):
    if "-" not in set(board):
        return True
    rand_index = int(random()*len(board))
    while board[rand_index] != "-":
        rand_index = int(random()*len(board))
    board = list(board)
    board[rand_index] = "#"
    fringe = deque()
    fringe.append(rand_index)
    while len(fringe) != 0:
        index = fringe.popleft()
        if "-" not in set(board):
            return True
        # Get Children
        # Right
        if board[index+1] != "#" and board[index+1] != "?":
            fringe.append(index+1)
            board[index+1] = "#"
        # Left
        if board[index-1] != "#" and board[index-1] != "?":
            fringe.append(index-1)
            board[index-1] = "#"
        # Up
        if board[index-col] != "#" and board[index-col] != "?":
            fringe.append(index-col)
            board[index-col] = "#"
        # Down
        if board[index+col] != "#" and board[index+col] != "?":
            fringe.append(index+col)
            board[index+col] = "#"
    return False


# Initial Setup (takes command line arguments and sets global variables)
# Returns initial board, which contains all input words, blocking squares, and propagated squares
# Count is the number of initial blocking squares
def initial_setup():
    global row
    global col
    global num_blocking_squares
    global word_dictionary
    row = int(argv[1][:argv[1].find("x")])
    col = int(argv[1][argv[1].find("x") + 1:])
    num_blocking_squares = int(argv[2])
    word_dictionary = argv[3]
    board, count = initial_blocking_squares(argv[4:], generate_board())
    return board, count


# Gets all blank spots (used for build crossword)
def all_blanks(board):
    blanks = list()
    for index in range(len(board)):
        if board[index] == "-":
            blanks.append(index)
    return blanks


# Builds the crossword given the input dictionary (horizontal only)
def horizontal_build_crossword(board):
    board = list(board)
    # Puts all words into a list
    words = list()
    for item in open(word_dictionary):
        words.append(item.rstrip())
    blanks = all_blanks(board)
    while len(blanks) != 0:
        search = r""
        spot = choice(blanks)
        # Finds starting spot
        while board[spot] != "#" and board[spot] != "?":
            spot -= 1
        spot += 1
        starting_spot = spot
        # Creates regex string
        while board[spot] != "#" and board[spot] != "?":
            if board[spot] == "-":
                search += r"\w"
                blanks.remove(spot)
            else:
                search += board[spot]
            spot += 1
        word = ""
        # Searches for an appropriate word
        while len(word) == 0:
            for result in re.finditer(r"^"+search+"$", choice(words), re.I):
                if result.group(0).isalpha():
                    word = result.group(0)
        words.remove(word)
        index = 0
        # Puts in board
        while board[starting_spot] != "#" and board[starting_spot] != "?":
            board[starting_spot] = word[index].upper()
            index += 1
            starting_spot += 1
    display(board)


# Builds the crossword given the input dictionary
def build_crossword(board, words):
    board = list(board)
    # Puts all words into a list
    blanks = all_blanks(board)
    if len(blanks) == 0:
        return board
    search = r""
    initial_spot = choice(blanks)
    spot = initial_spot
    while board[spot] != "#" and board[spot] != "?":
        spot -= 1
    spot += 1
    starting_spot = spot
    while board[spot] != "#" and board[spot] != "?":
        if board[spot] == "-":
            search += r"\w"
            blanks.remove(spot)
        else:
            search += board[spot]
        spot += 1
    word = ""
    while len(word) == 0:
        for result in re.finditer(r"^"+search+"$", choice(words), re.I):
            if result.group(0).isalpha():
                word = result.group(0)
    words.remove(word)
    index = 0
    new_board = board.copy()
    while new_board[starting_spot] != "#" and new_board[starting_spot] != "?":
        new_board[starting_spot] = word[index].upper()
        index += 1
        starting_spot += 1
    result = build_crossword(new_board, words)
    if result is not None:
        return result


# Main
# Makes initial board with blocking squares
board_main, count_main = initial_setup()
end_board = add_blocking_squares(board_main, count_main)
while not check(end_board):
    end_board = add_blocking_squares(board_main, count_main)
# Generates the rest of the board
# words_list = list()
# for item in open(word_dictionary):
#     words_list.append(item.rstrip())
# end_board = build_crossword(end_board, words_list)
horizontal_build_crossword(end_board)

# result = None
# while result is None:
#     new_board = deepcopy(board_main)
#     result = add_blocking_squares(board_main, count_main)
# display(result)


# Tests to see if my input reading works
# board_test, count_test = initial_setup()
# print(row)
# print(col)
# print(num_blocking_squares)
# print(word_dictionary)
# display(board_test)
# print(count_test)
