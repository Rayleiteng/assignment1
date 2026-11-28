"""Graph coloring: give each node of a graph one of k colors, so that no edge joins two nodes
of the same color. A candidate is a list of colors (0 to k - 1), one per node.
"""
import random

from core.optimization import GeneticProblem, OptimizationProblem

Coloring = list[int]


class GraphColoring(OptimizationProblem[Coloring], GeneticProblem[Coloring]):
    """The cost is the number of conflicts: edges whose two ends have the same color. The
    fitness is the number of edges without a conflict."""

    def __init__(self, n: int, edges: list[tuple[int, int]], k: int) -> None:
        self.n = n
        self.edges = edges
        self.k = k

    def conflicts(self, c: Coloring) -> int:
        # TODO:

        count = 0;
        for (u, v) in self.edges:
            if (c[u] == c[v]):
                count += 1;
        return count;


    def cost(self, c: Coloring) -> float:
        return self.conflicts(c)

    def fitness(self, c: Coloring) -> float:
        return len(self.edges) - self.conflicts(c)

    def random_state(self) -> Coloring:
        # TODO:

        colors = [];
        for i in range(self.n):
            colors.append(random.randrange(self.k));
        return colors;  


    def neighbors(self, c: Coloring) -> list[Coloring]:
        # TODO: give one node another color: n * (k - 1) neighbors.

        result = [];
        for i in range(self.n):
            for color in range(self.k):
                if (color != c[i]):
                    neighbor = c.copy();
                    neighbor[i] = color;
                    result.append(neighbor);
        return result;

    def random_individual(self) -> Coloring:
        return self.random_state()

    def crossover(self, parent1: Coloring, parent2: Coloring) -> Coloring:
        # TODO: uniform crossover: each node takes its color from either parent,
        #       at random.

        child = [];
        for i in range(self.n):
            x = random.random();
            if (x < 0.5):
                child.append(parent1[i]);
            else:
                child.append(parent2[i]);
        return child;


    def mutate(self, c: Coloring) -> Coloring:
        # TODO: give one random node a random color.

        mutated = c.copy();

        if (self.n == 0):
            return mutated;
        if (self.k <= 1):
            return mutated;

        index = random.randrange(self.n);
        new_color = random.randrange(self.k);
        
        while (new_color == mutated[index]):
            new_color = random.randrange(self.k);
        mutated[index] = new_color;

        return mutated;