import random
import copy

def binary(data : list, probability):
    perturbed = []
    for i in data:
        if random.random() <= probability:
            perturbed.append(0 if 1 else 1)
        else:
            perturbed.append(copy.deepcopy(i))

    return perturbed

