from __future__ import annotations

from functools import lru_cache
from typing import List, Tuple

from warehouse import State, Warehouse, Position


def manhattan(a: Position, b: Position) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def heuristic_h1(state: State, warehouse: Warehouse) -> int:
    """Admissible lower bound: distance to the nearest remaining item.

    Uses Manhattan distance times the minimum traversal cost in the map.
    This ignores walls, so it never overestimates the true remaining energy.
    """
    remaining = warehouse.remaining_items(state)
    if not remaining:
        return 0
    return min(manhattan(state.position, item) for item in remaining) * warehouse.min_step_cost


@lru_cache(maxsize=None)
def _mst_cost(points: Tuple[Position, ...], min_step_cost: int) -> int:
    """Prim's algorithm on Manhattan distances for an MST lower bound."""
    if len(points) <= 1:
        return 0

    n = len(points)
    in_tree = [False] * n
    best = [float('inf')] * n
    best[0] = 0
    total = 0

    for _ in range(n):
        u = -1
        min_val = float('inf')
        for i in range(n):
            if not in_tree[i] and best[i] < min_val:
                min_val = best[i]
                u = i
        in_tree[u] = True
        total += int(min_val)

        for v in range(n):
            if in_tree[v]:
                continue
            dist = manhattan(points[u], points[v]) * min_step_cost
            if dist < best[v]:
                best[v] = dist

    return total


def heuristic_h2(state: State, warehouse: Warehouse) -> int:
    """Stronger admissible heuristic.

    nearest remaining item cost + MST over remaining items

    Why admissible:
    - the robot must at least reach one remaining item
    - and then connect the remaining items somehow
    - Manhattan distance * min step cost is a lower bound on true energy
    """
    remaining = warehouse.remaining_items(state)
    if not remaining:
        return 0

    nearest = min(manhattan(state.position, item) for item in remaining) * warehouse.min_step_cost
    mst = _mst_cost(tuple(sorted(remaining)), warehouse.min_step_cost)
    return nearest + mst


HEURISTICS = {
    "h1": heuristic_h1,
    "h2": heuristic_h2,
}
