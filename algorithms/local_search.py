"""Local search for any OptimizationProblem: hill climbing and its variants. Each function
returns the best state found and the number of moves (or steps) it made."""
import random
from collections.abc import Callable
from typing import Optional

from core.optimization import OptimizationProblem, T



def hill_climbing(problem: OptimizationProblem[T], start: Optional[T] = None) -> tuple[T, int]:
    """Steepest descent: move to the best neighbor (ties broken at random) as long as it is
    better than the current state. Starts from start, or from a random state."""
    current = problem.random_state() if start is None else start
    moves = 0
    while True:
        candidates = problem.neighbors(current)
        costs = [problem.cost(c) for c in candidates]
        least = min(costs)
        if least >= problem.cost(current):
            return current, moves
        current = random.choice([c for c, k in zip(candidates, costs) if k == least])
        moves += 1


def stochastic_hill_climbing(problem: OptimizationProblem[T], start: Optional[T] = None) -> tuple[T, int]:
    """Move to a neighbor chosen at random among those better than the current state, until
    no neighbor is better."""
    # TODO:

    if start is None:
        current = problem.random_state();
    else:
        current = start;
    moves = 0;
    while True:
        candidates = problem.neighbors(current);
        current_cost = problem.cost(current);
        waiting_list = [];

        for neighbor in candidates:
            if problem.cost(neighbor) < current_cost:
                waiting_list.append(neighbor);
        
        if len(waiting_list) == 0:
            return current, moves;
    
        next_candidates = random.choice(waiting_list);
        moves += 1;
        current = next_candidates;


def random_restart(problem: OptimizationProblem[T],
                   search: Callable[[OptimizationProblem[T]], tuple[T, int]],
                   restarts: int) -> tuple[T, int]:
    """Run search (which starts from a random state) up to `restarts` times and keep the best
    result; stop early if a state of cost 0 is found. Returns the best state and the total
    number of moves of all the runs."""
    # TODO:
    best_state, moves = search(problem)
    best_cost = problem.cost(best_state)
    total_moves = moves
    if best_cost == 0:
        return best_state, total_moves
    
    for i in range(restarts - 1):

        state, moves = search(problem)
        cost = problem.cost(state)
        total_moves += moves

        if cost < best_cost:
            best_state = state
            best_cost = cost
        if best_cost == 0:
            break
    return best_state, total_moves



def local_beam_search(problem: OptimizationProblem[T], k: int, max_steps: int = 1000) -> tuple[T, int]:
    """Local beam search: start from k random states; at each step, keep the k best states
    among all the neighbors of the current k (without duplicates). Stop when the best of them
    is no better than the best state found so far, or after max_steps steps. Returns the best
    state found and the number of steps."""
    # TODO: states may be lists, which cannot be put in a set; to remove
    #       duplicates, you can compare their tuple(...) versions.
    states = [];
    steps = 0;
    for i in range(k):
        states.append(problem.random_state());
    best_state = states[0];
    best_cost = problem.cost(best_state);

    for state in states:
        cost = problem.cost(state);
        if cost < best_cost:
            best_state = state;
            best_cost = cost;
    
    while steps < max_steps:

        all_neighbors = [];
        seen = set();
        for state in states:
            neighbors = problem.neighbors(state);
            for neighbor in neighbors:
                if tuple(neighbor) not in seen:
                    seen.add(tuple(neighbor));
                    all_neighbors.append(neighbor);
        if len(all_neighbors) == 0:
            break;
        all_neighbors.sort(key = problem.cost);

        new_best_state = all_neighbors[0];
        new_best_cost = problem.cost(new_best_state);
        if new_best_cost >= best_cost:
            break;
        states = all_neighbors[:k];
        best_state = new_best_state;
        best_cost = new_best_cost;
        steps += 1;
    return best_state, steps;