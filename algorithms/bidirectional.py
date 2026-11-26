from collections.abc import Callable, Iterable
from typing import Optional

from core.node import Node
from core.reversible import ReversibleSearchProblem
from core.search_problem import S


def bidirectional_search(problem: ReversibleSearchProblem[S]) -> Optional[Node[S]]:
    """Bidirectional breadth-first search: one search forward from the initial state, and
    one backward from the goal state, expanding one complete layer at a time (always the
    side with the smaller layer) until they meet. Returns a goal node whose path has the
    fewest possible steps, or None if there is no solution."""
    def expand_backward(node: Node[S]) -> Iterable[Node[S]]:
        for state, action in problem.get_predecessors(node.state):
            # The parent is the next node towards the goal.
            yield Node(state, node, action, depth=node.depth + 1)

    def expand_layer(
        layer: list[Node[S]],
        reached: dict[S, Node[S]],
        opposite: dict[S, Node[S]],
        expand: Callable[[Node[S]], Iterable[Node[S]]],
    ) -> tuple[list[Node[S]], Optional[S]]:
        next_layer: list[Node[S]] = []
        meetings: list[S] = []
        for node in layer:
            for child in expand(node):
                if child.state in reached:
                    continue
                reached[child.state] = child
                next_layer.append(child)
                if child.state in opposite:
                    meetings.append(child.state)
        meeting = min(
            meetings,
            key=lambda state: reached[state].depth + opposite[state].depth,
            default=None,
        )
        return next_layer, meeting

    def join_paths(forward: Node[S], backward: Node[S]) -> Node[S]:
        while backward.parent is not None:
            next_node = backward.parent
            action = backward.action
            assert action is not None
            step_cost = problem.get_action_cost(forward.state, action, next_node.state)
            forward = Node(
                next_node.state, forward, action, forward.path_cost + step_cost, forward.depth + 1
            )
            backward = next_node
        return forward

    start = Node(problem.get_initial_state())
    goal = Node(problem.get_goal_state())
    if start.state == goal.state:
        return start

    forward_layer = [start]
    backward_layer = [goal]
    forward_reached = {start.state: start}
    backward_reached = {goal.state: goal}

    while forward_layer and backward_layer:
        if len(forward_layer) <= len(backward_layer):
            forward_layer, meeting = expand_layer(
                forward_layer, forward_reached, backward_reached, lambda node: node.expand(problem)
            )
        else:
            backward_layer, meeting = expand_layer(
                backward_layer, backward_reached, forward_reached, expand_backward
            )
        if meeting is not None:
            return join_paths(forward_reached[meeting], backward_reached[meeting])
    return None
