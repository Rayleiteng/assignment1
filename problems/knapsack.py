"""The 0/1 knapsack problem: choose items of greatest total value whose total weight does not
exceed the capacity. A candidate is a list of 0s and 1s, one per item: 1 means "take it".
"""
import random

from core.optimization import GeneticProblem, OptimizationProblem

Selection = list[int]


class Knapsack(OptimizationProblem[Selection], GeneticProblem[Selection]):
    """For local search, the cost is minus the fitness."""

    def __init__(self, weights: list[int], values: list[int], capacity: int) -> None:
        self.weights = weights
        self.values = values
        self.capacity = capacity

    def total_weight(self, s: Selection) -> int:
        return sum(w for w, take in zip(self.weights, s) if take)

    def total_value(self, s: Selection) -> int:
        return sum(v for v, take in zip(self.values, s) if take)

    def fitness(self, s: Selection) -> float:
        """The total value if the items fit; if they do not, minus the excess weight, so that
        any candidate that fits beats any candidate that does not."""
        # TODO:

        weight = self.total_weight(s);
        if (weight <= self.capacity):
            return self.total_value(s);
        else:
            return - (weight - self.capacity);
        

    def cost(self, s: Selection) -> float:
        # TODO:

        return - self.fitness(s);


    def random_state(self) -> Selection:
        # TODO: each item taken with probability 1/2.

        return [random.choice([0, 1]) for _ in range(len(self.weights))];

    def neighbors(self, s: Selection) -> list[Selection]:
        # TODO: take or leave one item more: one neighbor per item.

        result = [];
        for i in range(len(s)):
            neighbor = s.copy();
            neighbor[i] = 1 - neighbor[i];
            result.append(neighbor);
        return result;


    def random_individual(self) -> Selection:
        return self.random_state()

    def crossover(self, parent1: Selection, parent2: Selection) -> Selection:
        # TODO: one-point crossover.

        if (len(parent1) < 2):
            return parent1.copy();
    
        point = random.randrange(1, len(parent1));
        return parent1[:point] + parent2[point:];


    def mutate(self, s: Selection) -> Selection:
        # TODO: take or leave one random item.

        mutated = s.copy();
        if (len(mutated) == 0):
            return mutated;
        index = random.randrange(len(mutated));
        mutated[index] = 1 - mutated[index];
        return mutated;

