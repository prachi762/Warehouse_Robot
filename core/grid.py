from core.state import State

class Grid:
    def __init__(self, N):
        self.N = N
        self.grid = [[0]*N for _ in range(N)]

        self.items = []      
        self.item_map = {}
        self.item_weights = []   

        self.delivery = (0,0)
        self.start = (0,0)
        self.energy = 100

    def set_items(self, items):
        self.items = items
        self.item_map = {}
        self.item_weights = []
        
        for i, (x, y, w) in enumerate(items):
            self.item_map[(x, y)] = i
            self.item_weights.append(w)

    def is_valid(self, x, y):
        return 0 <= x < self.N and 0 <= y < self.N and self.grid[x][y] == 0

    def get_neighbors(self, state):
        moves = [(1,0),(-1,0),(0,1),(0,-1)]
        neighbors = []

        if state.energy == 0:
            return neighbors

        for dx, dy in moves:
            nx, ny = state.x + dx, state.y + dy

            if not self.is_valid(nx, ny):
                continue

            new_collected = state.collected
            new_value = state.value   

            if (nx, ny) in self.item_map:
                i = self.item_map[(nx, ny)]

                if not (state.collected & (1 << i)):
                    new_collected |= (1 << i)
                    new_value += self.item_weights[i]


            new_state = State(
                nx,
                ny,
                new_collected,
                state.energy - 1,
                state.cost + 1,
                state,
                new_value
            )

            neighbors.append(new_state)

        return neighbors

    def is_goal(self, state):
        k = len(self.items)
        dx, dy = self.delivery

        return (
            state.collected == (1 << k) - 1 and
            state.x == dx and
            state.y == dy
        )
