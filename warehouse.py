from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple

Position = Tuple[int, int]


@dataclass(frozen=True)
class State:
    """Search state: robot position + bitmask of collected items."""

    position: Position
    collected_mask: int


class Warehouse:
    """Grid warehouse for multi-item collection with weighted movement costs.

    Map symbols:
        S = start
        I = item (collect automatically when entered)
        # = wall/obstacle
        . = normal traversable cell with cost 1
        1-9 = traversable cell whose entry energy cost equals that digit

    Movement is 4-directional. The energy cost of a move is the cost of ENTERING
    the destination cell.
    """

    def __init__(self, grid_lines: List[str]) -> None:
        if not grid_lines:
            raise ValueError("Grid cannot be empty.")

        self.grid: List[List[str]] = [list(row.rstrip("\n")) for row in grid_lines]
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])

        if any(len(row) != self.cols for row in self.grid):
            raise ValueError("All grid rows must have the same length.")

        self.start: Optional[Position] = None
        self.items: List[Position] = []
        self.item_to_index: Dict[Position, int] = {}
        self.walkable: Set[Position] = set()

        for r in range(self.rows):
            for c in range(self.cols):
                ch = self.grid[r][c]
                if ch != '#':
                    self.walkable.add((r, c))
                if ch == 'S':
                    if self.start is not None:
                        raise ValueError("Map must contain exactly one start S.")
                    self.start = (r, c)
                elif ch == 'I':
                    self.item_to_index[(r, c)] = len(self.items)
                    self.items.append((r, c))

        if self.start is None:
            raise ValueError("Map must contain one start S.")
        if not self.items:
            raise ValueError("Map must contain at least one item I.")

        self.goal_mask = (1 << len(self.items)) - 1
        self.min_step_cost = min(self.cell_cost(pos) for pos in self.walkable)

    @classmethod
    def from_file(cls, path: str) -> "Warehouse":
        with open(path, "r", encoding="utf-8") as f:
            lines = [line.rstrip("\n") for line in f if line.strip("\n")]
        return cls(lines)

    def in_bounds(self, pos: Position) -> bool:
        r, c = pos
        return 0 <= r < self.rows and 0 <= c < self.cols

    def is_walkable(self, pos: Position) -> bool:
        return pos in self.walkable

    def symbol(self, pos: Position) -> str:
        r, c = pos
        return self.grid[r][c]

    def cell_cost(self, pos: Position) -> int:
        ch = self.symbol(pos)
        if ch.isdigit():
            return int(ch)
        return 1

    def initial_state(self) -> State:
        mask = 0
        if self.start in self.item_to_index:
            mask |= 1 << self.item_to_index[self.start]
        return State(self.start, mask)

    def is_goal(self, state: State) -> bool:
        return state.collected_mask == self.goal_mask

    def collect_mask(self, pos: Position, current_mask: int) -> int:
        if pos in self.item_to_index:
            return current_mask | (1 << self.item_to_index[pos])
        return current_mask

    def neighbors(self, state: State) -> List[Tuple[State, int, str]]:
        r, c = state.position
        moves = [(-1, 0, 'U'), (1, 0, 'D'), (0, -1, 'L'), (0, 1, 'R')]
        result: List[Tuple[State, int, str]] = []

        for dr, dc, action in moves:
            nxt = (r + dr, c + dc)
            if not self.in_bounds(nxt) or not self.is_walkable(nxt):
                continue
            new_mask = self.collect_mask(nxt, state.collected_mask)
            cost = self.cell_cost(nxt)
            result.append((State(nxt, new_mask), cost, action))

        return result

    def remaining_items(self, state: State) -> List[Position]:
        rem: List[Position] = []
        for idx, pos in enumerate(self.items):
            if not (state.collected_mask & (1 << idx)):
                rem.append(pos)
        return rem

    def state_id(self, state: State) -> Tuple[Position, int]:
        return state.position, state.collected_mask
