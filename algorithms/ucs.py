import heapq
from core.state import reconstruct_path
from utils.pareto import is_dominated, update_pareto


def ucs(grid, start_state):

    pq = []
    counter = 0
    heapq.heappush(pq, (0, counter, start_state))

    pareto = {}
    key = (start_state.x, start_state.y, start_state.collected)
    pareto[key] = [(start_state.cost, start_state.energy, start_state.value)]

    nodes_expanded = 0

    while pq:
        cost, _, current = heapq.heappop(pq)
        nodes_expanded += 1

        if grid.is_goal(current):
            return reconstruct_path(current), nodes_expanded, cost

        for neighbor in grid.get_neighbors(current):

            c, e, v = neighbor.cost, neighbor.energy, neighbor.value
            key = (neighbor.x, neighbor.y, neighbor.collected)

            if key not in pareto:
                pareto[key] = [(c, e, v)]
            else:
                if is_dominated(pareto[key], c, e, v):
                    continue
                pareto[key] = update_pareto(pareto[key], c, e, v)

            counter += 1
            heapq.heappush(pq, (c, counter, neighbor))

    return None, nodes_expanded, float('inf')
