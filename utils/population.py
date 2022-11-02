"""
Evolution population implementations
"""
import math

class Individual:
    def __init__(self, value, fitness) -> "Individual":
        self.value = value
        self.fitness = fitness

    def __repr__(self) -> str:
        return "Individual: "+ str(self.value) + " - " + "{:.2f}".format(self.fitness)

class EdgeMatrix:
    """
    Wrapper class for edge weight matrix for tsp problems
    """
    def __init__(self, matrix) -> "EdgeMatrix":
        self.matrix = matrix

    def distance(self, start, finish):
        """
        returns distance betwee the two cities from the edge matrix

        Args:
            start (city_index): index of starting city
            finish (city_index): index of destination city

        Returns:
            float: distance of the two cities
        """
        return self.matrix[start][finish]


class City:
    """
    Individual city repsresentation for tsp problems
    """
    def __init__(self, name, x, y) -> "City":
        self.name = name
        self.x = float(x)
        self.y = float(y)
        
    def __repr__(self) -> str:
        return str(self.name)

    def distance(self, city):
        """
        Compute distance between cities a eucladian space
        using pythogorean theorem

        Args:
            city (City): destination city

        Returns:
            float: distance to a given city
        """
        x_dis = abs(self.x - city.x)
        y_dis = abs(self.y - city.y)
        distance = math.sqrt((x_dis ** 2) + (y_dis ** 2))
        return distance
