import random
import pytest
from puzzle.state import State, GOAL_STATE
from algorithms.bfs import BFS
from algorithms.dfs import DFS
from algorithms.a_star import AStar


def apply(tiles, actions):
    s = State(tiles)
    for a in actions:
        s = next(c for c in s.neighbors() if c.action == a)
    return s.tiles


def scrambled(n, seed):
    rng = random.Random(seed)
    s = State(GOAL_STATE)
    for _ in range(n):
        s = rng.choice(s.neighbors())
    return State(s.tiles)


CASES = [State((1, 2, 3, 4, 5, 6, 0, 7, 8)), State((1, 2, 3, 0, 4, 6, 7, 5, 8))] + [
    scrambled(20, i) for i in range(5)
]


def test_goal_is_trivial():
    for algo in (BFS(), DFS(), AStar()):
        r = algo.search(State(GOAL_STATE))
        assert r.found and r.depth == 0 and r.actions == []


@pytest.mark.parametrize("initial", CASES)
def test_solutions_are_valid_and_optimal(initial):
    bfs, dfs, astar = BFS().search(initial), DFS().search(initial), AStar().search(initial)
    for r in (bfs, dfs, astar):
        assert r.found
        assert apply(initial.tiles, r.actions) == GOAL_STATE
        assert r.depth == len(r.actions) == r.path_cost
    assert astar.depth == bfs.depth
    assert astar.nodes_expanded <= bfs.nodes_expanded


def test_unsolvable():
    initial = State((2, 8, 3, 1, 6, 4, 7, 0, 5))
    for algo in (BFS(), DFS(), AStar()):
        assert not algo.search(initial).found


def test_heuristic_admissible():
    a = AStar()
    for s in CASES:
        assert a.heuristic(s) <= BFS().search(s).depth
