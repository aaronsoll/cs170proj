from parse import read_input_file, write_output_file
import os

def solve(tasks):
    """
    Args:
        tasks: list[Task], list of igloos to polish
    Returns:
        output: list[Int] of igloos in order of polishing  
    """
    
    # HYPERPARAMETERS
    PPD_WEIGHT = .8
    DURATION_WEIGHT = .05
    DEADLINE_WEIGHT = 1 - PPD_WEIGHT - DURATION_WEIGHT
    
    priority_func = lambda x: PPD_WEIGHT * x.perfect_benefit / x.duration + DURATION_WEIGHT * (-x.duration) + DEADLINE_WEIGHT * (-x.deadline)
    sorted_tasks = sorted(tasks, key=priority_func, reverse=True)
    
    rv = []
    remaining_time = 1440
    loop_again = True
    while loop_again:
        loop_again = False
        for task in sorted_tasks:
            if not task.taken and remaining_time >= task.duration:
                task.taken = True
                remaining_time -= task.duration
                rv.append(task.task_id)
                loop_again = True
    return rv


# Here's an example of how to run your solver.
if __name__ == '__main__':
    for input_path in os.listdir('inputs/inputs/small'):
        if input_path[0] == '.':
            continue
        full_input_path = 'inputs/inputs/small/' + input_path
        output_path = 'outputs/' + input_path[:-3] + '.out'
        tasks = read_input_file(full_input_path)
        output = solve(tasks)
        write_output_file(output_path, output)