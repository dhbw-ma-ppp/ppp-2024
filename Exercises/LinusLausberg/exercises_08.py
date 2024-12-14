
import os
import numpy as np
import textwrap as tw
import heapq
np.set_printoptions(threshold=np.inf)

# --- Day 15: Chiton ---
# You've almost reached the exit of the cave, but the walls are getting closer together. Your submarine can barely still fit, though; the main problem is that the walls of the cave are covered in chitons, and it would be best not to bump any of them.

# The cavern is large, but has a very low ceiling, restricting your motion to two dimensions. The shape of the cavern resembles a square; a quick scan of chiton density produces a map of risk level throughout the cave (your puzzle input). For example:

# 1163751742
# 1381373672
# 2136511328
# 3694931569
# 7463417111
# 1319128137
# 1359912421
# 3125421639
# 1293138521
# 2311944581
# You start in the top left position, your destination is the bottom right position, and you cannot move diagonally. The number at each position is its risk level; to determine the total risk of an entire path, add up the risk levels of each position you enter (that is, don't count the risk level of your starting position unless you enter it; leaving it adds no risk to your total).

# Your goal is to find a path with the lowest total risk. In this example, a path with the lowest total risk is highlighted here:

# 1163751742
# 1381373672
# 2136511328
# 3694931569
# 7463417111
# 1319128137
# 1359912421
# 3125421639
# 1293138521
# 2311944581
# The total risk of this path is 40 (the starting position is never entered, so its risk is not counted).

# What is the lowest total risk of any path from the top left to the bottom right?

def reading_relativ_cost():
    lines = []
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sequence_path = os.path.join(script_dir, "..", "..", "data",
                                "exercise_cave.txt")
    with open(sequence_path, 'r') as inputfile:
        lines = inputfile.readlines()
        relativ_cost = np.array([list(line.strip()) for line in lines], dtype= int)
    return relativ_cost

def dijkstra(relativ_cost):
    max_lines, max_columes = relativ_cost.shape
    absolut_cost = np.full((max_lines, max_columes), np.inf)
    absolut_cost[0, 0] = 0
    priority_queue = [(0, 0, 0)]  # (cost, x, y)

    while len(priority_queue) != 0:
        current_cost, x, y = heapq.heappop(priority_queue)

        if (x, y) == (max_lines - 1, max_columes - 1):
            return current_cost

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # right, down, left, up
            nx, ny = x + dx, y + dy
            if 0 <= nx < max_lines and 0 <= ny < max_columes:
                new_cost = current_cost + relativ_cost[nx, ny]
                if new_cost < absolut_cost[nx, ny]:
                    absolut_cost[nx, ny] = new_cost
                    heapq.heappush(priority_queue, (new_cost, nx, ny))    

# relativ_cost = np.array([
# [0, 1, 6, 3, 7, 5, 1, 7, 4, 2],
# [1, 3, 8, 1, 3, 7, 3, 6, 7, 2],
# [2, 1, 3, 6, 5, 1, 1, 3, 2, 8],
# [3, 6, 9, 4, 9, 3, 1, 5, 6, 9],
# [7, 4, 6, 3, 4, 1, 7, 1, 1, 1],
# [1, 3, 1, 9, 1, 2, 8, 1, 3, 7],
# [1, 3, 5, 9, 9, 1, 2, 4, 2, 1],
# [3, 1, 2, 5, 4, 2, 1, 6, 3, 9],
# [1, 2, 9, 3, 1, 3, 8, 5, 2, 1],
# [2, 3, 1, 1, 9, 4, 4, 5, 8, 1],
# ])
relativ_cost = reading_relativ_cost()
lowest_risk = dijkstra(relativ_cost)
print("Die niedrigsten Gesamtkosten:", lowest_risk)