# 🤖 Warehouse Robot: Multi-Objective Pathfinding & Routing

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-Video%20Generation-green)
![Pillow](https://img.shields.io/badge/Pillow-Image%20Processing-yellow)

This project implements a **Level 3 grid-based pathfinding simulation** for an autonomous warehouse robot. The robot must navigate a complex warehouse environment (including walls and variable-cost terrain), manage a limited energy supply, calculate optimal routes to collect multiple scattered items, and reach a final delivery zone without running out of battery.

## ✨ Key Features

* **Multi-Item Routing (TSP):** Implements a **Minimum Spanning Tree (MST)** over remaining uncollected items to generate highly accurate lower-bound distance estimates.
* **Energy-Aware Pruning:** Algorithms dynamically prune mathematically impossible paths early in the search tree if the heuristic distance exceeds the robot's remaining energy.
* **Advanced Heuristics:** Features both **Manhattan Distance** and **ALT (A*, Landmarks, Triangle Inequality)** heuristics, combined with MST logic for state-of-the-art node evaluation.
* **Headless Video Generation:** Includes a custom, headless visualization engine powered by Pillow and OpenCV that automatically stitches search paths into smooth `10 FPS` `.mp4` demo videos without requiring a GUI.
* **Detailed Analytics:** Automatically generates formatted text reports detailing step-by-step actions (U, D, L, R), nodes expanded, and total energy consumed.

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
