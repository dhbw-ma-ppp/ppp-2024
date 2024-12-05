import heapq

def find_minimal_risk(grid):
    rows, cols = len(grid), len(grid[0])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    priority_queue = [(0, 0, 0)]
    visited = set()
    minimal_risks = {(0, 0): 0}

    while priority_queue:
        current_risk, row, col = heapq.heappop(priority_queue)

        if (row, col) == (rows - 1, cols - 1):
            return current_risk

        if (row, col) in visited:
            continue
        visited.add((row, col))

        for delta_row, delta_col in directions:
            neighbor_row = row + delta_row
            neighbor_col = col + delta_col

            if 0 <= neighbor_row < rows and 0 <= neighbor_col < cols:
                new_risk = current_risk + grid[neighbor_row][neighbor_col]

                if (neighbor_row, neighbor_col) not in minimal_risks or new_risk < minimal_risks[(neighbor_row, neighbor_col)]:
                    minimal_risks[(neighbor_row, neighbor_col)] = new_risk
                    heapq.heappush(priority_queue, (new_risk, neighbor_row, neighbor_col))

# grid = [
#     [1, 1, 6, 3, 7, 5, 1, 7, 4, 2],
#     [1, 3, 8, 1, 3, 7, 3, 6, 7, 2],
#     [2, 1, 3, 6, 5, 1, 1, 3, 2, 8],
#     [3, 6, 9, 4, 9, 3, 1, 5, 6, 9],
#     [7, 4, 6, 3, 4, 1, 7, 1, 1, 1],
#     [1, 3, 1, 9, 1, 2, 8, 1, 3, 7],
#     [1, 3, 5, 9, 9, 1, 2, 4, 2, 1],
#     [3, 1, 2, 5, 4, 2, 1, 6, 3, 9],
#     [1, 2, 9, 3, 1, 3, 8, 5, 2, 1],
#     [2, 3, 1, 1, 9, 4, 4, 5, 8, 1]
# ]

with open("data/exercise_cave.txt", "r") as file:
    data = file.read()

grid = [list(map(int, line)) for line in data.strip().split("\n")]



minimal_risk = find_minimal_risk(grid)
print(f"The minimal risk is: {minimal_risk}")
