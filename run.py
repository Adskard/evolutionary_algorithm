"""
    Example search runs
"""
import random
from typing import MutableMapping
from display.display import Visual
from utils import crossover, fitness, initialization, replacement
from utils import perturbation
from utils import mapping
from utils import selection
from utils.condition import *
from search.search import SearchEngine
from utils.population import City


def sanity_check_search():
    """
    Looking for sanity!
    """
    init_solution = [1] * 8
    expected_result = [0] * 8
    search = SearchEngine(fitness.FitnessFunction(fitness.one_max),
        perturbation.bitflip_single, ResultMatchCondition(expected_result))
    search.local(init_solution)

    display = Visual()
    display.plot_fitness(search = search)

def some_mapping_search():
    """
    Example search with binary to interval mapping
    """
    init_solution = [1,1,1,1]

    func = fitness.FitnessFunction(fitness.rosenbrock,
            mapping = lambda x : mapping.binary_to_interval(x,[0,0],[1,1]))

    search = SearchEngine(func,perturbation.bitflip_single, NoImporvementCondition(10))
    print("Best: ", search.local( init_solution))
    print([mapping.binary_to_interval(x,[0,0],[1,1]) for x in search.solutions])

    display = Visual()
    display.plot_fitness(search = search)

def some_real_search():
    """
    Example search with real objective function
    """
    init_solution = [1]*6
    func = fitness.FitnessFunction(fitness.sphere, coefficients=[0]*6)
    perturbation = lambda x : perturbation.gaussian(x, deviation = 0.5)

    search = SearchEngine(func, perturbation, LoopCondition(300))
    print(search.local_one_fifth(init_solution, 1*(10**(-9))))

    display = Visual()
    display.plot_fitness(search = search)

def multiple_comp():
    """
    Multiple run comparison
    """
    init_solution = [1] * 32
    func = fitness.FitnessFunction(fitness.rosenbrock,
            mapping = lambda x : mapping.binary_to_interval(x,[0,0,0,0],[12,12,12,12]))
    mutation = perturbation.bitflip_single
    search = SearchEngine(func, mutation, LoopCondition(50))
    
    search.local(init_solution)
    searches = [search.snapshot()]
    for i in range(5):
        search.local(init_solution)
        searches += [search.snapshot()]
        
    display = Visual()
    display.comparison(searches = searches)

def some_simple_ea():
    member_length = 12
    loop_length = 50
    
    init_solution = initialization.populate_array(5, lambda  : initialization.chromosome(member_length))
    func = fitness.FitnessFunction(fitness.one_max)
    mutation = perturbation.bitflip_multiple
    search = SearchEngine(func, mutation=mutation, condition=LoopCondition(loop_length),
                          crossover=crossover.single_point, selection=selection.randomSelect)
    
    search.local([random.randint(0,1) in range(member_length)])
    searches = [search.snapshot()]
    
    search.simple_ea(init_solution)
    searches += [search.snapshot()]
    display = Visual()
    display.comparison(searches = searches)

def run_tsp_comparison(cities):
    loop_length = 100
    mutation_probability = 0.01
    tournament_size = 40
    elite_count = 40
    population_size = 100
    
    init_solution = initialization.populate_array(population_size, lambda :initialization.tsp_route(cities))
    func = fitness.FitnessFunction(fitness.tsp_route_distance)
    mutation = perturbation.Mutator(perturbation.tsp_swap, mutation_probability)
    crossover_operator = crossover.tsp_breed
    replacement_strategy = replacement.Replacer(replacement.elite, crossover_operator=crossover_operator, elite_count = elite_count)
    select = selection.Selector(selection.tournament, population_size, tourn_size = tournament_size)
    
    
    search = SearchEngine(func, mutation=mutation, condition=LoopCondition(loop_length),
                          selection=select, replacer=replacement_strategy)

    searches = []

    search.local(initialization.tsp_route(cities))
    result = search.snapshot()
    result.name = "Local"
    searches += [result]
    
    search.simple_ea(init_solution)
    result = search.snapshot()
    result.name = "EA"
    searches += [result]
    
    select.tourn_size = 60
    search.simple_ea(init_solution)
    result = search.snapshot()
    result.name = "tournament size 60"
    searches += [result]
    
    mutation.probability = 1
    search.simple_ea(init_solution)
    result = search.snapshot()
    result.name = "mutation rate = 1"
    searches += [result]
    
    display = Visual()
    display.comparison(searches = searches)

def read_euc_tsp(file_name):
    path = "./test_data/"
    file = open(path + str(file_name), "r")
    line = file.readline()
    cities = []
    with open(path + str(file_name), "r") as file:
        for line in file:
            line = line.strip()
            if(line[:1].isdigit()):
                line = line.split()
                cities.append(City(line[0], line[1], line[2]))
    file.close()
    return cities

if __name__ == "__main__":
    cities = read_euc_tsp("eil101.tsp")
    run_tsp_comparison(cities)
