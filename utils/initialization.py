import random


def populate_array(size : int, init_function):
    """_summary_

    Args:
        size (int): _description_
        initFucntion (_type_): _description_

    Returns:
        _type_: _description_
    """
    return [init_function()]*size

def tsp_route(cities):
    return random.sample(cities, len(cities))

def chromosome(length : int):
    return [random.randint(0,1) for i in range(length)]

def populate_matrix():
    """_summary_
    """
    return 

def populate(init_population, **kwargs):
    return init_population(**kwargs)
    

if __name__ == "__main__":
    pass