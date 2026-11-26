import math
from collections.abc import Callable
from typing import Optional

from algorithms.uninformed import graph_search
from core.frontier import PriorityFrontier
from core.node import Node
from core.search_problem import S, SearchProblem

Heuristic = Callable[[S], float]


def best_first_search(problem: SearchProblem[S], f: Callable[[Node[S]], float]) -> Optional[Node[S]]:
    """Graph search that always expands the node with the lowest f."""
    return graph_search(problem, PriorityFrontier(f))


def greedy_search(problem: SearchProblem[S], h: Heuristic[S]) -> Optional[Node[S]]:
    """Greedy best-first search: f(n) = h(n)."""
    return best_first_search(problem, lambda n: h(n.state))


def a_star_search(problem: SearchProblem[S], h: Heuristic[S]) -> Optional[Node[S]]:
    """A*: f(n) = g(n) + h(n)."""
    return best_first_search(problem, lambda n: n.path_cost + h(n.state))


def weighted_a_star_search(problem: SearchProblem[S], h: Heuristic[S], w: float) -> Optional[Node[S]]:
    """Weighted A*: f(n) = g(n) + w * h(n), with w >= 1."""
    return best_first_search(problem, lambda n: n.path_cost + w * h(n.state))


def ida_star_search(problem: SearchProblem[S], h: Heuristic[S]) -> Optional[Node[S]]:
    """Iterative deepening A*: a series of depth-first searches, each limited by a bound on
    f = g + h. The first bound is h(initial state); each new bound is the smallest f that
    exceeded the previous one. Like depth_limited_search, it skips states already on the
    current path. Returns a goal node, or None if there is no solution."""
    # TODO: write it, with a recursive helper function that searches
    #       depth-first from a node within the bound, and returns either a goal node or the
    #       smallest f above the bound that it saw (math.inf if none).
    raise NotImplementedError("ida_star_search")   # remove this line when you are done
