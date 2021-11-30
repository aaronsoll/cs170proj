from solver import profit
from parse import *
import os

def total_benefit(in_path, out_path):
    tasks = read_input_file(in_path)
    tasks = sorted(tasks, key=lambda task: task.task_id)
    ordered_tasks = read_output_file(out_path)
    curr_benefit = 0
    curr_time = 0
    for task_no in ordered_tasks:
        curr_task = tasks[task_no - 1]
        curr_benefit += profit(curr_task, curr_time)
        curr_time += curr_task.duration
        if curr_time > 1440:
            print(out_path + " is invalid; too many tasks scheduled")
            return
    return curr_benefit

if __name__ == '__main__':
    pass