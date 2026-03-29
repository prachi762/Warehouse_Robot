from collections import deque

def bfs_from_landmark(grid, start):
    N = grid.N
    dist = [[-1]*N for _ in range(N)]
    q = deque([start])
    dist[start[0]][start[1]] = 0
    moves = [(1,0),(-1,0),(0,1),(0,-1)]

    while q:
        x, y = q.popleft()
        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            if grid.is_valid(nx, ny) and dist[nx][ny] == -1:
                dist[nx][ny] = dist[x][y] + 1
                q.append((nx, ny))
    return dist

def precompute_landmarks(grid, landmarks):
    dist_table = {}
    for l in landmarks:
        dist_table[l] = bfs_from_landmark(grid, l)
    return dist_table

def get_alt_distance(p1, p2, dist_table, landmarks):
    
    max_val = 0
    for l in landmarks:
        d1 = dist_table[l][p1[0]][p1[1]]
        d2 = dist_table[l][p2[0]][p2[1]]
        if d1 == -1 or d2 == -1:
            continue
        val = abs(d1 - d2)
        if val > max_val:
            max_val = val
    return max_val

def get_mst_cost(points, dist_func):
    if len(points) <= 1: return 0
    n = len(points)
    in_tree = [False] * n
    best = [float('inf')] * n
    best[0] = 0
    total = 0
    for _ in range(n):
        u, min_val = -1, float('inf')
        for i in range(n):
            if not in_tree[i] and best[i] < min_val:
                min_val, u = best[i], i
        if u == -1: break
        in_tree[u] = True
        total += min_val
        for v in range(n):
            if not in_tree[v]:
                d = dist_func(points[u], points[v])
                if d < best[v]: best[v] = d
    return total

def get_landmark_heuristic(dx, dy, dist_table, landmarks):
    def h(state, grid):
        uncollected = []
        for i, (ix, iy, _) in enumerate(grid.items):
            if not (state.collected & (1 << i)):
                uncollected.append((ix, iy))

        current_pos = (state.x, state.y)
        delivery_pos = (dx, dy)

        if not uncollected:
            return get_alt_distance(current_pos, delivery_pos, dist_table, landmarks)

        min_to_item = min(get_alt_distance(current_pos, item, dist_table, landmarks) for item in uncollected)

        mst_cost = get_mst_cost(uncollected, lambda a, b: get_alt_distance(a, b, dist_table, landmarks))

        min_to_delivery = min(get_alt_distance(item, delivery_pos, dist_table, landmarks) for item in uncollected)

        return min_to_item + mst_cost + min_to_delivery

    return h
