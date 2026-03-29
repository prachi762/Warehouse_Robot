import heapq
from core.state import reconstruct_path

def ucs(grid, start_state):

    pq = []
    heapq.heappush(pq, (0, start_state))

    best_cost = {}
    best_cost[start_state] = 0

    nodes_expanded = 0

    while pq:
        cost, current = heapq.heappop(pq)

        if cost > best_cost[current]:
            continue

        nodes_expanded += 1

        if grid.is_goal(current):
            path = reconstruct_path(current)
            return path, nodes_expanded, cost

        for neighbor in grid.get_neighbors(current):

            new_cost = neighbor.cost  

            if neighbor not in best_cost or new_cost < best_cost[neighbor]:
                best_cost[neighbor] = new_cost
                heapq.heappush(pq, (new_cost, neighbor))

    return None, nodes_expanded, float('inf')

