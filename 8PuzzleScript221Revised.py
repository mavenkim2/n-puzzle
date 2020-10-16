# Maven Kim Artificial Intelligence Period 2 #221 9/17/18
# 1 Methods and Functionality
from collections import deque
from random import choice
from random import randint
import sys
import time
goal = "012345678"
size = 3


# Returns a list of game states one move away from state
def get_children(state):
    blank_index = state.index("0")
    children_list = []
    if blank_index+size < size**2:  # Move Down
        chars = list(state)
        temp = chars[blank_index+size]
        chars[blank_index+size] = "0"
        chars[blank_index] = temp
        children_list.append((''.join(chars), "D"))
    if blank_index-size >= 0:  # Move Up
        chars = list(state)
        temp = chars[blank_index-size]
        chars[blank_index-size] = "0"
        chars[blank_index] = temp
        children_list.append((''.join(chars), "U"))
    if (blank_index+1) % size != 0:  # Move Right
        chars = list(state)
        temp = chars[blank_index+1]
        chars[blank_index+1] = "0"
        chars[blank_index] = temp
        children_list.append((''.join(chars), "R"))
    if blank_index % size != 0:  # Move Left
        chars = list(state)
        temp = chars[blank_index-1]
        chars[blank_index-1] = "0"
        chars[blank_index] = temp
        children_list.append((''.join(chars), "L"))
    return children_list


# Tests to see if state is the goal state
def goal_test(state):
    if goal == state:
        return True
    return False


# Prints out state in a grid
def print_puzzle(state):
    print(state[:size] + "\n" + state[size:size*2] + "\n" + state[size*2:size*3])


# 2: Number of winnable game states (all game states that can be reached from goal state)
def part2():
    fringe = deque()
    fringe.append(goal)
    visited = set()
    visited.add(goal)
    while len(fringe) != 0:
        current_state = fringe.popleft()
        for state in get_children(current_state):
            if state[0] not in visited:
                fringe.append(state[0])
                visited.add(state[0])
    print(len(visited))


# 3: Generate a random game state and random solvable game state
def gen_state():
    puzzle = ""
    nums = [num for num in range(0, size**2)]
    while len(puzzle) < size ** 2:
        random = choice(nums)
        puzzle += str(random)
        nums.remove(random)
    return puzzle


# Generates a solvable game state
def gen_solve_state():
    fringe = deque()
    fringe.append(goal)
    visited = set()
    visited.add(goal)
    while len(fringe) != 0:
        current_state = fringe.popleft()
        for child in get_children(current_state):
            if child[0] not in visited:
                fringe.append(child[0])
                visited.add(child[0])
    return choice(tuple(visited))


# 4: Returns a list of board states based on the input moves and initial state
# Used for dfs and bfs to find past states
def move(puzzle, direction_list):
    board_states = []
    current_state = puzzle
    for direction in direction_list:
        if direction == "D":
            blank_index = current_state.index("0")
            chars = list(current_state)
            temp = chars[blank_index+size]
            chars[blank_index+size] = "0"
            chars[blank_index] = temp
            current_state = ''.join(chars)
            board_states.append(current_state)
        elif direction == "U":
            blank_index = current_state.index("0")
            chars = list(current_state)
            temp = chars[blank_index-size]
            chars[blank_index-size] = "0"
            chars[blank_index] = temp
            current_state = ''.join(chars)
            board_states.append(current_state)
        elif direction == "R":
            blank_index = current_state.index("0")
            chars = list(current_state)
            temp = chars[blank_index+1]
            chars[blank_index+1] = "0"
            chars[blank_index] = temp
            current_state = ''.join(chars)
            board_states.append(current_state)
        elif direction == "L":
            blank_index = current_state.index("0")
            chars = list(current_state)
            temp = chars[blank_index-1]
            chars[blank_index-1] = "0"
            chars[blank_index] = temp
            current_state = ''.join(chars)
            board_states.append(current_state)
    return board_states


# Find shortest path using BFS from any given state to the solution state; returns path length
def try_solve_length_bfs(puzzle):
    fringe = deque()
    fringe.append((puzzle, 0))
    visited = set()
    visited.add(puzzle)
    while len(fringe) != 0:
        current_state = fringe.popleft()
        if goal_test(current_state[0]):
            # print("Path length:", current_state[1])
            return current_state[1]
        for child in get_children(current_state[0]):
            if child[0] not in visited:
                fringe.append((child[0], current_state[1]+1))
                visited.add(child[0])
    # print("No path")
    return "No path"


# Finds shortest path from any given state to the solution state; returns path length and solution
def try_solve_actions_bfs_helper(puzzle):
    fringe = deque()
    fringe.append((puzzle, 0, list()))
    visited = set()
    visited.add(puzzle)
    while len(fringe) != 0:
        current_state = fringe.popleft()
        if goal_test(current_state[0]):
            # print("Path length:", current_state[1])
            # print(''.join(current_state[2]))
            return current_state[1], current_state[2]
        for state in get_children(current_state[0]):
            if state[0] not in visited:
                direction_list = current_state[2].copy()
                direction_list.append(state[1])
                fringe.append((state[0], current_state[1]+1, direction_list))
                visited.add(state[0])
    # print("No path")
    return "No path"


# Finds the shortest path from the puzzle to the goal state; returns path length, solution, and past states
def try_solve_actions_bfs(puzzle):
    bfs_info = try_solve_actions_bfs_helper(puzzle)
    if bfs_info == "No path":
        return "No path"
    return bfs_info[0], bfs_info[1], move(puzzle, bfs_info[1])


# 5 Generate 100 to 1000 random starting positions and try to solve them
def part5():
    max_length = 0
    total_length = 0
    num_pos = randint(100, 1000)
    num_unsolvable = 0
    for num in range(0, num_pos):
        game_state = gen_state()
        new_length = try_solve_length_bfs(game_state)
        if new_length == "No path":
            num_unsolvable += 1
        elif new_length > max_length:
            max_length = new_length
            total_length += new_length
        else:
            total_length += new_length
    print("Avg Length: ", total_length/(num_pos-num_unsolvable))
    print("Max Length: ", max_length)
    print("Fraction solvable: ", (num_pos - num_unsolvable)/num_pos)


# 6 Find the hardest 8-puzzle using breadth first search
def part6():
    fringe = deque()
    fringe.append((goal, 0, []))
    visited = set()
    visited.add(goal)
    max_length = 0
    hardest_puzzle = ()
    while len(fringe) != 0:
        current_state = fringe.popleft()
        for child in get_children(current_state[0]):
            if child[0] not in visited:
                direction_list = current_state[2].copy()
                direction_list.append(child[1])
                fringe.append((child[0], current_state[1] + 1, direction_list))
                visited.add(child[0])
                if current_state[1] + 1 > max_length:
                    max_length = current_state[1] + 1
                    hardest_puzzle = fringe[len(fringe)-1]
    directions = []
    for index in range(len(hardest_puzzle[2]) - 1, 0, -1):
        if hardest_puzzle[2][index] == "U":
            directions.append("D")
        elif hardest_puzzle[2][index] == "D":
            directions.append("U")
        elif hardest_puzzle[2][index] == "L":
            directions.append("R")
        elif hardest_puzzle[2][index] == "R":
            directions.append("L")
    # print("Hardest Puzzle: ")
    # print_puzzle(hardest_puzzle[0])
    # print("Path length:", hardest_puzzle[1])
    # print("Solution:", ''.join(directions))
    return hardest_puzzle[0], hardest_puzzle[1], directions


# 7: Find shortest path using DFS from any given state to the solution state; returns path length
def try_solve_length_dfs(puzzle):
    fringe = list()
    fringe.append((puzzle, 0))
    visited = set()
    while len(fringe) != 0:
        current_state = fringe.pop()
        visited.add(current_state[0])
        if goal_test(current_state[0]):
            # print("Path length:", current_state[1])
            return current_state[1]
        for child in get_children(current_state[0]):
            if child[0] not in visited:
                fringe.append((child[0], current_state[1]+1))
    # print("No path")
    return "No path"


# Finds shortest path from any given state to the solution state; returns path length and solution
def try_solve_actions_dfs_helper(puzzle):
    fringe = list()
    fringe.append((puzzle, 0, ""))
    visited = set()
    while len(fringe) != 0:
        current_state = fringe.pop()
        visited.add(current_state[0])
        if goal_test(current_state[0]):
            # print("Path length:", current_state[1])
            # print(''.join(current_state[2]))
            return current_state[1], current_state[2]
        for state in get_children(current_state[0]):
            if state[0] not in visited:
                direction_list = current_state[2]
                direction_list += state[1]
                fringe.append((state[0], current_state[1]+1, direction_list))
    # print("No path")
    return "No path"


# Returns the path length, the solution to the input puzzle, and the past board states
def try_solve_actions_dfs(puzzle):
    dfs_info = try_solve_actions_dfs_helper(puzzle)
    if dfs_info == "No path":
        return "No path"
    return dfs_info[0], dfs_info[1], move(puzzle, dfs_info[1])


# 9 Find all states by length
# Index 0 will contain the states 1 move away, index 1 will contain states 2 moves away, etc.
def part9():
    fringe = deque()
    fringe.append((goal, 0))
    visited = set()
    visited.add(goal)
    states_list = []
    while len(fringe) != 0:
        current_state = fringe.popleft()
        for state in get_children(current_state[0]):
            if state[0] not in visited:
                if current_state[1] + 1 > len(states_list):
                    states_list.append(1)
                else:
                    states_list[current_state[1]] = states_list[current_state[1]] + 1
                fringe.append((state[0], current_state[1] + 1))
                visited.add(state[0])
    print(states_list)


# 11 Parity Checker; returns 0 if solvable, 1 if not (used for turn in)
def parity_check(puzzle, input_goal, puzzle_size):
    parity = 0
    for index in range(0, len(puzzle)-1):
        if puzzle[index] == '0':
            continue
        for index2 in range(index+1, len(puzzle)):
            if puzzle[index2] != '0' and puzzle[index] > puzzle[index2]:
                parity += 1
    goal_parity = 0
    for index in range(0, len(input_goal)-1):
        if input_goal[index] == '0':
            continue
        for index2 in range(index+1, len(input_goal)):
            if input_goal[index2] != '0' and input_goal[index] > input_goal[index2]:
                goal_parity += 1
    # Parity check for odd sized boards (parity in goal state and the puzzle must either be both even or odd)
    if puzzle_size % 2 == 1:
        if parity % 2 == 0 and goal_parity % 2 == 0:
            return 0
        elif parity % 2 == 1 and goal_parity % 2 == 1:
            return 0
        else:
            return 1
    else:
        # Parity check for even sized boards (depends on parity of goal state, the puzzle, and location
        # of zeroes in both)
        if ((input_goal.index("0")//puzzle_size) % 2 == 0 and goal_parity % 2 == 0) or \
                ((input_goal.index("0")//puzzle_size) % 2 == 1 and goal_parity % 2 == 1):
            if (puzzle.index("0")//puzzle_size) % 2 == 0 and parity % 2 == 0:
                return 0
            elif (puzzle.index("0")//puzzle_size) % 2 == 1 and parity % 2 == 1:
                return 0
            else:
                return 1
        else:
            if (puzzle.index("0")//puzzle_size) % 2 == 0 and parity % 2 == 1:
                return 0
            elif (puzzle.index("0")//puzzle_size) % 2 == 1 and parity % 2 == 0:
                return 0
            else:
                return 1


# Finds shortest path from input puzzle to goal state (used for turn-in)
def bfs_length(puzzle, input_goal, input_board_size):
    fringe = deque()
    fringe.append((puzzle, 0))
    visited = set()
    visited.add(puzzle)
    while len(fringe) != 0:
        current_state = fringe.popleft()
        if current_state[0] == input_goal:
            return current_state[1]
        for child in getchildren(current_state[0], input_board_size):
            if child not in visited:
                fringe.append((child, current_state[1]+1))
                visited.add(child)
    return "No path"


# Returns all states one move away from the input state (used for turn-in)
def getchildren(state, input_size):
    blank_index = state.index("0")
    children_list = []
    if blank_index+input_size < input_size**2:  # Move Down
        chars = list(state)
        temp = chars[blank_index+input_size]
        chars[blank_index+input_size] = "0"
        chars[blank_index] = temp
        children_list.append(''.join(chars))
    if blank_index-input_size >= 0:  # Move Up
        chars = list(state)
        temp = chars[blank_index-input_size]
        chars[blank_index-input_size] = "0"
        chars[blank_index] = temp
        children_list.append(''.join(chars))
    if (blank_index+1) % input_size != 0:  # Move Right
        chars = list(state)
        temp = chars[blank_index+1]
        chars[blank_index+1] = "0"
        chars[blank_index] = temp
        children_list.append(''.join(chars))
    if blank_index % input_size != 0:  # Move Left
        chars = list(state)
        temp = chars[blank_index-1]
        chars[blank_index-1] = "0"
        chars[blank_index] = temp
        children_list.append(''.join(chars))
    return children_list


# Turn in Code
file = open(sys.argv[1])
overall_time = 0
for line in file:
    info = line.split()
    if len(info) == 0:
        break
    board_size = info[0]
    puzzle_goal = info[2]
    puzzle_input = info[1]
    parity_start = time.process_time()
    parity_test = parity_check(puzzle_input, puzzle_goal, int(board_size))
    parity_end = time.process_time()
    if parity_test == 0:
        start = time.process_time()
        length = bfs_length(puzzle_input, puzzle_goal, int(board_size))
        end = time.process_time()
        print("Length of Shortest Path:", length)
        print("Seconds to run:", (end-start))
        overall_time += (end-start)
    else:
        print("No solution")
        print("Seconds to run:", (parity_end-parity_start))
        overall_time += (parity_end-parity_start)
print("Total number of seconds to process all input pairs:", overall_time)
