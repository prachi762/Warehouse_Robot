def manhattan(state, dx, dy):
    """
    Manhattan-to-delivery heuristic

    h(n) = |x - x_d| + |y - y_d|

    Parameters:
        state : State object
        dx, dy : delivery location

    Returns:
        heuristic value (int)
    """
    return abs(state.x - dx) + abs(state.y - dy)

