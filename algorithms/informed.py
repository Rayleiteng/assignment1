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
    def recurse(node: Node[S], bound: float) -> Node[S] | float:
        score = node.path_cost + h(node.state)
        if score > bound:
            return score
        if problem.is_goal(node.state):
            return node

        next_bound = math.inf
        for child in node.expand(problem):
            if node.on_path(child.state):
                continue
            result = recurse(child, bound)
            if isinstance(result, Node):
                return result
            next_bound = min(next_bound, result)
        return next_bound

    root = Node(problem.get_initial_state())
    bound = h(root.state)
    while True:
        result = recurse(root, bound)
        if isinstance(result, Node):
            return result
        if result == math.inf:
            return None
        bound = result
