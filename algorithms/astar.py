import heapq
from core.state import reconstruct_path
from utils.pareto import is_dominated, update_pareto

def astar(grid, start_state, heuristic):
    pq = []
    counter = 0

    h0 = heuristic(start_state, grid)
    f0 = start_state.cost + h0

    heapq.heappush(pq, (f0, counter, start_state))

    pareto = {}  
    expansions = 0

    while pq:
        _, _, current = heapq.heappop(pq)
        expansions += 1

        if grid.is_goal(current):
            return reconstruct_path(current), expansions, current.cost

        key = (current.x, current.y, current.collected)
        current_p_list = pareto.get(key, [])

        if is_dominated(current_p_list, current.cost, current.energy, current.value):
            continue

        pareto[key] = update_pareto(current_p_list, current.cost, current.energy, current.value)

        for neighbor in grid.get_neighbors(current):
            if neighbor.energy < 0:
                continue

            n_key = (neighbor.x, neighbor.y, neighbor.collected)
            neighbor_p_list = pareto.get(n_key, [])

            if is_dominated(neighbor_p_list, neighbor.cost, neighbor.energy, neighbor.value):
                continue

            h_val = heuristic(neighbor, grid)
            
            if h_val > neighbor.energy:
                continue
                
            f_val = neighbor.cost + h_val
            counter += 1
            heapq.heappush(pq, (f_val, counter, neighbor))

    return None, expansions, float('inf')
