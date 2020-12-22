from bt_algorithm import *
from datetime import datetime


bt_log = open("bt_log.txt", "a")

bt_log.write(str(datetime.now())+": \n")

def bt_experiment(s_board):
    
    run_times = []
    s_board = [s_board[x:x+9] for x in range(0, len(s_board), 9)]

    for i in range(10):
         
        bt_log.write("\n Experiment "+ str(i+1) +":")
        start_time = time.time()
        solve(s_board)
        end_time = time.time()
        bt_log.write(str(end_time-start_time))
        run_times.append(end_time - start_time)
        
    mean_time_bt = sum(run_times) / len(run_times)
    std_time_bt = (sum([(x - mean_time_bt) ** 2 for x in run_times]) / (len(run_times) - 1)) ** 0.5
    bt_log.write("\n Time mean: {}; Std: {}".format(str(mean_time_bt), str(std_time_bt)))
    print("\n Time mean: {}; Std: {}".format(str(mean_time_bt), str(std_time_bt)))

    

def close_bt_log():
    bt_log.close()