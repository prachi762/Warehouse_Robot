import heapq
from core.state import reconstruct_path

def astar(grid, start_state, heuristic):

    pq = []
    counter = 0  

    start_h = heuristic(start_state)
    heapq.heappush(pq, (start_h, counter, start_state))

    best_cost = {}
    best_cost[start_state] = 0

    nodes_expanded = 0

    while pq:
        f_val, _, current = heapq.heappop(pq)

        g_val = current.cost

        if g_val > best_cost[current]:
            continue

        nodes_expanded += 1

        if grid.is_goal(current):
            path = reconstruct_path(current)
            return path, nodes_expanded, g_val

        for neighbor in grid.get_neighbors(current):

            g_new = neighbor.cost
            h_new = heuristic(neighbor)

            if h_new > neighbor.energy:
                continue

            if neighbor not in best_cost or g_new < best_cost[neighbor]:
                best_cost[neighbor] = g_new
                counter += 1
                f_new = g_new + h_new
                heapq.heappush(pq, (f_new, counter, neighbor))

    return None, nodes_expanded, float('inf')
