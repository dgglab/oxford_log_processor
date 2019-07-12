"""
Functions for processing log files generated from Oxford 80 RIE
"""

import numpy as np


def proccess_log(log_file, recipe_name, step_name, skip_lines=2):
    """
    Returns the mean and standard deviation of all measured parameters for a
    given step of a recipe in a log file.

    Arguments:
        log_file: txt file to parse
        recipe_name: string of the recipe name to pull from the log file
        step_name: string of the specific step in the recipe to pull data from
        skip_lines: logged lines to skip to allow for the plasma to stabalize
    """

    data = []
    for line in log_file:
        data.append(line.strip().split(' '))

    date = int(data[0][-1]) # epoch time

    params = []
    line_count = 0
    in_recipe = False
    in_step = False
    for ls in data:
        if in_recipe and in_step:
            if len(ls) != 32: # check if it is a data line
                if len(ls) == 3: # new recipe
                    in_recipe = False
                    in_step = False
                    line_count = 0
                else: # new step or other break
                    in_step = False
                    line_count = 0
            else:
                if line_count >= skip_lines:
                    params.append(ls)
                else:
                    line_count += 1

        if step_name in ls[0] and in_recipe:
            in_step = True

        if recipe_name in ls[0]:
            in_recipe = True

    stats = []
    stats.append(date)
    for ls in np.array(params).T:
        try:
            stats.append(np.mean(ls.astype(np.float64)))
            stats.append(np.std(ls.astype(np.float64)))
        except ValueError:
            pass
    return stats
