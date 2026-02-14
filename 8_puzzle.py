import heapq
import copy


#Goal State table which represents the solved puzzle
Goal_State = [
[1, 2, 3],
[4, 5, 6],
[7, 8, 0]
]


#Computes goal positions for heuristic calculation 
Goal_Position = {}
for r, row in enumerate(Goal_State):
    for c, val in enumerate(Goal_State):
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
def queueing_uniform_cost(nodes, counter, new_nodes):
    for child in new_nodes:
        child['h'] = H_Zero(child['state'])
        child['f'] = child['g'] + child['h']
        heapq.heappush(nodes, (child['f'], counter[0], child))
        counter[0] += 1
    return nodes

#Orders nodes by f(n) = g(N) + H_misplaced(n)
def queueing_misplaced_tile(nodes, counter, new_nodes):
    for child in new_nodes:
        child['h'] = H_MisplacedTile(child['state'])
        child['f'] = child['g'] + child['h']
        heapq.heappush(nodes, (child['f'], counter[0], child))
        counter[0] += 1
    return nodes

#Orders nodes by f(n) = g(n) + H_Manhattan(n)
def queueing_manhattan(nodes, counter, new_nodes):
    for child in new_nodes:
        child['h'] = H_Manhattan(child['state'])
        child['f'] = child['g'] + child['h']
        heapq.heappush(nodes, (child['f'], counter[0], child))
        counter[0] += 1
    return nodes
