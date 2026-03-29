Markdown# 🤖 Warehouse Robot: Multi-Objective Pathfinding & Routing

This project is a Level 3 grid-based pathfinding simulation for an autonomous warehouse robot. The robot must navigate a complex warehouse environment, manage a limited energy supply, calculate optimal routes to collect multiple scattered items, and reach a final delivery zone without running out of battery.

## ✨ Key Features

* **Multi-Item Routing (TSP):** Implements a Minimum Spanning Tree (MST) over remaining uncollected items to generate highly accurate lower-bound distance estimates.
* **Energy-Aware Pruning:** Algorithms dynamically prune mathematically impossible paths early in the search tree if the heuristic distance exceeds the robot's remaining energy.
* **Advanced Heuristics:** Features both Manhattan Distance and ALT (A*, Landmarks, Triangle Inequality) heuristics, combined with MST logic for state-of-the-art node evaluation.
* **Headless Video Generation:** Includes a custom, headless visualization engine powered by Pillow and OpenCV that automatically stitches search paths into 10 FPS `.mp4` demo videos without requiring a GUI.

---

## 📂 Project Structure

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
🚀 Installation & SetupClone the repository:Ensure you are in the root directory (Warehouse_Robot-main).Install dependencies:The search algorithms use standard Python libraries, but the visualizer requires Pillow for image generation and OpenCV for video stitching.Bashpip install pillow opencv-python
🕹️ UsageTo run the entire suite of test cases across all algorithms and generate the output files, run the main experiment script from the root directory:Bashpython experiments/run_tests.py
📊 Understanding the OutputsUpon completion, the script will generate an outputs/ folder inside the visualization/ directory. For every map and algorithm combination (e.g., hard_1_Astar-Manhattan), a dedicated folder is created containing:/grids/initial_grid.txt: A clean ASCII representation of the starting map showing walls (#), items (I), floor costs (5), the start point (S), and the delivery zone (D)./frames/*.png: High-quality PNG snapshots of every step the robot took./paths/final_path_result.png: A graphical overview of the map showing the robot's complete, color-coded movement trail./paths/*_stats.txt: A detailed statistical readout of the algorithm's performance, including total cost, nodes expanded, and the exact sequence of actions (U, D, L, R).*_demo.mp4: A smooth, auto-generated video animation of the robot solving the maze.🧠 Algorithms ExploredBFS (Breadth-First Search) & UCS (Uniform Cost Search): Serve as baseline, uninformed search algorithms. They guarantee optimal paths but expand massive numbers of nodes (often struggling on hard and energy cases).GBFS (Greedy Best-First Search): An informed search that aggressively pursues the lowest heuristic value. It is incredibly fast but does not guarantee the optimal (lowest cost) path.A Search:* The optimal informed search. By prioritizing $f(n) = g(n) + h(n)$, A* guarantees the most energy-efficient path while expanding significantly fewer nodes than BFS/UCS.The L3 Heuristic UpgradeBoth GBFS and A* rely on a custom multi-objective heuristic. Instead of blindly pointing to the delivery zone, the heuristic calculates:$h(n) = \text{Dist}(\text{Nearest Item}) + \text{MST}(\text{Remaining Items}) + \text{Dist}(\text{Delivery})$This ensures the algorithms sweep the warehouse methodically rather than backtracking.
