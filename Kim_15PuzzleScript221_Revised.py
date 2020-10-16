import time
import sys
from collections import deque
from heapq import heappush, heappop
from random import randint
from random import choice
goal = "0ABCDEFGHIJKLMNO"
size = 4


# Finds shortest path from input puzzle to goal state (using bfs)
def bfs_length(puzzle):
    # nodes = 0
    fringe = deque()
    fringe.append((puzzle, 0))
    visited = set()
    visited.add(puzzle)
    while len(fringe) != 0:
        current_state, depth = fringe.popleft()
        if current_state == goal:
            return depth  # ,nodes
        for child, move in get_children(current_state):
            if child not in visited:
                # nodes += 1
                fringe.append((child, depth+1))
                visited.add(child)
    return "No path"


# Finds shortest path from input puzzle to goal state (using k-dfs)
def k_dfs(puzzle, k):
    # nodes = 0
    fringe = list()
    start_info = (puzzle, 0, set(), "")
    start_info[2].add(puzzle)
    fringe.append(start_info)
    while len(fringe) != 0:
        current_state, depth, ancestors_set, moves_list = fringe.pop()
        if current_state == goal:
            return depth  # nodes
        if depth < k:
            for child in get_children(current_state):
                child_state, move = child
                if child_state not in ancestors_set:
                    # nodes += 1
                    ancestors = ancestors_set.copy()
                    ancestors.add(child_state)
                    moves = moves_list
                    moves += move
                    fringe.append((child_state, depth + 1, ancestors, moves))
    return None


# Finds the shortest path from the input to goal state using ID-DFS
def iterative_deepening(puzzle, max_depth):
    # total_nodes = 0
    for k in range(1, max_depth):
        dfs_info = k_dfs(puzzle, k)
        # Code used to calculate nodes per second
        # total_nodes += dfs_info[0]
        # if dfs_info[1] is not None:
        #     return dfs_info[1], total_nodes
        if dfs_info is not None:
            return dfs_info
    return None


# Finds shortest path from input puzzle to goal state (used for turn-in) using an informed search
def a_star(puzzle):
    # nodes = 0
    fringe = list()
    fringe.append((taxi_cab(puzzle), puzzle, 0, ""))
    visited = set()
    while len(fringe) != 0:
        taxi, current_state, depth, path = heappop(fringe)
        if current_state == goal:
            return depth  # ,nodes
        if current_state in visited:
            continue
        visited.add(current_state)
        for child in get_children_a_star(current_state):
            child_state, move, taxi_change = child
            if child_state not in visited:
                # nodes += 1
                moves = path
                moves += move
                heappush(fringe, (taxi + taxi_change + 1, child_state, depth+1, moves))
    return "No path"


# Finds shortest path from input puzzle to goal state by using bfs from both the start and end
def bfs_symmetric(puzzle):
    # total_nodes = 0
    start_fringe = deque()
    end_fringe = deque()
    start_fringe.append((puzzle, 0))
    end_fringe.append((goal, 0))
    start_visited = dict()
    start_visited[puzzle] = 0
    end_visited = dict()
    end_visited[goal] = 0
    while len(start_fringe) != 0 and len(end_fringe) != 0:
        start_state = start_fringe.popleft()
        end_state = end_fringe.popleft()
        # if start_state[0] in end_visited.keys():
        #     return start_state[1] + end_visited[start_state[0]]
        if end_state[0] in start_visited.keys():
            return end_state[1] + start_visited[end_state[0]]  # ,total_nodes
        for child in get_children(start_state[0]):
            if child[0] not in start_visited.keys():
                # total_nodes += 1
                start_fringe.append((child[0], start_state[1]+1))
                start_visited[child[0]] = start_state[1] + 1
        for child in get_children(end_state[0]):
            if child[0] not in end_visited.keys():
                # total_nodes += 1
                end_fringe.append((child[0], end_state[1]+1))
                end_visited[child[0]] = end_state[1] + 1
    return "No path"


# Finds shortest path from input puzzle to goal state (used for turn-in) using an informed search (exploration 4)
def a_star_rand(puzzle):
    fringe = list()
    fringe.append((taxi_cab(puzzle), randint(1, 1000), puzzle, 0, ""))
    visited = set()
    while len(fringe) != 0:
        taxi, rand, current_state, depth, path = heappop(fringe)
        if current_state == goal:
            return depth
        if current_state in visited:
            continue
        visited.add(current_state)
        for child in get_children_a_star(current_state):
            child_state, move, taxi_change = child
            if child_state not in visited:
                moves = path
                moves += move
                heappush(fringe, (taxi + taxi_change + 1, randint(1, 1000), child_state, depth+1, moves))
    return "No path"


# Finds shortest path from input puzzle to goal state (used for turn-in) using an informed search (exploration 5)
def a_star_multiplier(puzzle, m):
    fringe = list()
    fringe.append((taxi_cab(puzzle), randint(1, 1000), puzzle, 0, ""))
    visited = set()
    while len(fringe) != 0:
        taxi, rand, current_state, depth, path = heappop(fringe)
        if current_state == goal:
            return depth
        if current_state in visited:
            continue
        visited.add(current_state)
        for child in get_children_a_star(current_state):
            child_state, move, taxi_change = child
            if child_state not in visited:
                moves = path
                moves += move
                heappush(fringe, ((taxi-m*depth+taxi_change)+m*(depth+1), randint(1, 1000),
                                  child_state, depth+1, moves))
    return "No path"


# Uses buckets instead of a priority queue with A* (exploration E)
def bucket_a_star(puzzle):
    fringe = list()
    fringe.append(list())
    initial_taxi = taxi_cab(puzzle)
    start_index = 0
    fringe[0].append((initial_taxi, puzzle, 0, ""))
    visited = set()
    while len(fringe) != 0:
        if len(fringe[start_index]) == 0:
            start_index += 1
        taxi, current_state, depth, path = fringe[start_index].pop(len(fringe[start_index])-1)
        if current_state == goal:
            return depth
        if current_state in visited:
            continue
        visited.add(current_state)
        for child in get_children_a_star(current_state):
            child_state, move, taxi_change = child
            if child_state not in visited:
                moves = path
                moves += move
                new_heuristic = taxi+taxi_change+1
                calc = (new_heuristic-initial_taxi)//2
                if calc > len(fringe)-1:
                    fringe.append(list())
                fringe[calc].append((new_heuristic, child_state, depth + 1, moves))
    return "No path"


# Swaps the elements at the two input indices in the input list
def swap(input_list, index1, index2):
    temp = input_list[index1]
    input_list[index1] = "0"
    input_list[index2] = temp


# Returns all states one move away from the input state as well as the direction the blank moved
def get_children(state):
    blank_index = state.index("0")
    children_list = []
    if blank_index+size < size**2:  # Move Down
        chars = list(state)
        swap(chars, blank_index+size, blank_index)
        children_list.append((''.join(chars), 'D'))
    if blank_index-size >= 0:  # Move Up
        chars = list(state)
        swap(chars, blank_index-size, blank_index)
        children_list.append((''.join(chars), 'U'))
    if (blank_index+1) % size != 0:  # Move Right
        chars = list(state)
        swap(chars, blank_index+1, blank_index)
        children_list.append((''.join(chars), 'R'))
    if blank_index % size != 0:  # Move Left
        chars = list(state)
        swap(chars, blank_index-1, blank_index)
        children_list.append((''.join(chars), 'L'))
    return children_list


# Returns all states one move away from the input state, the direction the blank moved, and the change in taxicab
# distance
def get_children_a_star(state):
    blank_index = state.index("0")
    children_list = []
    if blank_index+size < size**2:  # Move Down
        chars = list(state)
        taxi_change = helper_taxi(state, blank_index+size, blank_index)
        swap(chars, blank_index+size, blank_index)
        children_list.append((''.join(chars), 'D', taxi_change))
    if blank_index-size >= 0:  # Move Up
        chars = list(state)
        taxi_change = helper_taxi(state, blank_index-size, blank_index)
        swap(chars, blank_index-size, blank_index)
        children_list.append((''.join(chars), 'U', taxi_change))
    if (blank_index+1) % size != 0:  # Move Right
        chars = list(state)
        taxi_change = helper_taxi(state, blank_index+1, blank_index)
        swap(chars, blank_index+1, blank_index)
        children_list.append((''.join(chars), 'R', taxi_change))
    if blank_index % size != 0:  # Move Left
        chars = list(state)
        taxi_change = helper_taxi(state, blank_index-1, blank_index)
        swap(chars, blank_index-1, blank_index)
        children_list.append((''.join(chars), 'L', taxi_change))
    return children_list


# Finds the sum taxicab distance for the input puzzle
def taxi_cab(puzzle):
    sum_taxicab = 0
    for letter in puzzle:
        if letter != '0':
            puzzle_index = puzzle.index(letter)
            goal_index = goal.index(letter)
            puzzle_row = puzzle_index//size
            goal_row = goal_index//size
            sum_taxicab += abs(puzzle_row - goal_row) + abs((puzzle_index - size*puzzle_row) -
                                                            (goal_index - size*goal_row))
    return sum_taxicab


# Finds the change in taxi_cab distance from one child to the next (optimization)
def helper_taxi(puzzle, index1, index2):
    goal_state_index = goal.index(puzzle[index1])
    goal_row = goal_state_index//size
    initial_row = index1//size
    end_row = index2//size
    if abs(initial_row-goal_row) + abs((index1-size*initial_row) - (goal_state_index-size*goal_row)) \
            > abs(end_row - goal_row) + abs((index2-size*end_row) - (goal_state_index-size*goal_row)):
        return -1
    return 1


# Generates a random list of 8 puzzles with increasing solution length; used for exploration C
def create_8_puzzles():
    puzzle_list = []
    fringe = deque()
    fringe.append((goal, 0))
    puzzle_length = dict()
    puzzle_length[0] = [goal]
    visited = set()
    visited.add(goal)
    while len(fringe) != 0:
        current_state, depth = fringe.popleft()
        for child, move in get_children(current_state):
            if child not in visited:
                fringe.append((child, depth+1))
                if depth+1 not in puzzle_length.keys():
                    puzzle_length[depth+1] = list()
                puzzle_length[depth+1].append(child)
                visited.add(child)
    for key in puzzle_length.keys():
        puzzle_list.append(choice(puzzle_length[key]))
    return puzzle_list


# Exploration 5
# start = time.perf_counter()
# data = a_star_multiplier("FIBEALDKJCNGHM0O", 0.6)
# end = time.perf_counter()
# print(data, (end-start))


# Exploration C (change goal to 0ABCDEFGH and size to 3 at the top)
# puzzles = create_8_puzzles()
# print("A*")
# for element in puzzles:
#     start = time.process_time()
#     info = a_star(element)
#     end = time.process_time()
#     print(info, end-start)
# print("BFS")
# for element in puzzles:
#     start = time.process_time()
#     info = bfs_length(element)
#     end = time.process_time()
#     print(info, end-start)
# print("Bidirectional BFS")
# for element in puzzles:
#     start = time.process_time()
#     info = bfs_symmetric(element)
#     end = time.process_time()
#     print(info, end-start)
# print("ID_DFS")
# for element in puzzles:
#     start = time.process_time()
#     info = iterative_deepening(element, 32)
#     end = time.process_time()
#     print(info, end-start)


# Korf100 Required Exploration Code
# file = open(sys.argv[1])
# for line in file:
#     info = line.split()
#     if len(info) == 0:
#         break
#     puzzle_input = info[0]
#     start = time.perf_counter()
#     length = a_star_multiplier(puzzle_input, 0.8)
#     stop = time.perf_counter()
#     print(length)  # , "Korf100", (stop-start))


# Bucket A* Code
# file = open(sys.argv[1])
# for line in file:
#     info = line.split()
#     if len(info) == 0:
#         break
#     puzzle_input = info[0]
#     start = time.perf_counter()
#     length = bucket_a_star(puzzle_input)
#     stop = time.perf_counter()
#     print(length, "Bucket A*", (stop-start))


# Turn in Code
file = open(sys.argv[1])
for line in file:
    info = line.split()
    if len(info) == 0:
        break
    puzzle_input = info[1]
    algorithm = info[0]
    if algorithm == "B":
        start = time.perf_counter()
        length = bfs_length(puzzle_input)
        stop = time.perf_counter()
        print(length, "BFS", (stop-start))
    elif algorithm == "I":
        start = time.perf_counter()
        length = iterative_deepening(puzzle_input, 100)
        stop = time.perf_counter()
        print(length, "ID_DFS", (stop-start))
    elif algorithm == "2":
        start = time.perf_counter()
        length = bfs_symmetric(puzzle_input)
        stop = time.perf_counter()
        print(length, "Bi-directional BFS", (stop-start))
    elif algorithm == "A":
        start = time.perf_counter()
        length = a_star(puzzle_input)
        stop = time.perf_counter()
        print(length, "A*", (stop-start))
    elif algorithm == "7":
        start = time.perf_counter()
        length = a_star_multiplier(puzzle_input, 0.7)
        stop = time.perf_counter()
        print(length, "A* with 0.7 multiplier", (stop-start))
    elif algorithm == "!":
        start = time.perf_counter()
        length = bfs_length(puzzle_input)
        stop = time.perf_counter()
        print(length, "BFS", (stop - start))
        start = time.perf_counter()
        length = iterative_deepening(puzzle_input, 100)
        stop = time.perf_counter()
        print(length, "ID_DFS", (stop - start))
        start = time.perf_counter()
        length = bfs_symmetric(puzzle_input)
        stop = time.perf_counter()
        print(length, "Bi-directional BFS", (stop - start))
        start = time.perf_counter()
        length = a_star(puzzle_input)
        stop = time.perf_counter()
        print(length, "A*", (stop - start))
        start = time.perf_counter()
        length = a_star_multiplier(puzzle_input, 0.7)
        stop = time.perf_counter()
        print(length, "A* with 0.7 multiplier", (stop - start))
