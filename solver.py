from parse import read_input_file, write_output_file
import os
import math
import Task
import heapq
    
def dp_hard_deadline_solver(tasks):
    tasks = sorted(tasks, key=lambda task: task.deadline)
    
    priority_func = lambda task: task.perfect_benefit / task.duration
    
    counter = 0
    rv = []
    curr_time_taken = 0
    heap = []
    used = set() # make sure to implement
    for task in tasks:
        if task.duration > task.deadline:
            continue
        elif task.task_id in used:
            continue
        elif curr_time_taken + task.duration <= task.deadline: # ADD TASK
            heapq.heappush(heap, (priority_func(task), counter,  task))
            counter += 1
            rv.append(task.task_id)
            curr_time_taken += task.duration
            used.add(task.task_id)
        else:
            popped_off_duration = 0
            lost_profit = 0
            popped = []
            while popped_off_duration < curr_time_taken + task.duration - task.deadline:
                popped.append(heapq.heappop(heap)) # can optimize by peaking, not popping
                popped_off_duration += popped[-1][2].duration
                lost_profit += popped[-1][2].perfect_benefit
            if lost_profit / popped_off_duration < task.perfect_benefit / task.duration: # ADD TASK AND REMOVE EXISTING ONES
                for tup in popped:
                    rv.remove(tup[2].task_id)
                    used.remove(tup[2].task_id)
                curr_time_taken -= popped_off_duration 
                curr_time_taken += task.duration
                rv.append(task.task_id)
                heapq.heappush(heap, (priority_func(task), counter, task))
                used.add(task.task_id)
                counter += 1
            else: # DON'T ADD TASK
                for replace in popped:
                    heapq.heappush(heap, replace)
    return rv

def solver(tasks):
    """
    Args:
        tasks: list[Task], list of igloos to polish
    Returns:
        output: list[Int] of igloos in order of polishing  
    """
    COPY_DIST = 1
    NUM_COPIES = 1440
    
    new_tasks = tasks.copy()
    for task in tasks:
        for copy_num in range(1, NUM_COPIES + 1):
            new_deadline = task.deadline + copy_num * COPY_DIST
            if new_deadline > 1440:
                continue
            new_payout = task.get_late_benefit(copy_num * COPY_DIST)
            new_task = Task.Task(task.task_id, new_deadline, task.duration, new_payout)
            new_task.copy_num = copy_num
            new_tasks.append(new_task)
    return dp_hard_deadline_solver(new_tasks)
    


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
                output = solver(tasks)
                write_output_file(output_path, output)