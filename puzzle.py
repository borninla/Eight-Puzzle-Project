from random import *
from sys import maxsize
from copy import deepcopy

num_of_children_expanded = max_depth = 0

# ============ Puzzle Class ============ #


class Puzzle:
    goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    def __init__(self, puzzle_matrix, size):
        self.puzzle_matrix = puzzle_matrix
        self.size = size
        self.empty_pos_x, self.empty_pos_y = find_empty_tile(puzzle_matrix)

    def move_up(self):
        if 0 not in self.puzzle_matrix[0]:
            self.swap_tiles(self.empty_pos_x, self.empty_pos_y - 1)
            self.empty_pos_y -= 1
            return True
        else:
            return False

    def move_down(self):
        if 0 not in self.puzzle_matrix[self.size - 1]:
            self.swap_tiles(self.empty_pos_x, self.empty_pos_y + 1)
            self.empty_pos_y += 1
            return True
        else:
            return False

    def move_left(self):
        zero_not_in_leftmost_column = True
        for i in range(self.size):
            if self.puzzle_matrix[i][0] == 0:
                zero_not_in_leftmost_column = False
                break
        if zero_not_in_leftmost_column:
            self.swap_tiles(self.empty_pos_x - 1, self.empty_pos_y)
            self.empty_pos_x -= 1
            return True
        else:
            return False

    def move_right(self):
        zero_not_in_leftmost_column = True
        for i in range(self.size):
            if self.puzzle_matrix[i][self.size - 1] == 0:
                zero_not_in_leftmost_column = False
        if zero_not_in_leftmost_column:
            self.swap_tiles(self.empty_pos_x + 1, self.empty_pos_y)
            self.empty_pos_x += 1
            return True
        else:
            return False

    def swap_tiles(self, x_change, y_change):
        temp = self.puzzle_matrix[self.empty_pos_y][self.empty_pos_x]
        self.puzzle_matrix[self.empty_pos_y][self.empty_pos_x] = self.puzzle_matrix[y_change][x_change]
        self.puzzle_matrix[y_change][x_change] = temp

    def print(self):
        print_matrix(self.puzzle_matrix)

# ============ Tree/Node Classes ============


class Node:
    def __init__(self, puzzle, path_cost):
        self.puzzle = puzzle
        self.child = []
        self.path_cost = path_cost

    def create_children(self, num_of_children, new_puzzle_state, new_path_cost):
        for i in range(0, num_of_children):
            self.child.append(Node(new_puzzle_state, new_path_cost))

    # def set_children_values(self, list):
    #     for i in range(0, len(list)):
    #         self.data.append(list[i])


# ============ Helper Functions ============ #


def find_empty_tile(puzzle_matrix):
    for column in range(len(puzzle_matrix)):
        for row in range(len(puzzle_matrix[column])):
            if puzzle_matrix[column][row] == 0:
                return row, column


def init_random_puzzle(puzzle_matrix, size_of_matrix):
    used_numbers = []

    while len(puzzle_matrix) < size_of_matrix:
        current_row = []
        while len(current_row) < size_of_matrix:
            rand_num = randint(0, size_of_matrix ^ 2 - 1)
            if rand_num not in used_numbers:
                current_row.append(rand_num)
                used_numbers.append(rand_num)
        puzzle_matrix.append(current_row)

    print(puzzle_matrix)


def print_matrix(matrix):
    for row in matrix:
        print("\t" + ' '.join([str(elem) for elem in row]))


def run_interface():
    print("Welcome to Andrew Lvovsky's Eight-Puzzle Solver!")
    response = ""
    puzzle = None

    while response != "1" and response != "2":
        print("Type '1' to use a default puzzle, or '2' to enter your own puzzle")
        response = input()

        if response == "1":
            print("Using a default puzzle...")
            # Take a saved puzzle from an array and solve it
            default_puzzles = [
                [[4, 0, 3], [6, 8, 7], [5, 2, 1]],
                [[1, 6, 3], [2, 7, 0], [5, 4, 8]],
                [[8, 0, 5], [4, 3, 7], [1, 6, 2]],
                [[2, 5, 1], [8, 4, 0], [3, 7, 6]],
                [[7, 0, 2], [4, 6, 3], [8, 5, 1]],
            ]
            # Constructing Puzzle object directly
            puzzle = Puzzle(default_puzzles[randint(0, len(default_puzzles))], 3)
        elif response == "2":
            print("Enter your puzzle, use a zero to represent the blank.")
            first_row = input("Enter the first row, using a space between numbers: ")
            first_row = [int(s) for s in first_row.split() if s.isdigit()]
            second_row = input("Enter the second row, using a space between numbers: ")
            second_row = [int(s) for s in second_row.split() if s.isdigit()]
            third_row = input("Enter the third row, using a space between numbers: ")
            third_row = [int(s) for s in third_row.split() if s.isdigit()]

            puzzle = Puzzle([first_row, second_row, third_row], 3)
        else:
            print("'" + response + "' is not a valid response.")

    response = ""

    while response != "1" and response != "2" and response != "3":
        print("Enter your choice of algorithm:")
        print("\t1. Uniform Cost Search")
        print("\t2. A* w/ Misplaced Tile Heuristic")
        print("\t3. A* w/ Manhattan Distance Heuristic\n")
        response = input()
        print("")

        if response == "1":
            print("Running Uniform Cost Search on")
            puzzle.print()
            print("")
            node = general_search(response, puzzle, queueing_function)
        elif response == "2":
            print("Running A* w/ Misplaced Tile Heuristic")
            # run A* w/ Misplaced Tile Heuristic
        elif response == "3":
            print("Running A* w/ Manhattan Distance Heuristic")
            # run A* w/ Manhattan Distance Heuristic
        else:
            print("'" + response + "' is not a valid response.")

        if node:
            print("Winner Winner Chicken Dinner!")
            print("")
            print("Total nodes expanded: " + str(num_of_children_expanded))
            print("Max num of nodes in queue at any time: ")
            print("Depth of goal node: ")
        else:
            print("No solution was found.")


def puzzle_movement_test():
    goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    p = Puzzle(goal_state, 3)
    response = ""

    print("Move (u)p, (d)own, (l)eft, or (r)ight")

    while response != "q":
        response = input()
        if response == 'w':
            p.move_up()
        elif response == 's':
            p.move_down()
        elif response == 'a':
            p.move_left()
        elif response == 'd':
            p.move_right()
        p.print()

# ============ Search Functions ============ #


def remove_node(list_of_nodes):
    lowest_path_cost = index_of_node_to_remove = maxsize  # using sys.maxsize
    for i in range(len(list_of_nodes)):
        if list_of_nodes[i].path_cost < lowest_path_cost:
            lowest_path_cost = list_of_nodes[i].path_cost
            index_of_node_to_remove = i
    node_to_return = list_of_nodes[index_of_node_to_remove]
    list_of_nodes.pop(index_of_node_to_remove)
    return node_to_return, index_of_node_to_remove


def copy_new_node_into_list(node, children_list):
    new_child = deepcopy(node)  # creates a child node by copying parent node with new legal move
    new_child.path_cost += 1    # increments path cost (g(n))
    children_list.append(new_child)


def expand_node(node):
    children = []

    if node.puzzle.move_up():
        copy_new_node_into_list(node, children)
        node.puzzle.move_down()     # resets move to original pos so future moves can be made
    if node.puzzle.move_down():
        copy_new_node_into_list(node, children)
        node.puzzle.move_up()
    if node.puzzle.move_left():
        copy_new_node_into_list(node, children)
        node.puzzle.move_right()
    if node.puzzle.move_right():
        copy_new_node_into_list(node, children)
        node.puzzle.move_left()

    global num_of_children_expanded
    num_of_children_expanded += len(children)
    return children


def queueing_function(response, index, node_list, node):

    children_nodes = expand_node(node)

    if response == "1":
        for child in children_nodes:
            node_list.insert(index, child)
            index += 1
        return node_list


def general_search(response, problem, queueing_func):
    nodes = [Node(problem, 0)]    # path_cost (g(n)) set to 0
    while True:
        if not nodes:   # if no nodes, return failure
            return -1
        (node, index) = remove_node(nodes)
        if problem.goal_state == node.puzzle.puzzle_matrix:
            return node

        print("The best state to expand with a g(n) = " + str(node.path_cost) + " and h(n) = 0 is...")
        node.puzzle.print()
        print("Expanding this node...")
        print("")

        nodes = queueing_func(response, index, nodes, node)

# ============ Main ============ #


def main():
    run_interface()


main()
