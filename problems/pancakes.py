"""The pancake problem: sort a stack of pancakes by repeatedly flipping the top k of them.

The pancakes have sizes 1, ..., n; a stack lists them from the top down, and it is sorted
when the smallest is on top: (1, 2, ..., n). Flipping k pancakes (2 <= k <= n) reverses
the order of the top k. Flips are their own inverse: flipping the same k twice undoes it.
"""
from collections.abc import Iterable

from core.reversible import ReversibleSearchProblem
from core.search_state import SearchState


class PancakeState(SearchState):
    """A stack of pancakes, from the top down."""

    def __init__(self, stack: tuple[int, ...]) -> None:
        self.stack = stack

    def key(self) -> tuple[int, ...]:
        return self.stack

    def __str__(self) -> str:
        return " ".join(str(p) for p in self.stack)


class PancakeProblem(ReversibleSearchProblem[PancakeState]):
    """Sort a stack with flips. Action names are "flip k".

    flip_cost=False: every flip costs 1. flip_cost=True: flipping k pancakes costs k.
    """

    def __init__(self, stack: tuple[int, ...], flip_cost: bool = False) -> None:
        self.stack = stack
        self.flip_cost = flip_cost

    def get_initial_state(self) -> PancakeState:
        return PancakeState(self.stack)

    def get_goal_state(self) -> PancakeState:
        # just return the sorted stack, which is always (1, 2, ..., n)
        return PancakeState(tuple(range(1, len(self.stack) + 1)))

    def is_goal(self, state: PancakeState) -> bool:
        # check if the current state is the goal state
        return state == self.get_goal_state()

    def get_successors(self, state: PancakeState) -> Iterable[tuple[PancakeState, str]]:
        # generate all possible flips of the current stack
        for k in range(2, len(state.stack) + 1):
            flipped = state.stack[:k][::-1] + state.stack[k:]
            yield PancakeState(flipped), f"flip {k}"

    def get_predecessors(self, state: PancakeState) -> Iterable[tuple[PancakeState, str]]:
        # A flip is its own inverse.
        return self.get_successors(state)

    def get_action_cost(self, state: PancakeState, action: str, next_state: PancakeState) -> float:
        # return the cost of the action based on whether it is flip cost or not
        k = int(action.split()[1])
        return float(k if self.flip_cost else 1)


def gap_heuristic(state: PancakeState) -> float:
    """The number of gaps: pairs of adjacent pancakes whose sizes differ by more than 1.
    The plate counts as a pancake of size n + 1 under the stack."""
    # Count the number of gaps in the stack, including the plate as a pancake of size n + 1
    stack = state.stack
    with_plate = stack + (len(stack) + 1,)
    return float(
        sum(abs(a - b) > 1 for a, b in zip(with_plate, with_plate[1:]))
    )


def my_heuristic(state: PancakeState) -> float:
    """A heuristic of your own design, for unit-cost flips. In the report, say whether it is
    admissible and consistent, with a proof or a counterexample."""
    # based on the gap heuristic, but if the first pancake is 1 and the stack is not sorted, return at least 3
    gaps = gap_heuristic(state)
    goal = tuple(range(1, len(state.stack) + 1))

    if state.stack and state.stack[0] == 1 and state.stack != goal:
        return max(gaps, 3.0)
    return gaps


def flip_cost_heuristic(state: PancakeState) -> float:
    """An admissible heuristic for the variant where flipping k pancakes costs k, better
    informed than gap_heuristic. Prove its admissibility in the report."""
    # if the stack is empty, return 0. Otherwise, return 2 * gaps + (n - 2 if the last pancake is not n else 0)
    n = len(state.stack)
    if n == 0:
        return 0.0

    gaps = gap_heuristic(state)
    plate_gap = state.stack[-1] != n
    return 2 * gaps + (n - 2 if plate_gap else 0)
