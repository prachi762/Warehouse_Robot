from collections import deque
from core.state import reconstruct_path
from utils.pareto import is_dominated, update_pareto


def bfs(grid, start_state):

    queue = deque([start_state])

    pareto = {}
    key = (start_state.x, start_state.y, start_state.collected)
    pareto[key] = [(start_state.cost, start_state.energy)]

    nodes_expanded = 0

    while queue:
        current = queue.popleft()
        nodes_expanded += 1

        if grid.is_goal(current):
            return reconstruct_path(current), nodes_expanded, current.cost

        for neighbor in grid.get_neighbors(current):

            c = neighbor.cost
            e = neighbor.energy
            key = (neighbor.x, neighbor.y, neighbor.collected)

            if key not in pareto:
                pareto[key] = [(c, e)]
            else:
                if is_dominated(pareto[key], c, e):
                    continue

                pareto[key] = update_pareto(pareto[key], c, e)

            queue.append(neighbor)

    return None, nodes_expanded, float('inf')
