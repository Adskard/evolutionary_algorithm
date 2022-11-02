"""
Replacement strategy for EA population control
"""
from multiprocessing import parent_process
import random
from utils.population import Individual

class Replacer:
    """
    Wrapper class for replacement strategy.
    """
    def __init__(self, strategy, crossover_operator = None, elite_count = 0, **kwargs) -> "Replacer":
        self.strategy = strategy
        self.crossover_operator = crossover_operator
        self.elite_count = elite_count
        self.new_population = []
    
    def replace(self, parents : "list[Individual]"):
        self.parents = parents
        self.new_population = self.strategy(self.parents, self.elite_count, self.crossover_operator)
        return self.new_population 

    def __repr__(self) -> str:
        return "{}, crossover: {}, elite count: {}".format(self.strategy.__name__, self.crossover_operator, self.elite_count)

def general_replacement(parents : "list[Individual]", crossover, **kwargs):
    """

    Args:
        old (Tuple[individuals, fitnessValue]): Valued members of old generation
        new (Tuple[individuals, fitnessValue]): Valued members of new generation
    """
    pass

def elite(parents : list, elite_count : int, crossover_operator, **kwargs):
    """
    Elite replacement strategy. Preserves the best individuals from
    previous generation.

    Args:
        parents (_type_): _description_
        elite_count (_type_): _description_
        crossover (_type_): _description_

    Returns:
        _type_: _description_
    """
    children = []
    length = len(parents) - elite_count
    pool = random.sample(parents, len(parents))

    for i in range(0, min(len(parents), elite_count)):
        children.append(parents[i])
    
    for i in range(0, length):
        child = crossover_operator(pool[i], pool[len(parents)-i-1])
        children.append(child)
    return children
    

def random_replacement(old_pop : "list[Individual]", new_pop : "list[Individual]", **kwargs):
    #TODO
    """ 
    Args:
        old (_type_): _description_
        new (_type_): _description_

    Returns:
        _type_: _description_
    """
    return [random.choice(old_pop[0].extend(new_pop[0])) for i in range(len(old_pop[0]))]
    
if __name__ == "__main__":
    pass