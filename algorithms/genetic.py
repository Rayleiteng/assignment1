"""A generic genetic algorithm for any GeneticProblem, and selection schemes."""
import random
from collections.abc import Callable

from core.optimization import GeneticProblem, T

Selection = Callable[[list[T], list[float]], T]   # (population, fitness scores) -> a parent


def tournament_selection(k: int) -> Selection[T]:
    """Tournaments of k: the fittest of k individuals chosen at random wins."""
    def select(population: list[T], scores: list[float]) -> T:
        contestants = random.sample(range(len(population)), k)
        return population[max(contestants, key=lambda i: scores[i])]
    return select


def roulette_selection(population: list[T], scores: list[float]) -> T:
    """Fitness-proportionate selection; the scores must not be negative, nor all zero."""
    return random.choices(population, weights=scores)[0]


def rank_selection(population: list[T], scores: list[float]) -> T:
    """Rank selection: rank the individuals from the worst (rank 1) to the best (rank N), and
    choose one with probability proportional to its rank. Works with any scores, including
    negative ones."""
    # TODO:
    ranked = [];
    weights = [];

    for i in range(len(population)):
        ranked.append((scores[i], i));
        weights.append(0)
    ranked.sort();

    for i in range(len(ranked)):
        index = ranked[i][1];
        weights[index] = i + 1;
    selected = random.choices(population, weights=weights);
    return selected[0];



def evolve(problem: GeneticProblem[T], population_size: int, generations: int,
           select: Selection[T], mutation_rate: float, elite: int = 1) -> tuple[T, list[float]]:
    """Evolve a random population for the given number of generations. In each generation,
    the `elite` fittest individuals pass unchanged to the next one; every other child is the
    crossover of two selected parents, mutated with probability mutation_rate. Returns the
    best individual of the last generation, and the best fitness of each generation (from the
    initial population to the last one: generations + 1 values)."""
    # TODO: use only the four methods of GeneticProblem, so that the same evolve
    #       works for every problem.
    population = [];
    history = [];
    for i in range(population_size):
        population.append(problem.random_individual());

    for generation in range(generations + 1):
        scores = [];

        for individual in population:
            scores.append(problem.fitness(individual));

        best_index = 0;
        for i in range(len(scores)):
            if scores[i] > scores[best_index]:
                best_index = i;
        best_individual = population[best_index];
        best_fitness = scores[best_index];
        history.append(best_fitness);
        if generation == generations:
            break;
        ranked = [];
        for i in range(len(population)):
            ranked.append((scores[i], i));
        ranked.sort(reverse=True);

        new_population = [];
        for i in range(elite):
            index = ranked[i][1];
            new_population.append(population[index]);
        
        while len(new_population) < population_size:
            parent1 = select(population, scores);
            parent2 = select(population, scores);
            child = problem.crossover(parent1, parent2);
            if random.random() < mutation_rate:
                child = problem.mutate(child);
            new_population.append(child);
        population = new_population;
    return best_individual, history