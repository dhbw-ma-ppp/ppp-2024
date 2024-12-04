import numpy as np

def instruction(filename):

    with open("data/exercise_cave.txt", "r") as file:
        rows = file.readlines()
    
    row_count = len(rows)
    column_count = len(rows[0].strip())
    print(f"Row Count: {row_count}")
    print(f"Column Count: {column_count}")

    array = np.zeros((row_count, column_count), dtype=int)
    for i, line in enumerate(rows):
        array[i] = [int(char) for char in line.strip()]
    
    return array

def dijkstra_algo(array, start, end):

    row_count, column_count = array.shape

    risk = np.full((row_count, column_count), np.inf)
    risk[start] = 0

    visited = np.zeros((row_count, column_count), dtype=bool)

    previous_tile = np.full((row_count, column_count), None, dtype=object)

    def get_neighbors(position):
        i, j = position
        neighbors = []

        if i > 0: 
            neighbors.append((i - 1, j))  # oben

        if i < row_count - 1: 
            neighbors.append((i + 1, j))  # unten

        if j > 0: 
            neighbors.append((i, j - 1))  # links

        if j < column_count - 1: 
            neighbors.append((i, j + 1))  # rechts

        return neighbors

    current = start

    while not visited[end]:
        visited[current] = True
        x, y = current

        # risk of neighbours
        for neighbor in get_neighbors(current):
            nx, ny = neighbor

            if not visited[neighbor]:
                new_risk = risk[x, y] + array[nx, ny]

                if new_risk < risk[nx, ny]:  
                    risk[nx, ny] = new_risk
                    previous_tile[nx, ny] = current

        min_risk = np.inf
        for x in range(row_count):

            for y in range(column_count):

                if not visited[x, y] and risk[x, y] < min_risk:
                    min_risk = risk[x, y]
                    current = (x, y)

    path_positions = []
    current = end

    while current is not None:
        path_positions.append(current)
        current = previous_tile[current]

    path_positions.reverse()

    path_values = [array[pos] for pos in path_positions]

    return risk[end], path_values

array = instruction("data/exercise_cave.txt")
start_tile = (0, 0)
end_tile = (array.shape[0] - 1, array.shape[1] - 1)

shortest_path_cost, shortest_path_values = dijkstra_algo(array, start_tile, end_tile)

print(f"Cost of Shortest Path: {shortest_path_cost}")
print(f"Values of Shortest Path: {shortest_path_values}")
