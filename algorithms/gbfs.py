import heapq
from core.state import reconstruct_path

def gbfs(grid, start_state, heuristic):

    pq = []
    heapq.heappush(pq, (heuristic(start_state), start_state))

    visited = set()
    visited.add(start_state)

    nodes_expanded = 0

    while pq:
        h_val, current = heapq.heappop(pq)
        nodes_expanded += 1

        if grid.is_goal(current):
            path = reconstruct_path(current)
            return path, nodes_expanded, current.cost

        for neighbor in grid.get_neighbors(current):

            if heuristic(neighbor) > neighbor.energy:
                continue

            if neighbor not in visited:
                visited.add(neighbor)
                heapq.heappush(pq, (heuristic(neighbor), neighbor))

    return None, nodes_expanded, float('inf')
