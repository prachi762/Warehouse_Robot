def manhattan_dist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def get_mst_cost(points, dist_func):
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
                
        if u == -1: break
        in_tree[u] = True
        total += min_val

        for v in range(n):
            if not in_tree[v]:
                d = dist_func(points[u], points[v])
                if d < best[v]:
                    best[v] = d
    return total

def get_manhattan(dx, dy):
    def h(state, grid):
        uncollected = []
        for i, (ix, iy, _) in enumerate(grid.items):
            if not (state.collected & (1 << i)):
                uncollected.append((ix, iy))

        current_pos = (state.x, state.y)
        delivery_pos = (dx, dy)

        if not uncollected:
            return manhattan_dist(current_pos, delivery_pos)

        min_to_item = min(manhattan_dist(current_pos, item) for item in uncollected)

        mst_cost = get_mst_cost(uncollected, manhattan_dist)

        min_to_delivery = min(manhattan_dist(item, delivery_pos) for item in uncollected)

        return min_to_item + mst_cost + min_to_delivery

    return h
