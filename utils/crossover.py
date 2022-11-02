"""
Module for crossover operatinos
"""
import random

class Crossover:
    def __init__(self, crossover) -> "Crossover":
        self.crossover_operator = crossover
        self.parents = []
        
        
    def __call__(self, parent1, parent2):
        return self.crossover_operator(parent1, parent2)
    
    def __repr__(self) -> str:
        return "{}".format(self.crossover_operator.__name__)
    

def single_point(p1,p2):
    """
    creates two children
    :param p1: parent 1
    """
    size = min(len(p1), len(p2))
    point = random.randint(0,size - 1)

    ch1 = list(p1[:point])
    ch1.extend(p2[point:])

    ch2 = list(p2[:point])
    ch2.extend(p1[point:])
    return ch1, ch2

def tsp_breed(p1, p2):
    point1 = random.randint(0, len(p1))
    point2 = random.randint(point1, len(p1))
    
    child1 = []
    for i in range(point1, point2):
        child1.append(p1[i])
    child2 = [item for item in p2 if item not in child1]
    
    return child1 + child2

def uniform(parents):
    pass

if __name__ == "__main__":
    print(single_point([1,1,1,1,1,1,1],[0,0,0,0,0,0,0,0]))