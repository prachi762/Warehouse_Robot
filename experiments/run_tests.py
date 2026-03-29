import time
from demo_cases.load_cases import load_case

from algorithms.bfs import bfs
from algorithms.ucs import ucs
from algorithms.gbfs import gbfs
from algorithms.astar import astar

from heuristics.manhattan import get_manhattan
from heuristics.landmark import (
    get_landmark_heuristic,
    precompute_landmarks
)


def run_all():

    cases = ["easy", "medium", "hard"]

    results = []

    for case in cases:
        print(f"\n===== Running Case: {case} =====")

        grid = load_case(case)

        start_state = __import__("core.state", fromlist=["State"]).State(
            grid.start[0],
            grid.start[1],
            0,
            grid.energy
        )

        dx, dy = grid.delivery

        # Heuristics
        h_manhattan = get_manhattan(dx, dy)

        landmarks = [(0,0), (grid.N-1, grid.N-1)]
        dist_table = precompute_landmarks(grid, landmarks)
        h_landmark = get_landmark_heuristic(dx, dy, dist_table, landmarks)

        # Algorithms list
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

            start_time = time.time()

            if heuristic:
                path, expanded, cost = algo(grid, start_state, heuristic)
            else:
                path, expanded, cost = algo(grid, start_state)

            end_time = time.time()

            runtime = end_time - start_time

            case_results.append({
                "Algorithm": name,
                "Cost": cost,
                "Expanded": expanded,
                "Time": round(runtime, 5)
            })

        results.append((case, case_results))

        # Print table
        print_table(case, case_results)

    # Save results
    save_results(results)


def print_table(case, case_results):
    print(f"\nResults for {case}:\n")

    print(f"{'Algorithm':<20} {'Cost':<10} {'Expanded':<15} {'Time(s)':<10}")
    print("-" * 60)

    for r in case_results:
        print(f"{r['Algorithm']:<20} {r['Cost']:<10} {r['Expanded']:<15} {r['Time']:<10}")


def save_results(results):
    with open("experiments/results.txt", "w") as f:

        for case, case_results in results:
            f.write(f"\n===== Case: {case} =====\n\n")
            f.write(f"{'Algorithm':<20} {'Cost':<10} {'Expanded':<15} {'Time(s)':<10}\n")
            f.write("-" * 60 + "\n")

            for r in case_results:
                f.write(f"{r['Algorithm']:<20} {r['Cost']:<10} {r['Expanded']:<15} {r['Time']:<10}\n")


if __name__ == "__main__":
    run_all()
