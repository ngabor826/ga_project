import numpy as np
import random
import networkx as nx
import copy
from datetime import datetime

ga_log = open("ga_log.txt", "a")


GRID_SIZE = 9
SQ_GRID = int(GRID_SIZE ** 0.5)

s_board = []

with open("test.txt", "r") as s_file:
    lines = s_file.readlines()
    s_board += [int(x) for line in lines for x in line.split()]


def init_board():
    sudoku = nx.Graph()
    sudoku.add_nodes_from([
        (i, {"color": 0, "fixed": False}) for i in range(81)
    ])
    neighbours = []

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            row_neighbours = [(i * GRID_SIZE + j, i * GRID_SIZE + x) for x in range(GRID_SIZE) if x != j]
            col_neighbours = [(i * GRID_SIZE + j, x * GRID_SIZE + j) for x in range(GRID_SIZE) if x != i]

            sqr_i = (i // SQ_GRID) * SQ_GRID
            sqr_j = (j // SQ_GRID) * SQ_GRID
            sqr_neighbours = [(i * GRID_SIZE + j, a * GRID_SIZE + b) for a in range(sqr_i, sqr_i + SQ_GRID) for b in
                              range(sqr_j, sqr_j + SQ_GRID) \
                              if (a != i or b != j)]

            unfiltered_neigh = row_neighbours + col_neighbours + sqr_neighbours
            filtered_neigh = list(set(unfiltered_neigh))

            neighbours = neighbours + filtered_neigh

    hyper_index = []
    indexes = [10, 14, 46, 50]
    for i in indexes:
        numbers = list(range(81))
        item = numbers[i::9]
        hyper_index.append(item[:3])

    for x in hyper_index:
        for i in x:
            for j in range(3):
                if (i != j):
                    hyper_neighbours = [(i + j, a + b) for a in x \
                                        for b in range(3) \
                                        if (a != i or b != j)]

                neighbours = neighbours + hyper_neighbours

    joint_neigh = list(set(neighbours))
    sudoku.add_edges_from(joint_neigh)

    return sudoku


# convert a given list "board" to networkx board
def board_to_nx(sudoku, board):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            idx = i * GRID_SIZE + j

            if board[idx] != 0:
                # 'fixed' means that the color of that node cannot be changed (during mutation or crossover)
                sudoku.nodes[idx]['fixed'] = True
                sudoku.nodes[idx]['color'] = board[idx]
    return sudoku


# utility function to display a sudoku board
def print_board(board):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            print(board.nodes[i * GRID_SIZE + j]['color'], end=' ')
        print()


def create_population(n, base_board, max_color):
    copies = [copy.deepcopy(base_board) for _ in range(n)]

    for graph in copies:
        graph.graph['fitness'] = None

        for i in range(max_color):

            row_colors = [graph.nodes[i * max_color + j]['color'] for j in range(max_color)]
            possible_colors = [(k + 1) for k in range(max_color) if not (k + 1) in row_colors]

            for j in range(max_color):
                if graph.nodes[i * max_color + j]['fixed'] == False:
                    color = random.choice(possible_colors)
                    graph.nodes[i * max_color + j]['color'] = color
                    possible_colors.remove(color)

    return copies


def fitness(population):
    for individual in population:
        if individual.graph['fitness'] != None:
            continue

        fitness = 0
        for edge in individual.edges:
            if individual.nodes[edge[0]]['color'] == individual.nodes[edge[1]]['color']:
                fitness -= 1

        individual.graph['fitness'] = fitness

    return population


def swap_mutation(population, pm, max_color):
    for instance in population:
        mut_hap = False

        for i in range(max_color):
            for j in range(max_color):
                node = i * max_color + j
                rn_node = random.randint(i * max_color, (i + 1) * max_color - 1)

                if instance.nodes[node]['fixed'] or instance.nodes[rn_node]['fixed']:
                    continue
                else:
                    if random.random() <= pm:
                        instance.nodes[node]['color'], instance.nodes[rn_node]['color'] = instance.nodes[rn_node][
                                                                                              'color'], \
                                                                                          instance.nodes[node]['color']
                        mut_hap = True
        if mut_hap:
            instance.graph['fitness'] = None

    return population


def tournament_selection(population, k, possible):
    best = random.choice(possible)

    for i in range(k):
        rnd_idx = random.choice(possible)
        if population[rnd_idx].graph['fitness'] >= population[best].graph['fitness']:
            best = rnd_idx

    return best


"""
    Uniform crossover when a row on the table is a permutation
    Specific to the sudoku problem.
"""


def crossover(p1, p2, pc):
    o1, o2 = copy.deepcopy(p1), copy.deepcopy(p2)

    if random.random() > pc:
        return o1, o2

    size = int(len(o1.nodes) ** 0.5)
    for i in range(size):
        if i % 2:
            for j in range(size):
                node = i * size + j
                o1.nodes[node]['color'], o2.nodes[node]['color'] = o2.nodes[node]['color'], o1.nodes[node]['color']

    o1.graph['fitness'] = None
    o2.graph['fitness'] = None

    return o1, o2


# choose N best individuals from population
def elitism_selection(population, N):
    new_pop = []

    while len(new_pop) != N:
        best = population[0]

        for individual in population:
            if individual.graph['fitness'] > best.graph['fitness']:
                best = individual

        new_pop.append(best)
        population.remove(best)

    return new_pop


# check if any of the individuals is a complete solution
def solution(population):
    for ind in population:
        if ind.graph['fitness'] == 0:
            return True
    return False


# find the best individual of a population
def find_best(population):
    best = population[0]

    for ind in population:
        if ind.graph['fitness'] > best.graph['fitness']:
            best = ind

    return best


def genetic_algorithm(sudoku,
                      create_fn, fitness_fn, selection_fn, solution_fn,
                      crossover_fn, mutation_fn, survivor_fn, best_fn,
                      # optional params
                      grid_size=9, pop_size=11, p_m=0.03, p_c=0.9,
                      mating_pool=2, s_pres=7, max_gen=500_000):
    GRID_SIZE = grid_size

    # initialize GA parameters
    POP_SIZE = pop_size
    P_MUTATION = p_m
    P_CROSSOVER = p_c
    N_MATING_POOL = mating_pool
    # selection pressure for tournament selection
    S_PRESSURE = s_pres
    MAX_GENER = max_gen

    generation = 0

    # init population
    population = create_fn(POP_SIZE, sudoku, GRID_SIZE)
    population = fitness_fn(population)

    while not solution_fn(population):

        # select parents
        possible_parents = [i for i in range(POP_SIZE)]
        parents = []

        for i in range(N_MATING_POOL):
            p1 = selection_fn(population, S_PRESSURE, possible_parents)
            possible_parents.remove(p1)
            p2 = selection_fn(population, S_PRESSURE, possible_parents)

            possible_parents.remove(p2)

            parents.append((p1, p2))

        # crossover
        for (p1, p2) in parents:
            o1, o2 = crossover_fn(population[p1], population[p2], P_CROSSOVER)
            # add new offspring to population
            population += [o1, o2]

        # mutation
        population = mutation_fn(population, P_MUTATION, GRID_SIZE)

        # evaluate fitness
        population = fitness_fn(population)

        # select survivors
        population = survivor_fn(population, POP_SIZE)

        # print best score
        if generation % 100 == 0:
            best = best_fn(population)
            ga_log.write("\n Generation {}. best score: {}".format(generation, best.graph['fitness']))

        generation += 1

        if generation == MAX_GENER:
            break

    return find_best(population), generation

def close_ga_log():
    ga_log.close()