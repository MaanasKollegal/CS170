# Eight Puzzle Solver — CS 170, Project 1
# Name: Maanas Kollegal
# SID:  862380535
# Date: February 13, 2026
#
# Resources consulted:
# - CS 170 class slides
# - Python docs: heapq (https://docs.python.org/3/library/heapq.html)
# - Python docs: copy module (deepcopy)


import heapq
import copy
import time


#Goal State table which represents the solved puzzle
Goal_State = [
[1, 2, 3],
[4, 5, 6],
[7, 8, 0]
]


#Computes goal positions for heuristic calculation 
Goal_Position = {}
for r, row in enumerate(Goal_State):
    for c, val in enumerate(row):
        Goal_Position[val] = (r, c)

N_Rows = len(Goal_State)
N_Cols = len(Goal_State[0])

    
#Returns true if goal state is reached
def GoalTest(state):
    return state == Goal_State

#Finds and returns the location of the blank tile
def find_blank(state):
    for r in range(N_Rows):
        for c in range(N_Cols):
            if state[r][c] == 0:
                return r, c
    raise ValueError("No blank tile found.")

# Swaps blank tile with target position; returns None if move is out of bounds
def MakeMove(state, r, c, nr, nc):
    if nr < 0 or nr >= N_Rows or nc < 0 or nc >= N_Cols:
        return None
    new_state = copy.deepcopy(state)
    new_state[r][c], new_state[nr][nc] = new_state[nr][nc], new_state[r][c]
    return new_state

#Move tile up
def move_up(state):
    r, c = find_blank(state)
    return MakeMove(state, r, c, r - 1, c)

#Move tile down
def move_down(state):
    r, c = find_blank(state)
    return MakeMove(state, r, c, r + 1, c)

#Move tile left
def move_left(state):
    r, c = find_blank(state)
    return MakeMove(state, r, c, r, c - 1)

#Move tile right
def move_right(state):
    r, c = find_blank(state)
    return MakeMove(state, r, c, r, c + 1)


OPERATORS = [move_up, move_down, move_left, move_right]    



def CreateNode(state, parent=None, g=0, h=0, depth=0): #Creates a search node dictionary, f = g + h
    return{
        "state": state,
        "parent": parent,
        "g": g, #cost
        "h": h, #cost estimate 
        "f": g + h, #total cost
        "depth": depth
    }


def CreateQueue(node): #Creates the queue which starts out with one node
    counter = [0]
    return[(node["f"], 0, node)], counter


#Uniform cost search, always returns 0
def H_Zero(state):
    return 0

#Counts tiles which are misplaced (tiles that are not in the goal position)
def H_MisplacedTile(state):
    count = 0
    for r in range(N_Rows):
        for c in range(N_Cols):
            val = state[r][c]
            if val != 0 and state[r][c] != Goal_State[r][c]:
                count += 1 
    return count


#Finds Manhattan Distance
#Sum of |current_row - goal_row| + |current_col - goal_col| for each non-blank tile.
def H_Manhattan(state):
    total = 0
    for r in range(N_Rows):
        for c in range(N_Cols):
            val = state[r][c]
            if val != 0:
                gr, gc = Goal_Position[val]
                total += abs(r - gr) + abs(c - gc)
    return total


#Creates children nodes by using each operator
def Expand(node, operators):
    children = []
    for op in operators:
        new_state = op(node['state'])
        if new_state is not None:
            child = CreateNode(
                state=new_state,
                parent=node,
                g=node['g'] + 1,   # unit cost
                h=0,                # heuristic set by queueing function
                depth=node['depth'] + 1
            )
            children.append(child)
    return children
    

#Uniform Cost Search, orders nodes by g(n)
def QueueingUniformCost(nodes, counter, new_nodes):
    for child in new_nodes:
        child['h'] = H_Zero(child['state'])
        child['f'] = child['g'] + child['h']
        heapq.heappush(nodes, (child['f'], counter[0], child))
        counter[0] += 1
    return nodes


#Orders nodes by f(n) = g(N) + H_misplaced(n)
def QueueingMisplacedTile(nodes, counter, new_nodes):
    for child in new_nodes:
        child['h'] = H_MisplacedTile(child['state'])
        child['f'] = child['g'] + child['h']
        heapq.heappush(nodes, (child['f'], counter[0], child))
        counter[0] += 1
    return nodes


#Orders nodes by f(n) = g(n) + H_Manhattan(n)
def QueueingManhattan(nodes, counter, new_nodes):
    for child in new_nodes:
        child['h'] = H_Manhattan(child['state'])
        child['f'] = child['g'] + child['h']
        heapq.heappush(nodes, (child['f'], counter[0], child))
        counter[0] += 1
    return nodes


#Converts a 2-D list state into a hashable tuple-of-tuples.
def state_to_tuple(state):
    return tuple(tuple(row) for row in state)

#Prints state of puzzle
def print_state(state):
    for row in state:
        print('  ' + ' '.join(str(v) if v != 0 else '_' for v in row))

#Based on pseudocode provided in instructions
def GeneralSearch(problem, queueing_function, verbose=True):
 
    initial_node = CreateNode(problem['initial_state'])
    nodes, counter = CreateQueue(initial_node)

    nodes_expanded = 0
    max_queue_size = 1
    visited = set() # closed list

    while True:
        #if EMPTY(nodes) then return "failure"
        if not nodes:
            return "failure", nodes_expanded, max_queue_size

        #node = REMOVE-FRONT(nodes)
        _, _, node = heapq.heappop(nodes)

        state_key = state_to_tuple(node['state'])
        if state_key in visited:
            # Already expanded a cheaper path to this state; skip.
            continue
        visited.add(state_key)

        # if problem.GOAL-TEST(node.STATE) succeeds then return node
        if problem['GoalTest'](node['state']):
            return node, nodes_expanded, max_queue_size

        nodes_expanded += 1

        if verbose:
            print(f"  Expanding: g(n)={node['g']}, h(n)={node['h']}, "
                  f"f(n)={node['f']}")
            print_state(node['state'])
            print()

        # nodes = QUEUEING-FUNCTION(nodes, EXPAND(node, problem.OPERATORS)) 
        new_nodes = Expand(node, problem['operators'])
        # Filter already-visited children before inserting
        new_nodes = [c for c in new_nodes
                     if state_to_tuple(c['state']) not in visited]
        nodes = queueing_function(nodes, counter, new_nodes)

        max_queue_size = max(max_queue_size, len(nodes))

#Prints a summary of the search result
def print_solution(result, nodes_expanded, max_queue_size, elapsed):
    print("\n" + "=" * 45)
    if result == "failure":
        print("No solution exists for this puzzle.")
    else:
        node = result
        print("  Goal state reached!")
        print(f"  Solution depth (moves):  {node['depth']}")
        print(f"  Nodes expanded:          {nodes_expanded}")
        print(f"  Max queue size:          {max_queue_size}")
        print(f"  Time elapsed:            {elapsed:.8f} s")

        # Reconstruct path from root to goal
        path = []
        curr = node
        while curr is not None:
            path.append(curr['state'])
            curr = curr['parent']
        path.reverse()

        print(f"\n  Solution path ({len(path) - 1} move(s)):")
        for i, state in enumerate(path):
            label = "Initial" if i == 0 else f"Step {i}"
            print(f"\n  [{label}]")
            print_state(state)
    print("=" * 45)

#Choose a preset puzzle or enter a puzzle
def get_puzzle():
    print("\n" + "=" * 45)
    print("  Eight Puzzle Solver")
    print("=" * 45)
    print("  1. Use a default puzzle (depth-8 test case)")
    print("  2. Enter your own puzzle")
    choice = input("\n  Choose (1 or 2): ").strip()

    if choice == "2":
        print("\n  Enter each row of the puzzle separated by spaces.")
        print("  Use 0 for the blank tile. Example:  1 2 3")
        state = []
        for i in range(N_Rows):
            while True:
                try:
                    raw = input(f"  Row {i + 1}: ").strip().split()
                    row = [int(x) for x in raw]
                    if len(row) != N_Cols:
                        print(f"  Please enter exactly {N_Cols} numbers.")
                        continue
                    state.append(row)
                    break
                except ValueError:
                    print("  Invalid input — please enter integers only.")
        return state
    else:
        print("Choose a puzzle 1-8")
        puzzle_choice = input("Enter Choice: ").strip()

        # Sample test cases
        if puzzle_choice == "1":
            return [
                [1, 2, 3],
                [4, 5, 6],
                [7, 8, 0]
            ]
        elif puzzle_choice == "2":
            return [
                [1, 2, 3],
                [4, 5, 6], 
                [0, 7, 8]
            ]
        elif puzzle_choice == "3":
            return [
                [1, 2, 3],
                [5, 0, 6], 
                [4, 7, 8]
            ]
        elif puzzle_choice == "4":
            return [
                [1, 3, 6],
                [5, 0, 2], 
                [4, 7, 8]
            ]
        elif puzzle_choice == "5":
            return [
                [1, 3, 6],
                [5, 0, 7], 
                [4, 8, 2]
            ]
        elif puzzle_choice == "6":
            return [
                [1, 6, 7],
                [5, 0, 3], 
                [4, 8, 2]
            ]
        elif puzzle_choice == "7":
            return [
                [7, 1, 2],
                [4, 8, 5], 
                [6, 3, 0]
            ]
        elif puzzle_choice == "8":
            return [
                [0, 7, 2],
                [4, 6, 1], 
                [3, 5, 8]
            ]
    

def get_algorithm():
    print("\n  Select algorithm:")
    print("  1. Uniform Cost Search")
    print("  2. A* with Misplaced Tile Heuristic")
    print("  3. A* with Manhattan Distance Heuristic")
    while True:
        choice = input("\n  Choose (1, 2, or 3): ").strip()
        if choice in ('1', '2', '3'):
            return int(choice)
        print("  Invalid choice — please enter 1, 2, or 3.")


def get_verbose():
    ans = input("\n  Print each expanded node? (y/n): ").strip().lower()
    return ans != 'n'







def main():
    #Gather inputs
    initial_state = get_puzzle()
    algorithm_choice = get_algorithm()
    verbose = get_verbose()

    print("\n  Initial state:")
    print_state(initial_state)

    #Build problem dict
    problem = {
        'initial_state': initial_state,
        'GoalTest':     GoalTest,
        'operators':     OPERATORS
    }

    #Map choice to algorithm name and queueing function
    algo_names = {
        1: "Uniform Cost Search",
        2: "A* — Misplaced Tile Heuristic",
        3: "A* — Manhattan Distance Heuristic"
    }
    queueing_funcs = {
        1: QueueingUniformCost,
        2: QueueingMisplacedTile,
        3: QueueingManhattan
    }

    print(f"\n  Running {algo_names[algorithm_choice]} ...\n")

    #Run search 
    start = time.time()
    result, nodes_expanded, max_queue_size = GeneralSearch(
        problem,
        queueing_funcs[algorithm_choice],
        verbose=verbose
    )
    elapsed = time.time() - start

    #Display results
    print_solution(result, nodes_expanded, max_queue_size, elapsed)


if __name__ == "__main__":
    main()