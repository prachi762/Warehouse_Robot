from core.grid import Grid

def load_case(case):

    if case == "easy":
        # ✅ Baseline sanity test
        g = Grid(10)
        g.start = (0,0)
        g.delivery = (9,9)
        g.set_items([(2,2), (5,5)])
        g.energy = 50

    elif case == "medium":
        # 🎯 Landmark vs Manhattan difference
        g = Grid(20)
        g.start = (0,0)
        g.delivery = (19,19)
        g.set_items([(3,15), (10,10), (15,3)])
        g.energy = 120

        # obstacle wall with gap
        for i in range(5,15):
            g.grid[i][8] = 1

        g.grid[10][8] = 0  # gap

    elif case == "hard":
        # 🎯 GBFS failure + energy constraint
        g = Grid(40)
        g.start = (0,0)
        g.delivery = (39,39)
        g.set_items([(5,35),(10,10),(20,30),(30,5)])
        g.energy = 200

        # misleading open path to delivery
        # but items are far off
        for i in range(10,30):
            g.grid[i][20] = 1

        g.grid[20][20] = 0  # small gap

    elif case == "energy_trap":
    g = Grid(15)
    g.start = (0,0)
    g.delivery = (14,14)
    g.set_items([(7,7)])

    # barely enough energy
    g.energy = 20

    return g
