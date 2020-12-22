from ga_algorithm import *
import time

ga_log.write(str(datetime.now())+": \n")    

def ga_experiment(s_board):

    sudoku = init_board()
    sudoku = board_to_nx(sudoku, s_board)
    
    n_generations = []
    time_run = []
    N_EXPERIMENTS = 10
    
    pop_size = [20]
    p_mutation = [0.07]
    p_crossover = [1.]
    selection_pressure = [10]
    
    ga_mean_times = []

    for p_size in pop_size:
        for p_m in p_mutation:
            for p_c in p_crossover:
                for s_pres in selection_pressure:
                    ga_log.write("\n Parameters: {}, {}, {}, {}.".format(str(p_size), str(p_m), 
                                                                str(p_c), str(s_pres)))
                    
                    for i in range(N_EXPERIMENTS):
                        ga_log.write("\n Experiment {}:".format(str(i)))
                        
                        stime = time.time()
                        sol, n_gens = genetic_algorithm(sudoku, create_population, fitness,
                                   tournament_selection, solution, crossover,
                                   swap_mutation, elitism_selection, find_best,
                                    pop_size=p_size, p_m=p_m, p_c=p_c, s_pres=s_pres, max_gen=100_000)
                        
                        time_run.append(time.time() - stime)
                        n_generations.append(n_gens)
                    
                    mean_gen = sum(n_generations) / len(n_generations)
                    std_gen = (sum([(x - mean_gen) ** 2 for x in n_generations]) / (len(n_generations) - 1)) ** 0.5
                    ga_log.write("\n Mean: {}; Std: {}".format(str(mean_gen), str(std_gen)))
                    print("\n Mean: {}; Std: {}".format(str(mean_gen), str(std_gen)))
                    
                    mean_time_ga = sum(time_run) / len(time_run)
                    std_time_ga = (sum([(x - mean_time_ga) ** 2 for x in time_run]) / (len(time_run) - 1)) ** 0.5
                    ga_log.write("\n Time mean: {}; Std: {}".format(str(mean_time_ga), str(std_time_ga)))
                    print("\n Time mean: {}; Std: {}".format(str(mean_time_ga), str(std_time_ga)))
                    

    
    