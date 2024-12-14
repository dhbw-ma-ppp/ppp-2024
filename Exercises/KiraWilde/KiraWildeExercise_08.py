# Solve the exercise described at https://adventofcode.com/2021/day/15
# using the data at `data/exercise_cave.txt` as input. Prepare a PR as usual.

import heapq
import os

def read_risk_map(file_path):
    with open(file_path, 'r') as f:
        return [[int(c) for c in line.strip()] for line in f]

def dijkstra_search(risk_map):
    rows = len(risk_map)
    cols = len(risk_map[0])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    #The heap automatically sorts according to risk
    priority_queue = [(0, 0, 0)]  # (risk, x, y)
    visited = set()
    min_risk = [[float('inf')] * cols for _ in range(rows)]
    # The float('inf') is used to represent a very large, practically “infinite” risk.
    # This makes it easy to compare and update lower values later
    min_risk[0][0] = 0 #Start cell

    while priority_queue:
        current_risk, x, y = heapq.heappop(priority_queue)
        if (x, y) == (rows - 1, cols - 1):
            return current_risk

        if (x, y) in visited:
            continue
        visited.add((x, y))

        for direction_x, direction_y in directions:
            # iterates over “directions”, which is a list of movement directions:
            new_x = x + direction_x
            new_y = y + direction_y
            if 0 <= new_x < rows and 0 <= new_y < cols:
                new_risk = current_risk + risk_map[new_x][new_y]
                if new_risk < min_risk[new_x][new_y]:
                    min_risk[new_x][new_y] = new_risk
                    heapq.heappush(priority_queue, (new_risk, new_x, new_y))

# Beispiel-Risikokarte
#risk_map = [
#    [int(c) for c in line]
#    for line in [
#        "1163751742",
#        "1381373672",
#        "2136511328",
#        "3694931569",
#        "7463417111",
#        "1319128137",
#        "1359912421",
#        "3125421639",
#        "1293138521",
#        "2311944581",
#    ]
#]

#print(dijkstra_search(risk_map))

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "..", "..", "data", "exercise_cave.txt")

risk_map = read_risk_map(file_path)
lowest_risk = dijkstra_search(risk_map)
print(f"The lowest total risk is: {lowest_risk}")
