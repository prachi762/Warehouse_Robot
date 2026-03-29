import time
import os


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_grid(grid, state=None, visited=None):
    """
    Prints the grid with:
    S = Start
    D = Delivery
    I = Item
    X = Obstacle
    R = Robot (current state)
    . = Visited
    - = Empty
    """

    N = grid.N

    for i in range(N):
        row = ""
        for j in range(N):

            if state and (i, j) == (state.x, state.y):
                row += " R "

            elif (i, j) == grid.start:
                row += " S "

            elif (i, j) == grid.delivery:
                row += " D "

            elif (i, j) in grid.items:
                row += " I "

            elif grid.grid[i][j] == 1:
                row += " X "

            elif visited and (i, j) in visited:
                row += " . "

            else:
                row += " - "

        print(row)
    print("\n")

def animate_path(grid, path, delay=0.2):
    """
    Animates the final path taken by the robot
    """

    print("Animating Final Path...\n")
    visited = set()

    for (x, y) in path:
        clear()

        visited.add((x, y))

        # create a dummy state-like object
        dummy = type("State", (), {"x": x, "y": y})

        print_grid(grid, dummy, visited)

        time.sleep(delay)


def animate_search(grid, path, explored_nodes, delay=0.05):
    """
    Shows exploration + final path
    """

    print("Animating Search Process...\n")

    visited = set()

    for (x, y) in explored_nodes:
        clear()

        visited.add((x, y))

        dummy = type("State", (), {"x": x, "y": y})
        print_grid(grid, dummy, visited)

        time.sleep(delay)

    animate_path(grid, path, delay=0.2)

