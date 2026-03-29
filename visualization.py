from __future__ import annotations

import os
from typing import Dict, List, Optional, Tuple

import matplotlib.pyplot as plt
from matplotlib import colors

from algorithms import SearchResult
from warehouse import Warehouse


BASE_COLORS = {
    "empty": 0,
    "wall": 1,
    "start": 2,
    "item": 3,
    "path": 4,
    "explored": 5,
    "robot": 6,
}

CMAP = colors.ListedColormap([
    "white",      # empty
    "black",      # wall
    "#4C78A8",    # start
    "#F58518",    # item
    "#54A24B",    # path
    "#BDBDBD",    # explored
    "#E45756",    # robot/current
])

BOUNDS = list(range(len(BASE_COLORS) + 1))
NORM = colors.BoundaryNorm(BOUNDS, CMAP.N)


def _base_matrix(warehouse: Warehouse):
    matrix = [[BASE_COLORS["empty"] for _ in range(warehouse.cols)] for _ in range(warehouse.rows)]
    for r in range(warehouse.rows):
        for c in range(warehouse.cols):
            ch = warehouse.grid[r][c]
            if ch == '#':
                matrix[r][c] = BASE_COLORS["wall"]
            elif ch == 'S':
                matrix[r][c] = BASE_COLORS["start"]
            elif ch == 'I':
                matrix[r][c] = BASE_COLORS["item"]
    return matrix


def _draw_grid(ax, warehouse: Warehouse, result: SearchResult, upto_step: Optional[int] = None) -> None:
    matrix = _base_matrix(warehouse)

    if upto_step is None:
        upto_step = len(result.expansion_order)

    first_seen: Dict[Tuple[int, int], int] = {}
    for idx, pos in enumerate(result.expansion_order[:upto_step]):
        if pos not in first_seen and pos != warehouse.start and pos not in warehouse.items:
            first_seen[pos] = idx

    for pos in first_seen:
        r, c = pos
        matrix[r][c] = BASE_COLORS["explored"]

    if result.found:
        for pos in result.path:
            if pos != warehouse.start and pos not in warehouse.items:
                r, c = pos
                matrix[r][c] = BASE_COLORS["path"]

    current_pos = None
    if upto_step > 0 and upto_step <= len(result.expansion_order):
        current_pos = result.expansion_order[upto_step - 1]
    elif result.found and result.path:
        current_pos = result.path[-1]

    if current_pos is not None:
        r, c = current_pos
        matrix[r][c] = BASE_COLORS["robot"]

    ax.imshow(matrix, cmap=CMAP, norm=NORM)
    ax.set_xticks(range(warehouse.cols))
    ax.set_yticks(range(warehouse.rows))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.grid(which="both", color="lightgray", linewidth=0.5)
    ax.set_title(
        f"{result.algorithm} | heuristic={result.heuristic_name} | "
        f"expanded={min(upto_step, len(result.expansion_order))}/{len(result.expansion_order)}"
    )

    for r in range(warehouse.rows):
        for c in range(warehouse.cols):
            ch = warehouse.grid[r][c]
            label = None
            if ch.isdigit():
                label = ch
            elif ch in {'S', 'I'}:
                label = ch
            if label:
                ax.text(c, r, label, ha="center", va="center", color="white", fontsize=10, fontweight="bold")


def save_search_snapshot(warehouse: Warehouse, result: SearchResult, output_path: str) -> None:
    fig, ax = plt.subplots(figsize=(7, 7))
    _draw_grid(ax, warehouse, result, upto_step=None)
    subtitle = (
        f"Found={result.found} | steps={result.steps} | energy={result.total_energy} | "
        f"expanded={result.nodes_expanded}"
    )
    fig.text(0.5, 0.02, subtitle, ha="center", fontsize=10)
    plt.tight_layout(rect=(0, 0.05, 1, 1))
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def save_search_progress_frames(warehouse: Warehouse, result: SearchResult, output_dir: str, stride: int = 5) -> List[str]:
    """Save multiple frames showing search progression.

    This is a simple, dependable interpretation of "visualization of the search process":
    you get stepwise images of the expanding search, plus a final snapshot.
    """
    os.makedirs(output_dir, exist_ok=True)
    saved_files: List[str] = []
    total = len(result.expansion_order)
    frame_steps = list(range(1, total + 1, max(1, stride)))
    if total not in frame_steps:
        frame_steps.append(total)

    for i, step in enumerate(frame_steps, start=1):
        fig, ax = plt.subplots(figsize=(7, 7))
        _draw_grid(ax, warehouse, result, upto_step=step)
        fig.text(0.5, 0.02, f"Expansion step {step}/{total}", ha="center", fontsize=10)
        plt.tight_layout(rect=(0, 0.05, 1, 1))
        path = os.path.join(output_dir, f"frame_{i:03d}.png")
        fig.savefig(path, dpi=160)
        plt.close(fig)
        saved_files.append(path)

    final_path = os.path.join(output_dir, "final.png")
    save_search_snapshot(warehouse, result, final_path)
    saved_files.append(final_path)
    return saved_files
