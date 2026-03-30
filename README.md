# Warehouse Robot: Multi-Objective Pathfinding & Routing

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-Video%20Generation-green)
![Pillow](https://img.shields.io/badge/Pillow-Image%20Processing-yellow)

This project implements a **Level 3 grid-based pathfinding simulation** for an autonomous warehouse robot. The robot must navigate a complex warehouse environment (including walls and variable-cost terrain), manage a limited energy supply, calculate optimal routes to collect multiple scattered items, and reach a final delivery zone without running out of battery.

## Key Features

* **Multi-Item Routing (TSP):** Implements a **Minimum Spanning Tree (MST)** over remaining uncollected items to generate highly accurate lower-bound distance estimates.
* **Energy-Aware Pruning:** Algorithms dynamically prune mathematically impossible paths early in the search tree if the heuristic distance exceeds the robot's remaining energy.
* **Advanced Heuristics:** Features both **Manhattan Distance** and **ALT (A*, Landmarks, Triangle Inequality)** heuristics, combined with MST logic for state-of-the-art node evaluation.
* **Headless Video Generation:** Includes a custom, headless visualization engine powered by Pillow and OpenCV that automatically stitches search paths into smooth `10 FPS` `.mp4` demo videos without requiring a GUI.
* **Detailed Analytics:** Automatically generates formatted text reports detailing step-by-step actions (U, D, L, R), nodes expanded, and total energy consumed.

---

## Project Structure

```text
Warehouse_Robot/
├── algorithms/              # Search algorithms
│   ├── astar.py             # A* Search
│   ├── bfs.py               # Breadth-First Search
│   ├── gbfs.py              # Greedy Best-First Search
│   └── ucs.py               # Uniform Cost Search
├── core/                    # Core logic and classes
│   ├── grid.py              # Warehouse grid environment
│   └── state.py             # Robot state representation
├── demo_cases/              # Test maps of varying difficulty
│   ├── easy_cases.py        
│   ├── medium_cases.py      
│   ├── hard_cases.py        
│   └── energy_cases.py      # Maps designed to test energy exhaustion
├── experiments/             
│   └── run_tests.py         # Main execution script
├── heuristics/              # Distance estimators
│   ├── landmark.py          # ALT Landmark heuristic + MST
│   └── manhattan.py         # Manhattan distance + MST
└── visualization/           
    └── visualizer.py        # OpenCV & Pillow rendering engine
```

---

## Extras / Supporting Material
1. **GRP_17_PPT USED IN DEMO FOR EXTRA UNDERSTANDING:** Presentation explaining problem setup, algorithms, heuristics, and demo flow
2. **GRP_17_empirical_validation:** Document with detailed experimental analysis and performance comparison
3. **D1 & D2 (PDFs):** Previous submissions included for reference and project progression

These materials provide a complete view of the project’s development, implementation, evaluation and deeper theoretical understanding.

## Installation & Setup

1. **Clone the repository:**
   Ensure you are in the root directory (`Warehouse_Robot-main`).

2. **Install dependencies:**
   The search algorithms use standard Python libraries, but the visualizer requires `Pillow` for image generation and `OpenCV` for video stitching. Run the following command in your terminal:
   ```bash
   pip install pillow opencv-python
   ```

---

## Usage

To run the entire suite of test cases across all algorithms and generate the output files, run the main experiment script from the root directory:

```bash
python experiments/run_tests.py
```

### Understanding the Outputs
Upon completion, the script will generate an `outputs/` folder inside the `visualization/` directory. For every map and algorithm combination (e.g., `hard_1_Astar-Manhattan`), a dedicated folder is created containing:

1. **`/grids/initial_grid.txt`**: A clean ASCII representation of the starting map showing walls (`#`), items (`I`), floor costs (e.g., `5`), the start point (`S`), and the delivery zone (`D`).
2. **`/frames/*.png`**: High-quality PNG snapshots of every step the robot took.
3. **`/paths/final_path_result.png`**: A graphical overview of the map showing the robot's complete, color-coded movement trail.
4. **`/paths/*_stats.txt`**: A detailed statistical readout of the algorithm's performance, including total cost, nodes expanded, and the exact sequence of actions.
5. **`*_demo.mp4`**: A smooth, auto-generated video animation of the robot solving the maze.

---

## Algorithms Explored

* **BFS (Breadth-First Search):** Serves as a baseline, uninformed search algorithm. It explores equally in all directions to find the path with the fewest *steps*. However, it ignores varying terrain costs, meaning it often fails to find the most energy-efficient route.
* **UCS (Uniform Cost Search):** The cost-aware baseline. Unlike BFS, UCS factors in the actual energy weight of the floor tiles. It guarantees the absolute lowest-cost (most energy-efficient) path. However, because it lacks a heuristic to guide it, it expands a massive number of nodes and struggles heavily on `hard` and `energy` test cases.
* **GBFS (Greedy Best-First Search):** An informed search that aggressively pursues the lowest heuristic value. It is incredibly fast and explores very few nodes, but it does not guarantee the optimal (lowest cost) path.
* **A\* Search:** The optimal informed search. By prioritizing $$f(n) = g(n) + h(n)$$, A* perfectly balances the energy cost so far with the estimated distance remaining. It guarantees the most energy-efficient path while expanding significantly fewer nodes than BFS or UCS.

### The L3 Heuristic Upgrade
Both `GBFS` and `A*` rely on a custom multi-objective heuristic. Instead of blindly pointing to the delivery zone, the heuristic calculates:

$$h(n) = \text{Dist}(\text{Nearest Item}) + \text{MST}(\text{Remaining Items}) + \text{Dist}(\text{Delivery})$$

This ensures the algorithms sweep the warehouse methodically to collect items efficiently without backtracking.

---

## Authors
* **Prachi Garg** *2023A7PS0548P*
* **Jyotsna Lal** *2023A7PS0660P*
* **Soham Kudva** *2023A7PS0589P*
* **Daksh Tyagi** *2023A7PS0647P*
