"""
Fitness (Objective) function utilities
"""

from audioop import bias
import math

class FitnessFunction:
    """
    Wrapper object used for storing statistics
    """
    def __init__(self, function,
        bias = None,
        coefficients = None,
        mapping = lambda x : x,
        **kwargs):

        self.last_fitness = None
        self.bias = bias
        self.coefficients = coefficients
        self.calls_made = 0
        self.mapping = mapping
        self.function = function
        
    def clear(self):
        self.last_fitness = None
        self.calls_made = 0
    
    def set_bias(self, bias):
        """
        Sets bias function argument
        """
        self.bias = bias

    def set_coefficients(self, coefficients):
        """
        Sets coefficients function argument
        """
        self.coefficients = coefficients

    def get_number_of_calls(self):
        """
        Returns number of calls made to the fitness function
        """
        return self.calls_made

    def __call__(self, data : list):
        self.calls_made += 1
        self.last_fitness = self.function(data = self.mapping(data), bias = self.bias, coefficients = self.coefficients)
        return self.last_fitness
    
    def __repr__(self):
        return "{}, mapping: {}, calls_made: {}, bias: {}, coefficients: {}".format(self.function.__name__,
            self.mapping.__name__, self.calls_made, self.bias, self.coefficients)

def tsp_route_distance(data : list, **kwargs):
    """
    Returns distance of given city route
    """
    route_distance = 0
    for i in range(len(data)):
        j = (i + 1) % len(data)  
        route_distance += data[i].distance(data[j])
    return route_distance

def one_max(data : list = 0, **kwargs):
    """
    Sanity check fitness function
    """
    return sum(data)

def labs(data : "list[int]", **kwargs):
    """
    LABS (Low-Autocorrelation binary sequence) fitness function
    """
    assert all([(item==0 or item==1) for item in data])

    chromosome = [-1 if x==0 else x for x in data ]
    energy = 0
    chromoseome_length = len(chromosome)

    for k in range(1,chromoseome_length):
        corr = 0
        for i in range(0, chromoseome_length - k):
            corr += chromosome[i] * chromosome[i+ k]
        energy += corr*corr
    return energy

def sphere(data : "list[int | float]", coefficients : "list[float | int]", **kwargs):
    """
    Sphere function, sanity check
    """
    assert len(data)==len(coefficients)

    output = 0
    for i,j in zip(data, coefficients):
        output += (i-j)*(i-j)
    return output

def rosenbrock(data : "list[int | float]", **kwargs):
    """
    Rosenbrock objective function
    """

    output = 0
    for i in range(len(data)-1):
        output+= 100*(data[i+1] - data[i]*data[i])**2 + (1-data[i])*(1-data[i])
    return output

def linear(data : "list[int | float]", bias : "float | int", coefficients : "list[int | float]", **kwargs):
    """
    Linear is a basic, easily solvable function of real arguments
    and serves mostly as a sanity check of your algorithm.
    It tests a different ability that the sphere function:
    the results on linear function shows how your algorithm behaves
    if you initialize it in a wrong way, i.e.,
    when the population does not surround the optimum.
    """
    assert len(data) == len(coefficients)
    result = bias
    for i, value in enumerate(data):
        result += value * coefficients[i]

    return result

def step(data : "list[int | float]", bias : "float | int", coefficients : "list[int | float]", **kwargs):
    """
    Similar to linear no gradient
    """
    assert len(data) == len(coefficients)
    result = bias
    for i, value in enumerate(data):
        result += math.floor(value * coefficients[i])

    return result

def rastrigin(data : "list[int | float]", **kwargs):
    """
    Plato na vajíčka
    """
    result = 10 * len(data)
    for pos, val in enumerate(data):
        result += val**2 - 10*math.cos(2*math.pi*val)
    return result

def griewank(data : "list[int | float]", **kwargs):
    """
    Více optim než rastigin
    """
    result = 0
    product = 1
    for pos, val in enumerate(data):
        product *= math.cos(val / math.sqrt(pos+1))

    for pos, val in enumerate(data):
        result += val**2

    result *= 1/4000
    result += 1
    result -= product
    return result

def schwefel(data : "list[int | float]", **kwargs):
    """
    Zrádná funkce
    """
    result = 0

    for pos, val in enumerate(data):
        result += val * math.sin(math.sqrt(abs(val)))

    return -result

def test_schwefel():
    """
    Test schwefel function
    """
    print("Testing schwefel function")
    assert schwefel([0]) == -0.0
    assert schwefel([1]) == -0.8414709848078965
    assert schwefel([-0.1,-0.2]) == 0.11758932708149258
    assert schwefel([0.1,0.2]) == -0.11758932708149258
    assert schwefel([5,-5,-5]) == 3.93374565773607
    assert schwefel([0.1,1.2,2.3,3.4,4.5,5.6,6.7,7.8,8.9,9.1]) == -23.145593064008178
    assert schwefel([5,5,-5]) == -3.93374565773607
    assert schwefel([5]) == -3.93374565773607

def test_griewank():
    """
    Test griewank function
    """
    print("Testing griewank function")
    assert griewank([0]) == 0.0
    assert griewank([1]) == 0.4599476941318603
    assert griewank([-0.1,-0.2]) == 0.014941804023654082
    assert griewank([0.1,0.2]) == 0.014941804023654082
    assert griewank([5,-5,-5]) == 0.765274977211063
    assert griewank([0.1,1.2,2.3,3.4,4.5,5.6,6.7,7.8,8.9,9.1]) == 1.088546150836955
    assert griewank([0,0,0,0,0,0,0,0,0,0,0]) == 0.0
    assert griewank([5]) == 0.7225878145367739

def test_rastrigin():
    """
    Test rastrigin function
    """
    print("Testing rastrigin function")
    assert rastrigin([0]) == 0.0
    assert rastrigin([1,1,1]) == 3.0
    assert rastrigin([-0.1,-0.2]) == 8.869660112501052
    assert rastrigin([0.1,0.2]) == 8.869660112501052
    assert rastrigin([5,-5,-5]) == 75.0
    assert rastrigin([0.1,1.2,2.3,3.4,4.5,5.6,6.7,7.8,8.9,9.1]) == 439.56983005625045
    assert rastrigin([0,0,0,0,0,0,0,0,0,0,0]) == 0.0
    assert rastrigin([5]) == 25.0

def test_step():
    """
    Run tests for step fitness function
    """
    print("Testing step function")
    assert step([0], 1, [2]) == 1
    assert step([0.1,0.2], 1, [2,3]) == 1
    assert step([-0.1, -0.2], 1, [2,3]) == -1
    assert step([-5,5], 1, [2,3]) == 6
    assert step([5,5], 1, [2,3]) == 26
    assert step([0.1,1.2,2.3,3.4,4.5,5.6,6.7,7.8,8.9,9.1], 1, [2,3,4,5,6,7,8,9,10,11]) == 408
    assert step([1,1], 1, [1,1]) == 3
    assert step([0], 1, [1]) == 1
    assert (step([-0.1,-1.2,-2.3,-3.4,-4.5,-5.6,-6.7,-7.8,-8.9,-9.1], 1, [1,1,1,1,1,1,1,1,1,1])
        == -54)

def test_linear():
    """
    Run tests for linear fitness function
    """
    print("Testing linear function")
    assert linear([0], 1, [2]) == 1
    assert linear([0.1,0.2], 1, [2,3]) == 1.8
    assert linear([-0.1, -0.2], 1, [2,3]) == 0.19999999999999996
    assert linear([-5,5], 1, [2,3]) == 6
    assert linear([5,5], 1, [2,3]) == 26
    assert linear([0.1,1.2,2.3,3.4,4.5,5.6,6.7,7.8,8.9,9.1], 1, [2,3,4,5,6,7,8,9,10,11]) == 410.1
    assert linear([1,1], 1, [1,1]) == 3
    assert linear([0], 1, [1]) == 1
    assert (linear([-0.1,-1.2,-2.3,-3.4,-4.5,-5.6,-6.7,-7.8,-8.9,-9.1], 1, [1,1,1,1,1,1,1,1,1,1])
        == -48.6)

def test_rosenbrock():
    """
    Run tests for rosenbrock fitness function
    """
    print("Testing rosenbrock function")
    assert rosenbrock([0]) == 0
    assert rosenbrock([-5]) == 0
    assert rosenbrock([0,0,0]) == 2
    assert rosenbrock([-5,5,-5]) == 130052
    assert rosenbrock([5,5,5]) == 80032
    assert rosenbrock([-0.1,-1.2,-2.3,-3.4,-4.5,-5.6,-6.7,-7.8,-8.9,-9.1]) == 1790768.58
    assert rosenbrock([1,1,1,1,1,1,1,1,1,1]) == 0
    assert rosenbrock([0.1,1.2,2.3,3.4,4.5,5.6,6.7,7.8,8.9,9.1]) == 986898.1800000002
    assert rosenbrock([0,0,0,0,0,0,0,0,0,0]) == 9

def test_sphere():
    """
    Run tests for sphere fitness function
    """
    print("Testing sphere function")
    assert sphere([0], [1]) == 1
    assert sphere([1], [1]) == 0
    assert sphere([0,0,0], [1,1,1]) == 3
    assert sphere([-5,5,-5], [1,1,1]) == 88
    assert sphere([5,5,5], [1,1,1]) == 48
    assert (sphere([-0.1,-1.2,-2.3,-3.4,-4.5,-5.6,-6.7,-7.8,-8.9,-9.1], [1,1,1,1,1,1,1,1,1,1]) 
            == 446.85999999999996)
    assert sphere([1,1,1,1,1,1,1,1,1,1], [1,1,1,1,1,1,1,1,1,1]) == 0
    assert (sphere([0.1,1.2,2.3,3.4,4.5,5.6,6.7,7.8,8.9,9.1], [1,1,1,1,1,1,1,1,1,1])
             == 248.45999999999998)
    assert sphere([0,0,0,0,0,0,0,0,0,0], [1,1,1,1,1,1,1,1,1,1]) == 10

def test_labs():
    """
    Run tests for labs fitness function
    """
    print("Testing labs function")
    assert labs([0]) == 0
    assert labs([1]) == 0
    assert labs([0,0,0]) == 5
    assert labs([0,0,1]) == 1
    assert labs([1,1,1]) == 5
    assert labs([1,1,0,0,1,1,0,0,1,1]) == 125
    assert labs([1,1,1,1,1,1,1,1,1,1]) == 285
    assert labs([0,1,0,1,0,1,0,1,0,1]) == 285
    assert labs([0,0,0,0,0,1,1,1,1,1]) == 125

def test_one_max():
    """
    Run tests for one_max fitness function
    """
    print("Testing one_max function")
    assert one_max([0]) == 0
    assert one_max([1]) == 1
    assert one_max([0,0,0]) == 0
    assert one_max([0,0,1]) == 1
    assert one_max([1,1,1]) == 3
    assert one_max([1,1,0,0,1,1,0,0,1,1]) == 6
    assert one_max([1,1,1,1,1,1,1,1,1,1]) == 10
    assert one_max([0,1,0,1,0,1,0,1,0,1]) == 5
    assert one_max([0,0,0,0,0,1,1,1,1,1]) == 5

def run_tests():
    """
    Run tests for fitness functions
    """
    print("Running tests...")
    print("================")
    test_one_max()
    test_labs()
    test_sphere()
    test_rosenbrock()
    test_linear()
    test_step()
    test_rastrigin()
    test_griewank()
    test_schwefel()
    print("================")
    print("Tests were succesfull")

if __name__ == "__main__":
    run_tests()
