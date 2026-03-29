import heapq
from core.state import reconstruct_path
from utils.pareto import is_dominated, update_pareto


def astar(grid, start_state, heuristic):

    pq = []
    counter = 0

    start_h = heuristic(start_state)
    heapq.heappush(pq, (start_h, counter, start_state))

    pareto = {}
    key = (start_state.x, start_state.y, start_state.collected)
    pareto[key] = [(start_state.cost, start_state.energy)]

    nodes_expanded = 0

    while pq:
        f_val, _, current = heapq.heappop(pq)
        nodes_expanded += 1

        if grid.is_goal(current):
            return reconstruct_path(current), nodes_expanded, current.cost

        for neighbor in grid.get_neighbors(current):

            h_val = heuristic(neighbor)

            if h_val > neighbor.energy:
                continue

            key = (neighbor.x, neighbor.y, neighbor.collected)
            c = neighbor.cost
            e = neighbor.energy

            if key not in pareto:
                pareto[key] = [(c, e)]
            else:
                if is_dominated(pareto[key], c, e):
                    continue

                pareto[key] = update_pareto(pareto[key], c, e)

            counter += 1
            heapq.heappush(pq, (c + h_val, counter, neighbor))

    return None, nodes_expanded, float('inf')
