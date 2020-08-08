import random


class ExplorerBee:
    def __init__(self, dimension, lower_limit, upper_limit):
        self.position = [lower_limit + random.uniform(0, 1) * (upper_limit - lower_limit) for _ in range(dimension)]
        self.worker_bees = []
        self.no_improvement_cycles_qtd = 0
