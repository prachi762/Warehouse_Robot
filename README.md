# Warehouse Robot Multi-Item Collection

This project implements four search algorithms for a warehouse robot that must collect all required items on a grid:

- BFS
- UCS
- Greedy Best-First Search
- A* Search

It also implements two heuristics:

- **H1**: nearest remaining item lower bound
- **H2**: nearest item + MST lower bound over remaining items

## 1. State representation

Each search state is:

```python
(position, collected_items_mask)
```

This is essential for a multi-item problem because reaching the same cell before and after collecting different items represents different search states.

## 2. Cost model

- The robot moves in four directions: up, down, left, right.
- The energy cost of a move is the cost of entering the destination cell.
- `.` means cost 1.
- Digits `1` to `9` mean that exact movement energy cost.
- `I` means an item cell.
- `#` means a wall.
- `S` means the start cell.

## 3. Map format

Example:

```text
###########
#S..2...I.#
#.###.##..#
#...#...#.#
#.I.#.3...#
#...###.#.#
#..I....#.#
###########
```

## 4. Files

- `warehouse.py` - map parsing, state representation, transitions
- `heuristics.py` - H1 and H2
- `algorithms.py` - BFS, UCS, Greedy, A*
- `visualization.py` - saves search snapshots and progression frames
- `main.py` - runs experiments and prints results
- `maps/sample_map.txt` - sample warehouse map

## 5. Requirements

Install:

```bash
pip install matplotlib
```

`heapq`, `deque`, and `itertools` are from Python standard library.

## 6. Run commands

Run all algorithms:

```bash
python main.py --map maps/sample_map.txt --algorithm all --visualize
```

Run only A* with H2:

```bash
python main.py --map maps/sample_map.txt --algorithm astar --heuristic h2 --visualize --frames
```

Run Greedy with H1:

```bash
python main.py --map maps/sample_map.txt --algorithm greedy --heuristic h1 --visualize
```

## 7. Output

For each run, the code prints:

- whether a solution was found
- path length in steps
- total energy
- number of nodes expanded
- max frontier size
- runtime
- action sequence
- full path

If visualization is enabled, it saves:

- `snapshot.png` - explored cells + final path
- `frames/` - multiple images showing search progression over time

## 8. Heuristics explanation

### H1

Nearest remaining item using Manhattan distance multiplied by minimum step cost in the map.

This is admissible because it ignores walls and therefore never overestimates the true remaining cost.

### H2

Nearest remaining item cost + MST cost over all remaining items, both computed using Manhattan-distance lower bounds.

This is stronger than H1 and still admissible for A*.

## 9. Expected behavior

- BFS minimizes number of steps, not energy.
- UCS minimizes total energy.
- Greedy follows the heuristic only, so it can be fast but suboptimal.
- A* combines actual energy used so far with heuristic estimate of remaining energy.

## 10. Notes for demo

For your presentation/demo, the strongest comparison is:

- BFS
- UCS
- Greedy + H1
- Greedy + H2
- A* + H1
- A* + H2

This clearly shows the effect of both heuristics and why A* is the most suitable algorithm for the warehouse problem.
