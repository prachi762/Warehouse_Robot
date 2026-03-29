class State:
    def __init__(self, x, y, collected, energy, cost=0, parent=None,value=0):
        self.x = x
        self.y = y
        self.collected = collected 
        self.energy = energy
        self.cost = cost            
        self.parent = parent  
        self.value = value      

    def __hash__(self):
        return hash((self.x, self.y, self.collected))

    def __eq__(self, other):
        if not isinstance(other, State):
            return False
        return (self.x, self.y, self.collected) == \
               (other.x, other.y, other.collected)

def reconstruct_path(state):
    path = []
    while state:
        path.append((state.x, state.y))
        state = state.parent
    return path[::-1]
