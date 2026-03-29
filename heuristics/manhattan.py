def get_manhattan(dx, dy):
    """
    Returns a Manhattan heuristic function

    h(n) = |x - x_d| + |y - y_d|
    """

    def h(state):
        return abs(state.x - dx) + abs(state.y - dy)

    return h
