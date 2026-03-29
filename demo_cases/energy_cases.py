from core.grid import Grid

def energy_case_1():
    g = Grid(15)
    g.start = (0,0)
    g.delivery = (14,14)

    g.set_items([
        (7,7,50)  
    ])

    g.energy = 20
    return g


def energy_case_2():
    g = Grid(20)
    g.start = (0,0)
    g.delivery = (19,19)

    g.set_items([
        (10,10,10),   
        (15,15,40)   
    ])

    g.energy = 40
    return g
