from core.grid import Grid

def easy_case_1():
    g = Grid(10)
    g.start = (0,0)
    g.delivery = (9,9)
    g.set_items([(2,2), (5,5)])
    g.energy = 50
    return g


def easy_case_2():
    g = Grid(8)
    g.start = (0,0)
    g.delivery = (7,7)
    g.set_items([(3,3)])
    g.energy = 30
    return g

