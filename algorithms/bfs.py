from collections import deque
from core.state import reconstruct_path

def bfs(grid, start_state):

    queue = deque([start_state])
    visited = set()

    visited.add(start_state)   

    nodes_expanded = 0

    while queue:
        current = queue.popleft()
        nodes_expanded += 1

        if grid.is_goal(current):
            path = reconstruct_path(current)
            return path, nodes_expanded, current.cost

        for neighbor in grid.get_neighbors(current):

            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return None, nodes_expanded, float('inf')

