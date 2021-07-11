import numpy as np


def concat_lists(*args, level=0):
    result = []
    if not level:
        for array in args:
            result = [*result, *array]
    else:
        for array in args:
            for item in array:
                result = [*result, *item]
    return result


def main(length, ballots, weigths):
    table = np.zeros((length, length))
    for ballot in range(len(ballots)):
        for entry in range(len(ballots[ballot])):
            for item in ballots[ballot][entry]:
                for item_lose in concat_lists(
                    ballots[ballot][min(entry + 1, len(ballots)) :], level=1
                ):
                    table[item - 1, item_lose - 1] += weigths[ballot]
    return table
