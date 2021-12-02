from parse import read_input_file, write_output_file
import os
import math
import Task
import heapq

# def solve_simple_dp(tasks, seed):
#     """
#     Args:
#         tasks: list[Task], list of igloos to polish
#     Returns:
#         output: list[Int] of igloos in order of polishing  
#     """
    
#     tasks = sorted(tasks, lambda task: task.deadline)
#     n = len(tasks)
#     W = 1440
    
#     K = [[None for w in range(W)] for j in range(n)]
#     for w in range(W):
#         K[w][0] = 0
#     for j in range(n):
#         K[0][j] = 0
        
#     for j in range(1, n + 1):
#         for w in range(1, W + 1):
#             if tasks[j].duration > w:
#                 K[w][j] = K[w][j - 1]
#             elif tasks[j].:
                
#             else:
#                 K[w][j] = max(K[w][j - 1], K[w - tasks[j].duration][j - 1] + tasks[j].perfect_benefit)
#     return K[W, n]
    
def dp_hard_deadline_solver(tasks):
    tasks = sorted(tasks, key=lambda task: task.deadline)
    
    priority_func = lambda task: task.perfect_benefit / task.duration
    
    counter = 0
    rv = []
    curr_time_taken = 0
    heap = []
    for task in tasks:
        if task.duration > task.deadline:
            continue
        elif curr_time_taken + task.duration <= task.deadline:
            heapq.heappush(heap, (priority_func(task), counter,  task)) # add middle element with ever increasing counter
            counter += 1
            rv.append(task.task_id)
        else:
            popped_off_duration = 0
            lost_profit = 0
            popped = []
            while popped_off_duration < curr_time_taken + task.duration - task.deadline:
                popped.append(heapq.heappop(heap)) # can optimize by peaking, not popping
                popped_off_duration += popped[-1][2].duration
                lost_profit += popped[-1][2].perfect_benefit
            if lost_profit / popped_off_duration < task.perfect_benefit / task.duration:
                for id in popped:
                    rv.remove(id) 
                rv.append(task.task_id)
                heapq.heappush(heap, (priority_func(task), counter, task))
                counter += 1
            else:
                for replace in popped:
                    heapq.heappush(heap, (priority_func(replace), counter, replace))
                    counter += 1
    return rv
    


if __name__ == '__main__':
    NUM_TRIALS = 1
    for trial in range(NUM_TRIALS):
        seed = trial
        for folder in ['small/', 'medium/', 'large/']:
            for input_path in os.listdir('inputs/' + folder):
                if input_path[0] == '.':
                    continue
                full_input_path = 'inputs/' + folder + input_path
                output_path = 'outputs/' + folder + input_path[:-3] + '.out'
                tasks = read_input_file(full_input_path)
                output = dp_hard_deadline_solver(tasks)
                write_output_file(output_path, output)