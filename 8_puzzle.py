import heapq

#Goal State table which represents the solved puzzle
Goal_State = [
[1, 2, 3],
[4, 5, 6],
[7, 8, 0]
]

def CreateNode(state, parent=None, g=0, h=0, depth=0): #Creates a search node dictionary, f = g + h
    return{
        "state": state,
        "parent": parent,
        "g": g, #cost
        "h": h, #cost estimate 
        "f": g + h, #total cost
        "depth": depth
    }
    