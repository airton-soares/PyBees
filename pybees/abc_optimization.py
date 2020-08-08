from numpy.random import choice
from models.explorer_bee import ExplorerBee

import random


def optimize(function, colony, limit, radius, comparison_type, max_num_iterations):
    best_position = None
    iteration = 0

    __alocate_worker_bees(colony.worker_bees, colony.explorer_bees, radius, function)

    while iteration < max_num_iterations:
        iteration += 1
        deallocated_worker_bees = []
        best_position_iter = None

        for i in range(len(colony.explorer_bees)):
            explorer_bee = colony.explorer_bees[i]
            best_position_food_source = None

            if len(explorer_bee.worker_bees) == 0:
                colony.explorer_bees[i] = ExplorerBee(len(explorer_bee.position), function.lower_limit,
                                                      function.upper_limit)
            else:
                for worker_bee in explorer_bee.worker_bees:
                    __move_worker_bee(worker_bee, explorer_bee, colony.explorer_bees + colony.worker_bees,
                                      function.lower_limit, function.upper_limit, function, comparison_type)

                    if best_position_food_source is None or function.compare_fitness(worker_bee.position,
                                                                                     best_position_food_source):
                        best_position_food_source = worker_bee.position.copy()

                    if best_position_iter is None or function.compare_fitness(best_position_food_source, best_position_iter):
                        best_position_iter = best_position_food_source.copy()

                if best_position_food_source is not None and function.compare_fitness(best_position_food_source,
                                                                                      explorer_bee.position):
                    explorer_bee.position = best_position_food_source.copy()
                    explorer_bee.no_improvement_cycles_qtd = 0
                else:
                    explorer_bee.no_improvement_cycles_qtd += 1

                if explorer_bee.no_improvement_cycles_qtd == limit or len(explorer_bee.worker_bees) == 0:
                    if len(explorer_bee.worker_bees) > 0:
                        deallocated_worker_bees += explorer_bee.worker_bees

                    colony.explorer_bees[i] = ExplorerBee(len(explorer_bee.position), function.lower_limit, function.upper_limit)

        if best_position is None or (best_position_iter is not None and function.compare_fitness(best_position_iter,
                                                                                                 best_position)):
            best_position = best_position_iter.copy()

        __alocate_worker_bees(deallocated_worker_bees, colony.explorer_bees, radius, function)

    return function.cost(best_position)


def __alocate_worker_bees(worker_bees, explorer_bees, radius, function):
    fitness_sum = sum([function.fitness(explorer_bee.position) for explorer_bee in explorer_bees])
    probability_distribution = [function.fitness(explorer_bee.position) / fitness_sum for explorer_bee in explorer_bees]

    for worker_bee in worker_bees:
        explorer_bee = choice(explorer_bees, 1, p=probability_distribution)[0]
        worker_bee.position = [coord + random.uniform(-radius, radius) for coord in explorer_bee.position]
        explorer_bee.worker_bees.append(worker_bee)


def __move_worker_bee(worker_bee, explorer_bee, all_bees, lower_limit, upper_limit, function, comparison_type):
    new_position = []

    if comparison_type == 1:
        candidate_bees = all_bees.copy()
    else:
        candidate_bees = [explorer_bee] + explorer_bee.worker_bees.copy()

    candidate_bees.remove(worker_bee)

    if comparison_type == 3:
        fitness_sum = sum([function.fitness(bee.position) for bee in candidate_bees])
        probability_distribution = [function.fitness(bee.position) / fitness_sum for bee in candidate_bees]
        candidate_bee = choice(candidate_bees, 1, p=probability_distribution)[0]
    else:
        candidate_bee = random.choice(candidate_bees)

    for i in range(len(worker_bee.position)):
        new_coord = worker_bee.position[i] + random.uniform(-1, 1) * (
                    worker_bee.position[i] - candidate_bee.position[i])

        if new_coord < lower_limit:
            new_coord = random.uniform(0.6, 0.9) * lower_limit
        elif new_coord > upper_limit:
            new_coord = random.uniform(0.6, 0.9) * upper_limit

        new_position.append(new_coord)

    if function.fitness(new_position) > function.fitness(worker_bee.position):
        worker_bee.position = new_position
