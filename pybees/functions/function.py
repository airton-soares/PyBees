from abc import ABC, abstractmethod


class Function(ABC):
    @abstractmethod
    def cost(self, position):
        pass

    @abstractmethod
    def fitness(self, position):
        pass

    @abstractmethod
    def compare_fitness(self, position_1, position_2):
        pass
