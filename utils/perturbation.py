"""
Perturbation operators
"""
import random
import copy
import numpy as np

from utils.population import Individual

class Mutator:
    def __init__(self, perturbation, probabilty : float) -> None:
        self.perturbation_function = perturbation
        self.probability = probabilty
        self.before_mutation = None
        self.after_mutation = None
    
    def mutate_single(self, genome):
        self.before_mutation = genome
        self.after_mutation = self.perturbation_function(data = genome, probability = self.probability)
        return self.after_mutation
    
    def mutate_population(self, population):
        self.before_mutation = population
        self.after_mutation = []
        for individual in population:
            self.after_mutation.append(self.perturbation_function(data = individual, probability = self.probability))
        return self.after_mutation
    
    def __repr__(self) -> str:
        return "{}, mutation rate: {}".format(self.perturbation_function.__name__, self.probability)
    
def tsp_swap(data : list, probability : float = 0.0, **kwargs):
    mutated = data[:]
    for swapped in range(len(mutated)):
        if random.random() < probability:
            swap_with = random.randint(0, len(mutated) -1)
            
            city1 = mutated[swapped]
            city2 = mutated[swap_with]
            
            mutated[swapped] = city2
            mutated[swap_with] = city1
    return mutated
    
def bitflip_multiple(data : "list[int]" = [], probability : float = 0.0, **kwargs):
    """
    Decides independently for each bit, whether it will be inverted or not.
    returns flipped copy
    """
    perturbed = []
    for i in data:
        if random.random() < probability:
            if i==1:
                perturbed.append(0)
            else:
                perturbed.append(1)
        else:
            perturbed.append(copy.deepcopy(i))
    return perturbed

def gaussian(data : "list[float]", deviation = 1, **kwargs):
    """
    Mutates a vector of real numbers by adding vector of normal values
    returns perturbed copy
    """
    perturbed =[]
    for pos, value in enumerate(data):
        normal = random.normalvariate(0.0, deviation)
        perturbed.append(value + normal)
    return perturbed

def cauchy(data : "list[float]", **kwargs):
    """
    Mutates a vector of real numbers by adding vector of values
    from Cauchy distribution, returns perturbed copy
    """
    perturbed = []
    cauch = np.random.default_rng().standard_cauchy(len(data))
    for pos, value in enumerate(data):
        perturbed.append(value + cauch[pos])
    return perturbed

def bitflip_single(data : "list[int]", **kwargs):
    """
    For each bit decide randomly whether it should be mutated or not
    """
    perturbed = []
    rnd_num = random.randrange(0,len(data))
    perturbed = copy.deepcopy(data)
    perturbed[rnd_num] = 1 if perturbed[rnd_num] == 0 else 0
    return perturbed


if __name__ == "__main__":
    print(cauchy([1,0,1,1,1,1,1]))
