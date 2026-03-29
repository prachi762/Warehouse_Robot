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

from demo_cases import (
    easy_case_1, easy_case_2,
    medium_case_1, medium_case_2,
    hard_case_1, hard_case_2,
    energy_case_1, energy_case_2
)


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
        print(f"\n===== Running Case: {case_name} =====")

        grid = case_fn()
        dx, dy = grid.delivery

        # Heuristics
        h_manhattan = get_manhattan(dx, dy)

        landmarks = [(0, 0), (grid.N - 1, grid.N - 1)]
        dist_table = precompute_landmarks(grid, landmarks)
        h_landmark = get_landmark_heuristic(dx, dy, dist_table, landmarks)

        # Algorithms
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

            runtime = round(time.time() - start_time, 5)

            case_results.append({
                "Algorithm": name,
                "Cost": cost,
                "Expanded": expanded,
                "Time": runtime
            })

        results.append((case_name, case_results))

        print_table(case_name, case_results)

    save_results_txt(results)
    save_results_csv(results)


# ------------------------------

def print_table(case, case_results):
    print(f"\nResults for {case}:\n")

    print(f"{'Algorithm':<20} {'Cost':<10} {'Expanded':<15} {'Time(s)':<10}")
    print("-" * 60)

    for r in case_results:
        print(f"{r['Algorithm']:<20} {r['Cost']:<10} {r['Expanded']:<15} {r['Time']:<10}")


# ------------------------------

def save_results_txt(results):
    filename = f"experiments/results_{int(time.time())}.txt"

    with open(filename, "w") as f:
        for case, case_results in results:
            f.write(f"\n===== Case: {case} =====\n\n")
            f.write(f"{'Algorithm':<20} {'Cost':<10} {'Expanded':<15} {'Time(s)':<10}\n")
            f.write("-" * 60 + "\n")

            for r in case_results:
                f.write(f"{r['Algorithm']:<20} {r['Cost']:<10} {r['Expanded']:<15} {r['Time']:<10}\n")

    print(f"\nTXT results saved to: {filename}")


# ------------------------------

def save_results_csv(results):
    filename = f"experiments/results_{int(time.time())}.csv"

    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)

        # Header
        writer.writerow(["Case", "Algorithm", "Cost", "Expanded", "Time"])

        # Data
        for case, case_results in results:
            for r in case_results:
                writer.writerow([
                    case,
                    r["Algorithm"],
                    r["Cost"],
                    r["Expanded"],
                    r["Time"]
                ])

    print(f"CSV results saved to: {filename}")


# ------------------------------

if __name__ == "__main__":
    run_all()
