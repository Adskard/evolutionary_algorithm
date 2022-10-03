"""
Search function implementations
"""
import matplotlib
import matplotlib.pyplot as plt
from utils.condition import LoopCondition, NoImporvementCondition, ResultMatchCondition, TerminalCondition
from utils import fitness
from utils import perturbation
from utils import mapping

from utils.condition import LoopCondition, NoImporvementCondition, ResultMatchCondition, TerminalCondition

class LocalSearchEngine:
    """
    Search function wrapper
    """

    def __init__(self, fitness_function : fitness.FitnessFunction, mutation):
        self.fitness_function = fitness_function
        self.mutation = mutation
        self.solutions = []
        self.fitnesses = []
        self.time_stamps = [0]


    def run(self, condition : TerminalCondition, initial_solution):
        """
        Commences the search
        """
        self.solutions.append(initial_solution)
        current_solution = self.solutions[-1]

        self.fitnesses.append(self.fitness_function.evaluate(data = current_solution))
        current_fitness = self.fitnesses[-1]
        probability = 0.5

        while condition.test(result = current_solution):
            next_step = self.mutation(current_solution, probability)
            next_fitness = self.fitness_function.evaluate(data = next_step)

            if current_fitness < next_fitness:
                self.solutions.append(next_step)
                self.fitnesses.append(next_fitness)
                self.time_stamps.append(self.fitness_function.calls_made)

                current_solution = next_step
                current_fitness = next_fitness
        return current_solution
    
    def display_statistics_plot(self):
        print(self.fitnesses)
        print(self.time_stamps)

        matplotlib.use("TkAgg")
        plt.plot(self.time_stamps, self.fitnesses, 'x--')
        plt.title("Search")
        plt.ylabel('Fitness values')
        plt.xlabel("Function calls")

        for i,j,k in zip(self.time_stamps,self.fitnesses, self.solutions):
            plt.text(i,j,k)

        plt.show()
        

if __name__ == "__main__":
    search = LocalSearchEngine(fitness.FitnessFunction(fitness.one_max),
        perturbation.bitflip_single)
    print("Final solution: ", search.run(NoImporvementCondition(10), [0]*50))
    print("Calls made: ", search.fitness_function.calls_made)
    search.display_statistics_plot()
    #
    #search2 = LocalSearchEngine(fitness.FitnessFunction(fitness.one_max),
    #    perturbation.bitflip_multiple)
    #print("Final solution: ", search2.run(ResultMatchCondition([1,1,1,1,1,1]), [0,0,0,0,0,0]))
    #print("Calls made: ", search2.fitness_function.calls_made)

    search3 = LocalSearchEngine(fitness.FitnessFunction(fitness.rastrigin),
        perturbation.bitflip_single)
    print("Final solution: ", search3.run(NoImporvementCondition(10), [0,1,0,1,0,0]))
    print("Calls made: ", search3.fitness_function.calls_made)
    search3.display_statistics_plot()