from core.grid import Grid

def medium_case_1():
    g = Grid(20)
    g.start = (0,0)
    g.delivery = (19,19)
    g.set_items([(3,15), (10,10), (15,3)])
    g.energy = 120

    # vertical wall with gap
    for i in range(5,15):
        g.grid[i][8] = 1

    g.grid[10][8] = 0  
    return g


def medium_case_2():
    g = Grid(20)
    g.start = (0,0)
    g.delivery = (19,19)
    g.set_items([(5,5), (10,15)])
    g.energy = 100

    # horizontal wall
    for j in range(5,15):
        g.grid[10][j] = 1

    g.grid[10][10] = 0  
    return g
