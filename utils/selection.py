
import random

from .population import Individual
class Selector:
    """
    wrapper
    """
    def __init__(self, function, selection_count = 0, tourn_size = 0 ) -> "Selector":
        self.function = function
        self.selection_count = selection_count
        self.pool = []
        self.selected = []
        self.tourn_size = tourn_size

    def __call__(self, population : "list[Individual]") -> "list[Individual]":
        self.pool = population
        self.selected = self.function(population, count = self.selection_count, tourn_size = self.tourn_size)
        return self.selected
    
    def __repr__(self) -> str:
        return "{}, selection size: {}, tournament size: {}".format(self.function.__name__, self.selection_count, self.tourn_size)

def tournament():
    pass

def randomSelect(population : "list[Individual]", count : int):
    """
    Random selection implementation

    Args:
        population (_type_): _description_
        next_gen_count (_type_): _description_

    Returns:
        _type_: _description_
    """
    return [random.choice(population) for i in range(count)]

def proportionate(evaluated_pop : "list[Individual]", count : int) -> list:
    """
    Proportionate selection of individuals

    Args:
        evaluated_pop (list[Individual]): _description_
        count (int): _description_

    Returns:
        _type_: _description_
    """
    chosen = []
    sorted_pop = sorted(evaluated_pop, key=lambda individual: individual.fitness)
    sum_fits = sum([i.fitness for i in evaluated_pop])
    print("Pop: ")
    for i in sorted_pop:
        print(i)
    for i in range(count):
        rnd = random.random() * sum_fits
        sum_ind = 0
        for individual in sorted_pop:
            sum_ind += individual.fitness
            if sum_ind > rnd:
                chosen.append(individual.value)
                break
    print("chosen: ")
    for i in chosen:
        print(i)
    return chosen
    
def tournament(evaluated_pop : "list[Individual]", count : int, tourn_size : int) -> list:
    chosen = []
    for i in range(count):
        aspirants = [random.choice(evaluated_pop) for i in range(tourn_size)]
        chosen.append(min(aspirants, key= lambda x : x.fitness).value)
    return chosen
if __name__ == "__main__":
    print(proportionate([Individual(2,4),Individual(1,1),Individual(1,2)], 2))