from functions.function import Function

import math


class Rastrigin(Function):
    def __init__(self):
        self.lower_limit = -5.12
        self.upper_limit = 5.12

    def cost(self, position):
        return sum([(coord ** 2) - 10 * math.cos(2 * math.pi * coord) + 10 for coord in position])

    def fitness(self, position):
        cost = self.cost(position)
        return 1 / (1 + abs(cost))

    def compare_fitness(self, position_1, position_2):
        return self.fitness(position_1) > self.fitness(position_2)
