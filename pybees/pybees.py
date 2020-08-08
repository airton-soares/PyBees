import os
import abc_optimization
import time
import matplotlib.pyplot as plt

from argparse import ArgumentParser
from functions.function_factory import build_function
from functions.function_type import FunctionType
from models.colony import Colony


def build_args_parser():
    usage = 'python pybees.py -d <dimension>\n       ' \
            'run with --help for arguments descriptions'
    parser = ArgumentParser(description='A Python implementation of the Artificial Bee Colony algorithm', usage=usage)

    parser.add_argument('-c', '--colony', dest='colony_size', type=int, default=100,
                        help='Size of the colony')
    parser.add_argument('--limit', dest='limit', type=int, default=200,
                        help='Limit of iterations without enhancement in a food source')
    parser.add_argument('--radius', dest='radius', type=float, default=0.0,
                        help='Possible radius distance initialization for workers from the explorer')
    parser.add_argument('--comparison_type', dest='comparison_type', type=int, default=1,
                        help='Defines if the comparison type to be used in the movement phase. Could be '
                             '1 (global), 2 (only neighbors) or 3 (only neighbors weighted)')
    parser.add_argument('-i', '--iterations', dest='max_num_iterations', type=int, default=10000,
                        help='Maximum number of iterations in the search')
    parser.add_argument('-d', '--dimension', dest='dimension', type=int, default=30,
                        help='Dimension of the functions input')
    parser.add_argument('--simulations', dest='num_simulations', type=int, default=30,
                        help='Number of simulations to be done for the optimization')

    return parser


def main():
    args_parser = build_args_parser()
    args = args_parser.parse_args()
    results_dir_path = "results"

    if not os.path.exists(results_dir_path):
        os.makedirs(results_dir_path)

    for function_type in [f.value for f in FunctionType]:
        function = build_function(function_type)
        best_fitness_list = []

        for i in range(args.num_simulations):
            start_time = time.time()

            colony = Colony(args.colony_size, args.dimension, function.lower_limit, function.upper_limit)
            best_fitness = abc_optimization.optimize(function, colony, args.limit, args.radius, args.comparison_type,
                                                     args.max_num_iterations)

            elapsed_time = time.time() - start_time

            print(function_type + ", simulação: " + str(i + 1) + ", fitness: " + str(round(best_fitness, 2)) + "(" +
                  str(round(elapsed_time, 2)) + " s)")

            best_fitness_list.append(best_fitness)

        plt.clf()
        plt.boxplot(best_fitness_list)
        plt.title(function_type)
        plt.savefig(os.path.join(results_dir_path, function_type + "_box_plot.png"), bbox_inches='tight')


if __name__ == '__main__':
    main()
