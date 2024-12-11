import os
import numpy as np

script_dir = os.path.dirname(os.path.abspath(__file__))
sequence_path = os.path.join(
    script_dir, "..", "..", "data", "exercise_cave.txt"
)


def read_input_sequence(file_path: str) -> np.ndarray:
    """ Read the input sequence from a file and return it as a numpy array. """
    with open(file_path, 'r') as file:
        # Read the file line by line
        lines = file.readlines()

    # Create the matrix
    matrix = np.array([list(line.strip()) for line in lines if line.strip()], dtype=int)
    return matrix


def minCost(cost: np.ndarray) -> int:
    """ Returns the minimum cost to reach the end of the cave using dynamic programming """
    m, n = cost.shape
    dp = np.zeros((m, n), dtype=int)
    dp[0][0] = cost[0][0]

    for i in range(1, m):
        dp[i][0] = dp[i-1][0] + cost[i][0]

    for j in range(1, n):
        dp[0][j] = dp[0][j-1] + cost[0][j]

    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = cost[i][j] + min(dp[i-1][j], dp[i][j-1])

    return dp[m-1][n-1]


def test_path_finding():
    test_matrix = np.array([[1, 2, 3],
                            [4, 8, 2],
                            [1, 5, 3]])
    assert minCost(test_matrix) == 11


cave: np.array = read_input_sequence(sequence_path)
print(minCost(cave))
