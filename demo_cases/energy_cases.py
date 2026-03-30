from core.grid import Grid

def energy_case_1():
    g = Grid(15)
    g.start = (0,0)
    g.delivery = (14,14)

    g.set_items([
        (7,7,50)  
    ])

    g.energy = 45
    
    for y in range(4, 7):
        for x in range(4, 7):
            g.grid[y][x] = 3
            
    return g


def energy_case_2():
    g = Grid(20)
    g.start = (0,0)
    g.delivery = (19,19)

    g.set_items([
        (10,10,10),   
        (15,15,40)   
    ])

    g.energy = 70

    for y in range(2, 18):
        for x in range(12, 14):
            g.grid[y][x] = 5
            
    return g
