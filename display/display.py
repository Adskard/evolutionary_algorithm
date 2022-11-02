"""
For displaying search results
"""

from math import floor
import matplotlib
import matplotlib.pyplot as plt

from search.search import SearchEngine, SearchResult

class Visual:
    """
    Displays search results using matplotlib
    """
    def __init__(self) -> "Visual":
        self.display_backend = "TkAgg"
        matplotlib.use(self.display_backend)

    def plot_fitness(self, search : SearchEngine):
        """
        Displays statistics of last run
        """

        #appends last plot point for better x axis
        points = (search.time_stamps + [search.fitness_function.calls_made],
        search.fitnesses + [search.fitnesses[-1]])

        plt.plot(points[0], points[1]
            , "-")
        plt.title("Impovements")
        plt.ylabel('Fitness values')
        plt.xlabel("Function calls")

        plt.text(points[0][0],points[1][0],floor(points[0][1]))
        for i,j in zip(points[0][-1:], points[1][-1:]):
            plt.text(i,j,floor(j))
        plt.show()

    def scatter_steps(self, search : SearchEngine):
        """
        Displays all steps taken during the search
        """
        plt.ylabel('Fitness values')
        plt.xlabel("Function calls")
        plt.title("All steps")

        points = (search.time_stamps + [search.fitness_function.calls_made],
        search.fitnesses + [search.fitnesses[-1]])

        plt.scatter(range(len(search.steps)), [i[1] for i in search.steps], s = 2, color = "#FF0000")
        plt.plot(points[0], points[1]
            , "-")
        plt.plot(points[0][-2], points[1][-2], "go")
        plt.text(points[0][-2], points[1][-2], "optimum", horizontalalignment='left',
        verticalalignment='bottom', snap=False)
        plt.show()

    def comparison(self, searches : SearchResult):
        """
        Displays comparison between different searches
        """

        for pos, value in enumerate(searches):
            points = (value.time_stamps + [value.generations],
                value.fitnesses + [value.fitnesses[-1]])
            plt.plot(points[0], points[1]
            , "-", label=value.name)
            plt.legend(loc = "best")
            plt.xlabel("Generations")
            plt.ylabel("Fitness value")
        plt.show()
