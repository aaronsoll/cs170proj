from parse import read_input_file, write_output_file
import os
import math

def profit(task, start_time):
    if start_time + task.duration <= task.deadline:
        return task.perfect_benefit
    return task.perfect_benefit * math.exp(-.017 * (start_time + task.duration - task.deadline))

def solve(tasks, seed):
    """
    Args:
        tasks: list[Task], list of igloos to polish
    Returns:
        output: list[Int] of igloos in order of polishing  
    """
    
    # HYPERPARAMETERS
    NUM_TIMESTEPS = 1440
    BEFORE_SLOPE = .01
    AFTER_SLOPE = .02
    
    def priority_func(task, curr_time):
        if task.deadline >= curr_time:
            multiplier = 1 - AFTER_SLOPE * (curr_time - task.deadline)
        else:
            multiplier = 1 - BEFORE_SLOPE * (task.deadline - curr_time)
        return multiplier * task.perfect_benefit / task.duration
    
    rv = []
    time_taken = 0
    for timestep in range(NUM_TIMESTEPS):
        curr_time = timestep * 1440 / NUM_TIMESTEPS
        next_time = (timestep + 1) * 1440 / NUM_TIMESTEPS
        if time_taken > curr_time:
            continue
        for task in tasks:
            task.curr_profit = profit(task, curr_time)
            task.next_profit = profit(task, curr_time + 40)
        while time_taken < next_time and len(tasks) > 0:
            best_task = max(tasks, key=lambda task: priority_func(task, curr_time + task.duration))
            tasks.remove(best_task)
            if time_taken + best_task.duration <= 1440:
                time_taken += best_task.duration
                rv.append(best_task.task_id)
    return rv


if __name__ == '__main__':
    NUM_TRIALS = 1
    for trial in range(NUM_TRIALS):
        seed = trial
        for folder in ['small/', 'medium/', 'large/']:
            os.mkdir("outputs/" + folder)
            for input_path in os.listdir('inputs/' + folder):
                if input_path[0] == '.':
                    continue
                full_input_path = 'inputs/' + folder + input_path
                output_path = 'outputs/' + folder + input_path[:-3] + '.out'
                tasks = read_input_file(full_input_path)
                output = solve(tasks, trial)
                write_output_file(output_path, output)