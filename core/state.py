class State:
    def __init__(self, x, y, collected, energy, cost=0, parent=None):
        self.x = x
        self.y = y
        self.collected = collected 
        self.energy = energy
        self.cost = cost            
        self.parent = parent        

    def __hash__(self):
        return hash((self.x, self.y, self.collected, self.energy))

    def __eq__(self, other):
        if not isinstance(other, State):
            return False
        return (self.x, self.y, self.collected, self.energy) == \
               (other.x, other.y, other.collected, other.energy)


def is_goal(state, k, dx, dy):
    return state.collected == (1 << k) - 1 and state.x == dx and state.y == dy


def reconstruct_path(state):
    path = []
    while state:
        path.append((state.x, state.y))
        state = state.parent
    return path[::-1]
