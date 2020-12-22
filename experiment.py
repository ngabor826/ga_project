from ga_algorithm import *
from ga_experiment import *
from bt_experiment import *
from bt_algorithm import *

def printGrid(grid):
            print("-"*25)
            for i in range(9):
                print("|", end=" ")
                for j in range(9):
                    print(grid[i][j], end=" ")
                    if (j % 3 == 2):
                        print("|", end=" ")
                print()
                if (i % 3 == 2):
                    print("-"*25)

for i in range(5):
    
    s_board = []
    
    with open("test"+str(i)+".txt", "r") as s_file:
        lines = s_file.readlines()
        s_board += [int(x) for line in lines for x in line.split()]
        s_board_array = [s_board[x:x+9] for x in range(0, len(s_board), 9)]
    
    print("\n" + str(i+1)+". sudoku to solve: \n")           
    printGrid(s_board_array)
    
    print(" \n GA Experiment Results:")
    ga_experiment(s_board)
    
    print(" \n Backtracking Experiment Results:")

    bt_experiment(s_board)
    
close_ga_log()
close_bt_log()


