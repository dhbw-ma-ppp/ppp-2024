# You've almost reached the exit of the cave, but the walls are getting closer together. 
# Your submarine can barely still fit, though; the main problem is that the walls of the cave are 
# covered in chitons, and it would be best not to bump any of them.

# The cavern is large, but has a very low ceiling, restricting your motion to two dimensions.
# The shape of the cavern resembles a square; a quick scan of chiton density produces a map of risk 
# level throughout the cave (your puzzle input). For example:

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
# You start in the top left position, your destination is the bottom right position,
# and you cannot move diagonally. The number at each position is its risk level; 
# to determine the total risk of an entire path, add up the risk levels of each position you enter 
# (that is, don't count the risk level of your starting position unless you enter it; leaving it
# adds no risk to your total).

# Your goal is to find a path with the lowest total risk. 
# In this example, a path with the lowest total risk is highlighted here:

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
# The total risk of this path is 40 (the starting position is never entered, 
# so its risk is not counted).

# What is the lowest total risk of any path from the top left to the bottom right?


from collections import deque
import numpy as np

def read_file_to_matrix(file_cave, rows, cols):
    with open(file_cave, 'r') as f:
        content = f.read().strip().split('\n')

    numbers = []
    for line in content:
        numbers.extend([int(char) for char in line])
    matrix = np.array(numbers).reshape(rows, cols)

    return matrix

file_cave = 'data/exercise_cave.txt'
rows = 100
cols = 100
matrix = read_file_to_matrix(file_cave, rows, cols)


moves = [[-1, 0], [1, 0], [0, -1], [0, 1]]

def shortest_distance(grid):
    R = len(grid)
    C = len(grid[0])
    dist = [[float('inf')] * C for _ in range(R)]
    dist[0][0] = 0
    q = deque([(0, 0)])
    
    while q:
        x, y = q.popleft()
        
        for dx, dy in moves:
            new_x = x + dx
            new_y = y + dy
            if 0 <= new_x < R and 0 <= new_y < C:
                new_cost = dist[x][y] + grid[new_x][new_y]
                if new_cost < dist[new_x][new_y]:
                    dist[new_x][new_y] = new_cost
                    q.append((new_x, new_y))
    
    print(dist[R-1][C-1])


shortest_distance(matrix)


