from __future__ import annotations

import heapq
import itertools
import time
from collections import deque
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Set, Tuple

from warehouse import State, Warehouse

HeuristicFn = Callable[[State, Warehouse], int]


@dataclass
class SearchResult:
    algorithm: str
    heuristic_name: str
    found: bool
    path: List[Tuple[int, int]]
    actions: List[str]
    total_energy: int
    steps: int
    nodes_expanded: int
    max_frontier: int
    elapsed_time: float
    expansion_order: List[Tuple[int, int]]
    expansion_states: List[State]


@dataclass
class Node:
    state: State
    parent: Optional['Node']
    action: Optional[str]
    g: int
    h: int

    @property
    def f(self) -> int:
        return self.g + self.h


def reconstruct(node: Node) -> Tuple[List[Tuple[int, int]], List[str]]:
    path: List[Tuple[int, int]] = []
    actions: List[str] = []
    cur: Optional[Node] = node
    while cur is not None:
        path.append(cur.state.position)
        if cur.action is not None:
            actions.append(cur.action)
        cur = cur.parent
    path.reverse()
    actions.reverse()
    return path, actions


def _empty_result(name: str, heuristic_name: str, t0: float,
                  expanded: int, max_frontier: int,
                  expansion_order: List[Tuple[int, int]],
                  expansion_states: List[State]) -> SearchResult:
    return SearchResult(
        algorithm=name,
        heuristic_name=heuristic_name,
        found=False,
        path=[],
        actions=[],
        total_energy=0,
        steps=0,
        nodes_expanded=expanded,
        max_frontier=max_frontier,
        elapsed_time=time.perf_counter() - t0,
        expansion_order=expansion_order,
        expansion_states=expansion_states,
    )


def bfs(warehouse: Warehouse) -> SearchResult:
    t0 = time.perf_counter()
    start = warehouse.initial_state()
    root = Node(start, None, None, 0, 0)

    frontier = deque([root])
    visited: Set[Tuple[Tuple[int, int], int]] = {warehouse.state_id(start)}
    expansion_order: List[Tuple[int, int]] = []
    expansion_states: List[State] = []
    expanded = 0
    max_frontier = 1

    while frontier:
        node = frontier.popleft()
        expanded += 1
        expansion_order.append(node.state.position)
        expansion_states.append(node.state)

        if warehouse.is_goal(node.state):
            path, actions = reconstruct(node)
            return SearchResult(
                algorithm="BFS",
                heuristic_name="-",
                found=True,
                path=path,
                actions=actions,
                total_energy=node.g,
                steps=len(actions),
                nodes_expanded=expanded,
                max_frontier=max_frontier,
                elapsed_time=time.perf_counter() - t0,
                expansion_order=expansion_order,
                expansion_states=expansion_states,
            )

        for next_state, cost, action in warehouse.neighbors(node.state):
            sid = warehouse.state_id(next_state)
            if sid in visited:
                continue
            visited.add(sid)
            frontier.append(Node(next_state, node, action, node.g + cost, 0))
        max_frontier = max(max_frontier, len(frontier))

    return _empty_result("BFS", "-", t0, expanded, max_frontier, expansion_order, expansion_states)


def ucs(warehouse: Warehouse) -> SearchResult:
    t0 = time.perf_counter()
    start = warehouse.initial_state()
    root = Node(start, None, None, 0, 0)

    counter = itertools.count()
    frontier: List[Tuple[int, int, Node]] = [(0, next(counter), root)]
    best_cost: Dict[Tuple[Tuple[int, int], int], int] = {warehouse.state_id(start): 0}
    closed: Set[Tuple[Tuple[int, int], int]] = set()
    expansion_order: List[Tuple[int, int]] = []
    expansion_states: List[State] = []
    expanded = 0
    max_frontier = 1

    while frontier:
        _, _, node = heapq.heappop(frontier)
        sid = warehouse.state_id(node.state)
        if sid in closed:
            continue
        closed.add(sid)

        expanded += 1
        expansion_order.append(node.state.position)
        expansion_states.append(node.state)

        if warehouse.is_goal(node.state):
            path, actions = reconstruct(node)
            return SearchResult(
                algorithm="UCS",
                heuristic_name="-",
                found=True,
                path=path,
                actions=actions,
                total_energy=node.g,
                steps=len(actions),
                nodes_expanded=expanded,
                max_frontier=max_frontier,
                elapsed_time=time.perf_counter() - t0,
                expansion_order=expansion_order,
                expansion_states=expansion_states,
            )

        for next_state, cost, action in warehouse.neighbors(node.state):
            next_sid = warehouse.state_id(next_state)
            new_g = node.g + cost
            if next_sid in closed and new_g >= best_cost.get(next_sid, float('inf')):
                continue
            if new_g < best_cost.get(next_sid, float('inf')):
                best_cost[next_sid] = new_g
                heapq.heappush(frontier, (new_g, next(counter), Node(next_state, node, action, new_g, 0)))
        max_frontier = max(max_frontier, len(frontier))

    return _empty_result("UCS", "-", t0, expanded, max_frontier, expansion_order, expansion_states)


def greedy_best_first(warehouse: Warehouse, heuristic: HeuristicFn, heuristic_name: str) -> SearchResult:
    t0 = time.perf_counter()
    start = warehouse.initial_state()
    root = Node(start, None, None, 0, heuristic(start, warehouse))

    counter = itertools.count()
    frontier: List[Tuple[int, int, Node]] = [(root.h, next(counter), root)]
    visited: Set[Tuple[Tuple[int, int], int]] = set()
    seen_best_h: Dict[Tuple[Tuple[int, int], int], int] = {warehouse.state_id(start): root.h}
    expansion_order: List[Tuple[int, int]] = []
    expansion_states: List[State] = []
    expanded = 0
    max_frontier = 1

    while frontier:
        _, _, node = heapq.heappop(frontier)
        sid = warehouse.state_id(node.state)
        if sid in visited:
            continue
        visited.add(sid)

        expanded += 1
        expansion_order.append(node.state.position)
        expansion_states.append(node.state)

        if warehouse.is_goal(node.state):
            path, actions = reconstruct(node)
            return SearchResult(
                algorithm="Greedy Best-First Search",
                heuristic_name=heuristic_name,
                found=True,
                path=path,
                actions=actions,
                total_energy=node.g,
                steps=len(actions),
                nodes_expanded=expanded,
                max_frontier=max_frontier,
                elapsed_time=time.perf_counter() - t0,
                expansion_order=expansion_order,
                expansion_states=expansion_states,
            )

        for next_state, cost, action in warehouse.neighbors(node.state):
            next_sid = warehouse.state_id(next_state)
            if next_sid in visited:
                continue
            h = heuristic(next_state, warehouse)
            if h < seen_best_h.get(next_sid, float('inf')):
                seen_best_h[next_sid] = h
                heapq.heappush(frontier, (h, next(counter), Node(next_state, node, action, node.g + cost, h)))
        max_frontier = max(max_frontier, len(frontier))

    return _empty_result("Greedy Best-First Search", heuristic_name, t0, expanded, max_frontier, expansion_order, expansion_states)


def a_star(warehouse: Warehouse, heuristic: HeuristicFn, heuristic_name: str) -> SearchResult:
    t0 = time.perf_counter()
    start = warehouse.initial_state()
    root_h = heuristic(start, warehouse)
    root = Node(start, None, None, 0, root_h)

    counter = itertools.count()
    frontier: List[Tuple[int, int, Node]] = [(root.f, next(counter), root)]
    best_cost: Dict[Tuple[Tuple[int, int], int], int] = {warehouse.state_id(start): 0}
    closed: Set[Tuple[Tuple[int, int], int]] = set()
    expansion_order: List[Tuple[int, int]] = []
    expansion_states: List[State] = []
    expanded = 0
    max_frontier = 1

    while frontier:
        _, _, node = heapq.heappop(frontier)
        sid = warehouse.state_id(node.state)

        if sid in closed:
            continue
        closed.add(sid)

        expanded += 1
        expansion_order.append(node.state.position)
        expansion_states.append(node.state)

        if warehouse.is_goal(node.state):
            path, actions = reconstruct(node)
            return SearchResult(
                algorithm="A* Search",
                heuristic_name=heuristic_name,
                found=True,
                path=path,
                actions=actions,
                total_energy=node.g,
                steps=len(actions),
                nodes_expanded=expanded,
                max_frontier=max_frontier,
                elapsed_time=time.perf_counter() - t0,
                expansion_order=expansion_order,
                expansion_states=expansion_states,
            )

        for next_state, cost, action in warehouse.neighbors(node.state):
            next_sid = warehouse.state_id(next_state)
            new_g = node.g + cost
            if next_sid in closed and new_g >= best_cost.get(next_sid, float('inf')):
                continue
            if new_g < best_cost.get(next_sid, float('inf')):
                best_cost[next_sid] = new_g
                h = heuristic(next_state, warehouse)
                child = Node(next_state, node, action, new_g, h)
                heapq.heappush(frontier, (child.f, next(counter), child))
        max_frontier = max(max_frontier, len(frontier))

    return _empty_result("A* Search", heuristic_name, t0, expanded, max_frontier, expansion_order, expansion_states)
