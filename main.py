from __future__ import annotations

import argparse
import os
from typing import List

from algorithms import a_star, bfs, greedy_best_first, ucs
from heuristics import HEURISTICS
from visualization import save_search_progress_frames, save_search_snapshot
from warehouse import Warehouse


def run_algorithm(warehouse: Warehouse, algorithm: str, heuristic_name: str):
    algorithm = algorithm.lower()
    heuristic_name = heuristic_name.lower()

    if algorithm == "bfs":
        return bfs(warehouse)
    if algorithm == "ucs":
        return ucs(warehouse)
    if algorithm == "greedy":
        return greedy_best_first(warehouse, HEURISTICS[heuristic_name], heuristic_name)
    if algorithm == "astar":
        return a_star(warehouse, HEURISTICS[heuristic_name], heuristic_name)
    raise ValueError(f"Unsupported algorithm: {algorithm}")


def print_result(result) -> None:
    print("=" * 72)
    print(f"Algorithm      : {result.algorithm}")
    print(f"Heuristic      : {result.heuristic_name}")
    print(f"Found solution : {result.found}")
    print(f"Steps          : {result.steps}")
    print(f"Total energy   : {result.total_energy}")
    print(f"Nodes expanded : {result.nodes_expanded}")
    print(f"Max frontier   : {result.max_frontier}")
    print(f"Runtime (s)    : {result.elapsed_time:.6f}")
    if result.found:
        print(f"Actions        : {' '.join(result.actions)}")
        print(f"Path           : {result.path}")


def print_summary_table(results: List) -> None:
    print("\nSummary")
    print("-" * 72)
    header = f"{'Algorithm':<28} {'Heuristic':<10} {'Found':<6} {'Steps':<7} {'Energy':<8} {'Expanded':<9}"
    print(header)
    print("-" * len(header))
    for r in results:
        print(f"{r.algorithm:<28} {r.heuristic_name:<10} {str(r.found):<6} {r.steps:<7} {r.total_energy:<8} {r.nodes_expanded:<9}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Warehouse robot multi-item collection")
    parser.add_argument("--map", dest="map_path", default="maps/sample_map.txt", help="Path to map file")
    parser.add_argument("--algorithm", choices=["bfs", "ucs", "greedy", "astar", "all"], default="all")
    parser.add_argument("--heuristic", choices=["h1", "h2"], default="h2")
    parser.add_argument("--visualize", action="store_true", help="Save visualization PNG files")
    parser.add_argument("--frames", action="store_true", help="Save progression frames")
    parser.add_argument("--output-dir", default="outputs", help="Directory for result images")
    args = parser.parse_args()

    warehouse = Warehouse.from_file(args.map_path)
    results = []

    if args.algorithm == "all":
        results.append(run_algorithm(warehouse, "bfs", args.heuristic))
        results.append(run_algorithm(warehouse, "ucs", args.heuristic))
        results.append(run_algorithm(warehouse, "greedy", "h1"))
        results.append(run_algorithm(warehouse, "greedy", "h2"))
        results.append(run_algorithm(warehouse, "astar", "h1"))
        results.append(run_algorithm(warehouse, "astar", "h2"))
    else:
        results.append(run_algorithm(warehouse, args.algorithm, args.heuristic))

    for result in results:
        print_result(result)

        if args.visualize or args.frames:
            safe_algo = result.algorithm.lower().replace(" ", "_").replace("*", "star")
            subdir = os.path.join(args.output_dir, f"{safe_algo}_{result.heuristic_name}")
            os.makedirs(subdir, exist_ok=True)

            snapshot_path = os.path.join(subdir, "snapshot.png")
            save_search_snapshot(warehouse, result, snapshot_path)
            print(f"Saved snapshot : {snapshot_path}")

            if args.frames:
                frames_dir = os.path.join(subdir, "frames")
                files = save_search_progress_frames(warehouse, result, frames_dir, stride=5)
                print(f"Saved frames   : {len(files)} files in {frames_dir}")

    if len(results) > 1:
        print_summary_table(results)


if __name__ == "__main__":
    main()
