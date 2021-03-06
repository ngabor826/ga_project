import copy
import time

def solve(grid):
        """
        Input: An 9x9 hyper-sudoku grid with numbers [0-9].
                0 means the spot has no number assigned.
                grid is a 2-Dimensional array. 

        Output: A solution to the game in the same format. 
                'None' otherwise.
        """
        stack = []
        all_moves = set([1,2,3,4,5,6,7,8,9])
        # i is for row and j is for column
        (i, j) = 0, 0
        while i < 9:
            j = 0
            while j < 9:
                if (grid[i][j] == 0):
                    restrictions = get_restrictions(grid,i,j)
                    # Case where restrictions have been broken, must backtrack
                    if restrictions == None:
                        # If backtracking fails, sudoku grid is not solvable
                        bt_result = back_track(grid, stack)
                        if bt_result[2] is False:                        
                            return None
                        else:
                            # Update indexes for grid appropriately
                            i = bt_result[0]
                            j = bt_result[1]                        
                    else:
                        # Get all possible moves
                        moves = list(all_moves.difference(restrictions))
                        if (len(moves) == 0):
                            bt_result = back_track(grid, stack)
                            if bt_result[2] is False:
                                return None
                            else:
                                # Update indexes for grid appropriately
                                i = bt_result[0]
                                j = bt_result[1]
                        else:
                            # Assign last value of moves to grid index
                            grid[i][j] = moves.pop()
                            # Save the other moves in the stack
                            stack.append((i, j, moves))
                j= j + 1
            i = i + 1
        return grid

def get_hyperbox(row_index, column_index):
        # cond. if index is in upper left hyperbox
        if ((1 <= row_index <= 3) and (1 <= column_index <= 3)):
            return (1,1)
        # cond. if index is in upper right hyperbox
        elif ((1 <= row_index <= 3) and (5 <= column_index <= 7)):
            return (1,5)
        # cond. if index is in bottom left hyperbox
        elif ((5 <= row_index <= 7) and (1 <= column_index <= 3)):
            return (5,1)
        # cond. if index is in bottom right hyperbox
        elif ((5 <= row_index <= 7) and (5 <= column_index <= 7)):
            return (5,5)
        # cond. when index is in none of the hyperboxes
        else:
            return (None, None)
        
def get_restrictions(grid, row, column):
        """
        Gets all values in a row, column and 3x3 that can break sudoku rules
        """
        block_row, block_col = row//3 , column//3
        row_restrt, col_restrt, box_restrt, hyper_restrt  = (set([]), set([]),
                                                             set([]), set([]))
        # Getting row and column restrictions
        for i in range(9):
            if grid[row][i] != 0:
                if grid[row][i] in row_restrt:
                    return None;
                row_restrt.add(grid[row][i])
            if grid[i][column] != 0:
                if grid[i][column] in col_restrt:
                    return None;
                col_restrt.add(grid[i][column])
                
        # Get box restrictions
        for m in range(3):
            for n in range(3):
                value = grid[(block_row*3) + m][(block_col*3) + n]
                if value != 0:
                    if value in box_restrt:
                        return None                    
                    box_restrt.add(value)
        
        # Get which hyper box index resides in
        block_row, block_col = get_hyperbox(row, column)
        if (block_row is not None):
            # Get hyper box restrictions
            for m in range(3):
                for n in range(3):
                    value = grid[block_row + m][block_col + n]
                    if value != 0:
                        if value in hyper_restrt:
                            return None                    
                        hyper_restrt.add(value)            
        
        # Union all restrictions before returning
        return (row_restrt.union(col_restrt.union(
                box_restrt.union(hyper_restrt))))
    
def back_track(grid, stack):
        back_track_success = False
        while ((back_track_success is False) and (len(stack) != 0)):
            recent_event = stack.pop()
            row_index = recent_event[0]
            column_index = recent_event[1]
            moves = recent_event[2]
            if (len(moves) != 0):
                # assign new value at grid index and end backtracking
                grid[row_index][column_index] = moves.pop()
                stack.append((row_index, column_index, moves))
                back_track_success = True
                return (row_index, column_index, back_track_success)
            else:
                # Reset index assignment on grid and continue backtracking
                grid[row_index][column_index] = 0
        return (0, 0, False)
    
