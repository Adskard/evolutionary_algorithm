"""
Perturbation operators
"""
import random
import copy

def bitflip_multiple(data : "list[int]", probability : float):
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

def gaussian(data, deviation):
    """
    Mutates a vector of real numbers by adding vector of normal values
    returns perturbed copy
    """
    perturbed =[]
    for pos, value in enumerate(data):
        normal = random.normalvariate(0.0, deviation)
        perturbed.append(value + normal)
    return perturbed

def bitflip_single(data : "list[int]", probability : float):
    """
    For each bit decide randomly whether it should be mutated or not
    """
    perturbed = []
    rnd_num = random.randrange(0,len(data))
    perturbed = copy.deepcopy(data)
    perturbed[rnd_num] = 1 if perturbed[rnd_num] == 0 else 0
    return perturbed


if __name__ == "__main__":
    print(bitflip_multiple([1,0,1,1,1,1,1], 1.0))