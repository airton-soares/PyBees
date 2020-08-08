from models.explorer_bee import ExplorerBee
from models.worker_bee import WorkerBee


class Colony:
    def __init__(self, size, dimension, lower_limit, upper_limit):
        explorer_bees_size = int(size / 4)
        worker_bees_size = size - explorer_bees_size
        self.explorer_bees = [ExplorerBee(dimension, lower_limit, upper_limit) for _ in range(explorer_bees_size)]
        self.worker_bees = [WorkerBee() for _ in range(worker_bees_size)]
