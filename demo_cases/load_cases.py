def load_case(case):

    if case == "easy":
        g = Grid(10)
        g.start = (0,0)
        g.delivery = (9,9)
        g.items = [(2,2), (5,5)]
        g.energy = 50

    elif case == "medium":
        g = Grid(20)
        g.start = (0,0)
        g.delivery = (19,19)
        g.items = [(3,15), (10,10), (15,3)]
        g.energy = 120

        # obstacles
        for i in range(5,15):
            g.grid[i][8] = 1

    elif case == "hard":
        g = Grid(40)
        g.start = (0,0)
        g.delivery = (39,39)
        g.items = [(5,35),(10,10),(20,30),(30,5)]
        g.energy = 200

    return g
