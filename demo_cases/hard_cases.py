from core.grid import Grid

def hard_case_1():
    g = Grid(40)
    g.start = (0,0)
    g.delivery = (39,39)
    g.set_items([(5,35),(10,10),(20,30),(30,5)])
    g.energy = 200

    # misleading wall
    for i in range(10,30):
        g.grid[i][20] = 1

    g.grid[20][20] = 0 
    return g


def hard_case_2():
    g = Grid(30)
    g.start = (0,0)
    g.delivery = (29,29)
    g.set_items([(10,5),(5,20),(20,15)])
    g.energy = 150

    # maze-like structure
    for i in range(5,25):
        g.grid[i][10] = 1
        g.grid[i][20] = 1

    g.grid[15][10] = 0
    g.grid[15][20] = 0
    return g
