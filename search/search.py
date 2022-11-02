"""
Search function implementations
"""

from copy import deepcopy
from time import time
from utils import fitness
from utils import replacement
from utils.condition import *
from utils import perturbation
from utils import crossover
from utils.population import Individual
from utils.replacement import Replacer, elite


class SearchResult:
    def __init__(self, steps, solutions, fitnesses, generations, time_stamps):
        self.steps = steps
        self.solutions = solutions
        self.fitnesses = fitnesses
        self.time_stamps = time_stamps
        self.generations = generations
        self.name = ""

class SearchEngine:
    """
    Search function wrapper
    """

    def __init__(self, fitness_function : fitness.FitnessFunction, mutation,
                 condition : TerminalCondition,
                replacer: Replacer = None , selection = None, **kwargs):
        self.fitness_function = fitness_function
        self.mutation = mutation
        self.condition = condition
        self.selection = selection
        self.replacer = replacer
        
        self.steps = []
        self.solutions = []
        self.fitnesses = []
        self.time_stamps = [0]
        
    def next_generation(self, population : "list[Individual]"): 
        selected_parents = self.selection(population)
        next_generation = self.replacer.replace(selected_parents)
        perturbed_generation = self.mutation.mutate_population(next_generation)
        return [Individual(i, self.fitness_function(i)) for i in perturbed_generation]

    def simple_ea(self, initial_population : list):
        """
        Simple evolutionary algorithm

        Args:
            condition (TerminalCondition): _description_
            initial_solution (_type_): _description_
        """
        print("================Starting EA search================")
        print("Population: " + str(len(initial_population)))
        print("Fitness function: " + str(self.fitness_function))
        print("Selection: " + str(self.selection))
        print("Replacement: " + str(self.replacer))
        print("Mutation: " + str(self.mutation))
        print("Termination condition: " + str(self.condition))
        population = [Individual(i, self.fitness_function(i)) for i in initial_population]
        sorted(population, key= lambda x: x.fitness)
        
        best = population[0]
        self.solutions.append(best.value)
        self.fitnesses.append(best.fitness)
        curr_best = best

        while self.condition.test(result = best.value):
            population = self.next_generation(population)
            sorted(population, key= lambda x: x.fitness)
            curr_best = population[0]
            if(curr_best.fitness < best.fitness):
                best = curr_best
                self.solutions.append(best.value)
                self.fitnesses.append(best.fitness)
                self.time_stamps.append(self.fitness_function.calls_made // len(initial_population))
        print("Cycle " + str(self.condition.calls) +" best: " + str(best))
        return best

    def local(self, initial_solution):
        """
        Commences local (1+1)ES search
        """
        self.solutions.append(initial_solution)
        current_solution = self.solutions[-1]

        self.fitness_function(current_solution)
        self.fitnesses.append(self.fitness_function.last_fitness)
        current_fitness = self.fitness_function.last_fitness

        self.steps.append((current_solution, current_fitness))

        while self.condition.test(result = current_solution):
            next_step = self.mutation.mutate_single(current_solution)
            next_fitness = self.fitness_function(next_step)
            self.steps.append((next_step, next_fitness))

            if current_fitness > next_fitness:
                self.solutions.append(next_step)
                self.fitnesses.append(next_fitness)
                self.time_stamps.append(self.fitness_function.calls_made - 1)

                current_solution = next_step
                current_fitness = next_fitness
        return current_solution

    def local_one_fifth(self, initial_solution, initial_sigma):
        """
        Commences local (1+lambda)ES search with improving one fifth rule
        """
        sigma = initial_sigma
        sigmas = [sigma]
        self.mutation = lambda x : perturbation.gaussian(x, deviation = sigma)
        
        self.solutions.append(initial_solution)
        current_solution = self.solutions[-1]

        self.fitness_function(current_solution)
        self.fitnesses.append(self.fitness_function.last_fitness)
        current_fitness = self.fitness_function.last_fitness

        self.steps.append((current_solution, current_fitness))

        while self.condition.test(result = current_solution):
            next_step = self.mutation(current_solution)
            next_fitness = self.fitness_function(next_step)
            self.steps.append((next_step, next_fitness))

            if current_fitness > next_fitness:
                self.solutions.append(next_step)
                self.fitnesses.append(next_fitness)
                self.time_stamps.append(self.fitness_function.calls_made - 1)

                current_solution = next_step
                current_fitness = next_fitness
                sigma = sigma * 1.5
                sigmas.append(sigma)
            else:
                sigma = 1.5**(-1/4)*sigma
                sigmas.append(sigma)
        return current_solution,sigmas
    
    def clear(self):
        """
        Clears all variables, reset to base state, for another run
        """
        self.fitness_function.clear()
        self.condition.clear()
        self.steps = []
        self.solutions = []
        self.fitnesses = []
        self.time_stamps = [0]
        
    def snapshot(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        result = SearchResult(self.steps, self.solutions, self.fitnesses, self.condition.calls, self.time_stamps)
        self.clear()
        return result


