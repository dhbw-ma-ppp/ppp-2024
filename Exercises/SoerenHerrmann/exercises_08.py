import os
import numpy as np
import sys
from concurrent.futures import ThreadPoolExecutor
# Solve the exercise described at https://adventofcode.com/2021/day/15 using the data at `data/exercise_cave.txt` as input. Prepare a PR as usual.
script_dir = os.path.dirname(os.path.abspath(__file__))
sequence_path = os.path.join(
    script_dir, "..", "..", "data", "exercise_cave.txt"
)


def read_input_sequence(file_path):
    """ Read the input sequence from a file and return it as a numpy array. """
    with open(file_path, 'r') as file:
        # Read the file line by line
        lines = file.readlines()

    # Create the matrix
    matrix = np.array([list(line.strip()) for line in lines if line.strip()], dtype=int)
    return matrix


def minCost(cost, m, n):
    """ Returns the minimum cost to reach the end of the cave using multithreading. """
    if (n < 0 or m < 0):
        return sys.maxsize
    elif (m == 0 and n == 0):
        return cost[m][n]
    else:
        with ThreadPoolExecutor() as executor:
            future1 = executor.submit(minCost, cost, m-1, n)
            future2 = executor.submit(minCost, cost, m, n-1)
            return cost[m][n] + min(future1.result(), future2.result())


def min(x, y):
    """ Returns the minimum of two values. """
    if (x < y):
        return x
    else:
        return y


def test_path_finding():
    test_matrix = [[1, 2, 3],
               [4, 8, 2],
               [1, 5, 3]]
    assert minCost(test_matrix, 2,2) == 11


cave = read_input_sequence(sequence_path)
print(minCost(cave, cave.shape[0]-1, cave.shape[1]-1))