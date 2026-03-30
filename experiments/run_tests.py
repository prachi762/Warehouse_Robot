import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
import csv
from core.state import State

from algorithms.bfs import bfs
from algorithms.ucs import ucs
from algorithms.gbfs import gbfs
from algorithms.astar import astar

from heuristics.manhattan import get_manhattan
from heuristics.landmark import (
    get_landmark_heuristic,
    precompute_landmarks
)

from demo_cases.easy_cases import easy_case_1, easy_case_2
from demo_cases.medium_cases import medium_case_1, medium_case_2
from demo_cases.hard_cases import hard_case_1, hard_case_2
from demo_cases.energy_cases import energy_case_1, energy_case_2

from visualization.visualizer import WarehouseVisualizer

def get_actions_from_path(path):
    if not path or len(path) < 2:
        return ""
    
    actions = []
    for i in range(len(path) - 1):
        r1, c1 = path[i]
        r2, c2 = path[i+1]
        
        if r2 > r1: actions.append("D")
        elif r2 < r1: actions.append("U")
        elif c2 > c1: actions.append("R")
        elif c2 < c1: actions.append("L")
        
    return " ".join(actions)


def run_all():

    cases = [
        ("easy_1", easy_case_1),
        ("easy_2", easy_case_2),
        ("medium_1", medium_case_1),
        ("medium_2", medium_case_2),
        ("hard_1", hard_case_1),
        ("hard_2", hard_case_2),
        ("energy_1", energy_case_1),
        ("energy_2", energy_case_2),
    ]

    results = []

    for case_name, case_fn in cases:
        print("\n" + "=" * 62)
        print(f"RUNNING {case_name.upper().replace('_', ' ')} CASE")
        print("=" * 62)

        grid = case_fn()
        dx, dy = grid.delivery

        h_manhattan = get_manhattan(dx, dy)
        landmarks = [(0, 0), (grid.N - 1, grid.N - 1)]
        dist_table = precompute_landmarks(grid, landmarks)
        h_landmark = get_landmark_heuristic(dx, dy, dist_table, landmarks)

        algos = [
            ("BFS", bfs, None),
            ("UCS", ucs, None),
            ("GBFS-Manhattan", gbfs, h_manhattan),
            ("GBFS-Landmark", gbfs, h_landmark),
            ("A*-Manhattan", astar, h_manhattan),
            ("A*-Landmark", astar, h_landmark),
        ]

        case_results = []

        for name, algo, heuristic in algos:

            start_state = State(
                grid.start[0],
                grid.start[1],
                0,
                grid.energy
            )

            start_time = time.time()

            if heuristic:
                path, expanded, cost = algo(grid, start_state, heuristic)
            else:
                path, expanded, cost = algo(grid, start_state)

            runtime = round(time.time() - start_time, 6)

            vis = WarehouseVisualizer(grid, title=f"{case_name}_{name}")

            path_states = []
            if path is not None and cost != float('inf'):
                for (px, py) in path:
                    dummy_state = type("State", (), {"x": px, "y": py, "collected": 0, "energy": 0, "value": 0})
                    path_states.append(dummy_state)

            original_stdout = sys.stdout 
            sys.stdout = open(os.devnull, 'w') 
            vis.save_final_results(path_states, explored_keys_states=None, delay=0.0)
            sys.stdout = original_stdout

            found_solution = path is not None and cost != float('inf')
            steps = len(path) - 1 if found_solution else 0
            actions_str = get_actions_from_path(path) if found_solution else ""
            
            heuristic_name = "-"
            if "Manhattan" in name: heuristic_name = "Manhattan"
            elif "Landmark" in name: heuristic_name = "Landmark"
            
            algo_base_name = name.split('-')[0]
            
            snapshot_text = os.path.join(vis.dirs['paths'], 'final_path_result.png') if found_solution else "-"
            frames_text = f"{vis.frame_count} files in {vis.dirs['frames']}" if found_solution else "-"

            output_text = (
                f"Algorithm      : {algo_base_name}\n"
                f"Heuristic      : {heuristic_name}\n"
                f"Found solution : {found_solution}\n"
                f"Steps          : {steps}\n"
                f"Total energy   : {cost}\n"
                f"Nodes expanded : {expanded}\n"
                f"Runtime (s)    : {runtime:.6f}\n"
                f"Actions        : {actions_str}\n"
                f"Path           : {path}\n"
                f"Saved snapshot : {snapshot_text}\n"
                f"Saved frames   : {frames_text}\n"
                + "=" * 62
            )

            print(output_text)

            safe_file_name = f"{name.replace('*', 'star')}_stats.txt"
            stats_file_path = os.path.join(vis.dirs['paths'], safe_file_name)
            
            with open(stats_file_path, "w") as f:
                f.write("=" * 62 + "\n")
                f.write(f"RUNNING {case_name.upper().replace('_', ' ')} CASE\n")
                f.write("=" * 62 + "\n")
                f.write(output_text + "\n")

            case_results.append({
                "Algorithm": name,
                "Cost": cost,
                "Expanded": expanded,
                "Time": runtime
            })

        results.append((case_name, case_results))

    save_results_csv(results)


def save_results_csv(results):
    filename = f"experiments/results_{int(time.time())}.csv"

    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow(["Case", "Algorithm", "Cost", "Expanded", "Time"])

        for case, case_results in results:
            for r in case_results:
                writer.writerow([
                    case,
                    r["Algorithm"],
                    r["Cost"],
                    r["Expanded"],
                    r["Time"]
                ])

    print(f"\nCSV results saved to: {filename}")



if __name__ == "__main__":
    run_all()
