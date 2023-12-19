########################################################
#
# CMPSC 441: Homework 4
#
########################################################



student_name = 'Ilaaksh'
student_email = 'ijm5304@psu.edu'



########################################################
# Import
########################################################

from hw4_utils import *
import math
import random



# Add your imports here if used






################################################################
# 1. Genetic Algorithm
################################################################


def genetic_algorithm(problem, f_thres, ngen=1000):
    population = problem.init_population()
    best = problem.fittest(population, f_thres)

    if best is not None:
        return -1, best

    for i in range(ngen):
        population = problem.next_generation(population)
        best = problem.fittest(population, f_thres)

        if best is not None:
            return i, best

    best = problem.fittest(population)
    return ngen, best


################################################################
# 2. NQueens Problem
################################################################


class NQueensProblem(GeneticProblem):
    def __init__(self, n, g_bases, g_len, m_prob):
        super().__init__(n, g_bases, g_len, m_prob)

    def init_population(self):

        population = []
        for _ in range(self.n):
            chromosome = tuple(random.choice(self.g_bases) for _ in range(self.g_len))
            population.append(chromosome)
        return population

    def next_generation(self, population):

        new_generation = []
        for _ in range(self.n):
            parent1 = random.choice(population)
            parent2 = random.choice(population)
            offspring = self.crossover(parent1, parent2)
            offspring = self.mutate(offspring)
            new_generation.append(offspring)
        return new_generation

    def mutate(self, chrom):

        mutated_chrom = list(chrom)
        if random.random() < self.m_prob:
            index_to_mutate = random.randint(0, self.g_len - 1)
            mutated_chrom[index_to_mutate] = random.choice(self.g_bases)
        return tuple(mutated_chrom)

    def crossover(self, chrom1, chrom2):

        crossover_point = random.randint(1, self.g_len - 1)
        offspring = chrom1[:crossover_point] + chrom2[crossover_point:]
        return offspring

    def fitness_fn(self, chrom):

        non_attacking_queens = 0
        for i in range(self.g_len):
            for j in range(i + 1, self.g_len):
                if chrom[i] != chrom[j] and abs(i - j) != abs(chrom[i] - chrom[j]):
                # The queens at positions i and j do not attack each other
                    non_attacking_queens += 1

        return non_attacking_queens

    def select(self, m, population):

        selected = random.choices(population, weights=[self.fitness_fn(chrom) for chrom in population], k=m)
        return selected

    def fittest(self, population, f_thres=None):

        best_chromosome = max(population, key=self.fitness_fn)
        if f_thres is None or self.fitness_fn(best_chromosome) >= f_thres:
            return best_chromosome
        else:
            return None






################################################################
# 3. Function Optimaization f(x,y) = x sin(4x) + 1.1 y sin(2y)
################################################################

class FunctionProblem(GeneticProblem):
    def __init__(self, n, g_bases, g_len, m_prob):
        super().__init__(n, g_bases, g_len, m_prob)


    def init_population(self):
        return [(random.uniform(0, self.g_bases[0]), random.uniform(0, self.g_bases[1])) for _ in range(self.n)]

    def next_generation(self, population):
        new_generation = []
        while len(new_generation) < self.n:
            parent1 = self.select(1, population)[0]
            parent2 = self.select(1, population)[0]
            child = self.crossover(parent1, parent2)
            child = self.mutate(child)

            new_generation.append(child)

        return new_generation

    def mutate(self, chrom):
        mutated_chrom = list(chrom)
        for i in range(len(mutated_chrom)):
            if random.random() < self.m_prob:
                mutated_chrom[i] = random.choice(self.g_bases)
        return tuple(mutated_chrom)

    def crossover(self, chrom1, chrom2):
        component_to_interpolate = random.choice([0, 1])

        alpha = random.uniform(0, 1)

        if component_to_interpolate == 0:
            xnew = (1 - alpha) * chrom1[0] + alpha * chrom2[0]
            offspring = (xnew, chrom1[1])
        else:
            ynew = (1 - alpha) * chrom1[1] + alpha * chrom2[1]
            offspring = (chrom1[0], ynew)

        return offspring

    def fitness_fn(self, chrom):
        x, y = chrom
        fitness_value = x * math.sin(4 * x) + 1.1 * y * math.sin(2 * y)
        return fitness_value

    def select(self, m, population):
        fitness_values = [self.fitness_fn(chrom) for chrom in population]
        selected_indices = random.choices(range(len(population)), weights=fitness_values, k=m)
        selected_population = [population[i] for i in selected_indices]
        return selected_population

    def fittest(self, population, f_thres=None):

        if f_thres is None:
            return max(population, key=self.fitness_fn)
        else:
            eligible_chromosomes = [chrom for chrom in population if self.fitness_fn(chrom) <= f_thres]
            if eligible_chromosomes:
                return max(eligible_chromosomes, key=self.fitness_fn)
            else:
                return None





################################################################
# 4. Traveling Salesman Problem
################################################################

class HamiltonProblem(GeneticProblem):
    def __init__(self, n, g_bases, g_len, m_prob, graph=None):
        super().__init__(n, g_bases, g_len, m_prob)
        self.graph = graph


    def init_population(self):

        population = []
        vertices = self.graph.vertices()
        for _ in range(self.n):
            chromosome = random.sample(vertices, len(vertices))
            population.append(tuple(chromosome))
        return population


    def next_generation(self, population):

        new_population = []
        for _ in range(self.n):
            parent1 = self.select(1, population)[0]
            parent2 = self.select(1, population)[0]
            child = self.crossover(parent1, parent2)
            child = self.mutate(child)
            new_population.append(child)


        combined_population = population + new_population


        next_gen_population = self.select(self.n, combined_population)

        return next_gen_population

    def mutate(self, chrom):

        mutated_chrom = list(chrom)
        if random.random() < self.m_prob:

            i, j = random.sample(range(self.g_len), 2)
            mutated_chrom[i], mutated_chrom[j] = mutated_chrom[j], mutated_chrom[i]
        return tuple(mutated_chrom)


    def crossover(self, chrom1, chrom2):

        offspring = [None] * self.g_len

        i = random.randint(0, self.g_len - 1)


        while True:

            offspring[i] = chrom1[i]
            i = chrom2.index(chrom1[i])

            if offspring[i] is not None:
                break

        for j in range(self.g_len):
            if offspring[j] is None:
                offspring[j] = chrom2[j]

        return tuple(offspring)


    def fitness_fn(self, chrom):

        fitness_value = 0
        for i in range(self.g_len - 1):
            fitness_value += self.graph.get(chrom[i], chrom[i+1])

        fitness_value += self.graph.get(chrom[-1], chrom[0])
        return fitness_value


    def select(self, m, population):

        selected = random.choices(population, weights=[1/self.fitness_fn(chrom) for chrom in population], k=m)
        return selected


    def fittest(self, population, f_thres=None):

        best_chrom = min(population, key=self.fitness_fn)
        if f_thres is None or self.fitness_fn(best_chrom) < f_thres:
            return best_chrom
        else:
            return None
