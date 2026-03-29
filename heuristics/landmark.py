from collections import deque

def bfs_from_landmark(grid, start):
    """
    Computes shortest distance from a landmark to all cells
    """
    N = grid.N
    dist = [[-1]*N for _ in range(N)]

    q = deque()
    q.append(start)
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
    """
    Precompute distance tables for all landmarks

    Returns:
        dict: { landmark -> distance matrix }
    """
    dist_table = {}

    for l in landmarks:
        dist_table[l] = bfs_from_landmark(grid, l)

    return dist_table


def landmark_heuristic(state, dx, dy, dist_table, landmarks):
    """
    ALT-style Landmark heuristic

    h(n) = max_l |dist(l, D) - dist(l, n)|
    """
    max_val = 0

    for l in landmarks:
        d_ld = dist_table[l][dx][dy]
        d_ln = dist_table[l][state.x][state.y]

        # Skip unreachable cases
        if d_ld == -1 or d_ln == -1:
            continue

        val = abs(d_ld - d_ln)
        if val > max_val:
            max_val = val

    return max_val


def get_landmark_heuristic(dx, dy, dist_table, landmarks):
    """
    Returns a callable heuristic function
    """

    def h(state):
        return landmark_heuristic(state, dx, dy, dist_table, landmarks)

    return h
