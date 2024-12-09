import os
import numpy as np
import textwrap as tw
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
        relativ_cost = np.array([list(line[:-1]) for line in lines], dtype= int)
    return relativ_cost


def calcuate_absolut_cost(relativ_cost):
    max_lines = len(relativ_cost)
    max_columes = len(relativ_cost[0])
    absolute_cost = np.zeros((len(relativ_cost),len(relativ_cost[0])), dtype= int)
    for position in range(1, max_lines):
        absolute_cost[position,0] = absolute_cost[position-1,0] + relativ_cost[position,0]
        absolute_cost[0, position] = absolute_cost[0,position-1] + relativ_cost[0, position]
    
    for line_position in range(1, max_lines):
        for colum_position in range(1, max_columes):
            smallest_neighbor = min(check_neighbor(absolute_cost, line_position, 
                                                    colum_position, max_lines, max_columes))
            value = smallest_neighbor + relativ_cost[line_position, colum_position]
            absolute_cost[line_position, colum_position] = value
    # print(absolute_cost)
    for x in absolute_cost:
        print(tw.wrap(str(x), width=400))
    print(absolute_cost[-1,-1])

             

def check_neighbor(absolut_cost, line_position, colum_position, max_lines, max_columes):
    up_absolut_cost = absolut_cost[line_position-1, colum_position]
    
    if line_position+1 < max_lines:
        down_absolut_cost = absolut_cost[line_position+1, colum_position]
    else:
        down_absolut_cost = 1000

    left_absolut_cost = absolut_cost[line_position, colum_position-1]

    if colum_position+1 < max_columes:
        right_absolut_cost = absolut_cost[line_position, colum_position+1]
    else:
        right_absolut_cost = 1000
    if up_absolut_cost == 0: up_absolut_cost = 1000
    if down_absolut_cost == 0: down_absolut_cost = 1000
    if right_absolut_cost == 0: right_absolut_cost = 1000
    if left_absolut_cost == 0: left_absolut_cost = 1000
    return [up_absolut_cost, right_absolut_cost, down_absolut_cost, left_absolut_cost]


relativ_cost = reading_relativ_cost()
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
# print(relativ_cost)
calcuate_absolut_cost(relativ_cost)
