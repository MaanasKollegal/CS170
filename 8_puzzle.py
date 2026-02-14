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
C_Cols = len(Goal_State[0])



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
    {

    }
    