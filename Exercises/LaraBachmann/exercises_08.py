"""
- Solve the exercise described at https://adventofcode.com/2021/day/15 using the data at `data/exercise_cave.txt` as input. Prepare a PR as usual.

- Prepare for next Friday by forming groups of 2 (4 with task splitting), and deciding on the rough outline of the analytical app you'd like to build. 
  - Take a look at the datasets available e.g. at
    - https://www.kaggle.com/datasets
    - https://archive.ics.uci.edu/datasets
    - https://scikit-learn.org/1.5/datasets/toy_dataset.html
  - Have some initial idea of what you want to achieve
  - No need to prepare any code yet. You will have the entire lecture on Friday to start working.
"""
import heapq
from pathlib import Path


def read_input_as_matrix(filepath: str) -> list[list[int]]:
    with open(filepath, 'r') as file:
        matrix = [[int(char) for char in line.strip()] for line in file]
        return matrix


def dijkstra(matrix: list[list[int]], target_row: int, target_col: int) -> int:
    rows, cols = len(matrix), len(matrix[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    distances = [[float('inf')] * cols for _ in range(rows)]
    start_row, start_col = 0, 0
    distances[start_row][start_col] = matrix[start_row][start_col]
    
    priority_queue = [(matrix[start_row][start_col], start_row, start_col)]

    while priority_queue:
        current_distance, current_row, current_col = heapq.heappop(priority_queue)

        for directions_row, directions_col in directions:
            neighbor_row, neighbor_col = current_row + directions_row, current_col + directions_col
            if 0 <= neighbor_row < rows and 0 <= neighbor_col < cols:
                new_distance = current_distance + matrix[neighbor_row][neighbor_col]
                if new_distance < distances[neighbor_row][neighbor_col]:
                    distances[neighbor_row][neighbor_col] = new_distance
                    heapq.heappush(priority_queue, (new_distance, neighbor_row, neighbor_col))
    
    return distances[target_row][target_col]


filepath = Path(__file__).parent.parent.parent / 'data' / 'exercise_cave.txt'
matrix = read_input_as_matrix(filepath)
cost_to_last_cell = dijkstra(matrix, len(matrix) - 1, len(matrix[0]) - 1)
print(f"Cost to reach the bottom-right corner: {cost_to_last_cell - matrix[0][0]}")