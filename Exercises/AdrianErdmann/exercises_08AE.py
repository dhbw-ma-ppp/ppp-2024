from colorama import Fore
import os

def getKMinDistance(remains: dict, distances: dict|list) -> int|str|tuple:
    """returns the key for 'remains' with the lowest enty in 'distances'"""
    d_min = float("inf")
    n_min = None
    for node in remains:
        if distances[node] < d_min:
            n_min = node
            d_min = distances[node]
    return n_min

def djikstra(graph: dict|list, start=None, end=None) -> dict:
    """djikstra from start in graph to all nodes reachable from start\n
    if end is given the algorithm returns if a path to end is found;\n
    None isn't allowed to be a key for the graph-dict"""
    optimal = {} # stores all nodes that already have a optimal distance; node: (distance, node_reached_from)
    remains = {} # stores node to reach key with least distance; node: node_to_reach_from
    distances = {} # stores least distance to node; node: least_distance

    # initializing
    for node in range(len(graph)):
        remains[node] = None
        distances[node] = float("inf")
    
    optimal[start] = (0)
    for edge in graph[start]:
        distances[edge[0]] = edge[1]
        remains[edge[0]] = start
    
    # djikstra loop
    while remains != {}:
        n_min = getKMinDistance(remains, distances)
        if n_min is None: break # no reachable nodes left
        optimal[n_min] = (distances[n_min], remains[n_min])
        del remains[n_min]

        # if end in optimal: break # end is reached

        # update distances
        for edge_to_n_min in graph[n_min]:
            if edge_to_n_min in optimal: continue # if optimal distance to ege already exists
            if distances[n_min] + edge_to_n_min[1] < distances[edge_to_n_min[0]]:
                remains[edge_to_n_min[0]] = n_min
                distances[edge_to_n_min[0]] = distances[n_min] + edge_to_n_min[1]
    return optimal


script_dir = os.path.dirname(os.path.abspath(__file__))
sequence_path = os.path.join(
    script_dir, "..", "..", "data", "exercise_cave.txt"
)

cave_matrix = []
path_matrix = [] # for later path visualization

with open(sequence_path) as file:
    for line in file:
        cave_column = []
        path_column = []
        for number in line.rstrip():
            cave_column.append(int(number))
            path_column.append(number) # for later path visualization
        if cave_column != []:
            cave_matrix.append(cave_column)
            path_matrix.append(path_column) # for later path visualization

# test matrix:
# cave_matrix = [
#         [1, 1, 6, 3, 7, 5, 1, 7, 4, 2],
#         [1, 3, 8, 1, 3, 7, 3, 6, 7, 2],
#         [2, 1, 3, 6, 5, 1, 1, 3, 2, 8],
#         [3, 6, 9, 4, 9, 3, 1, 5, 6, 9],
#         [7, 4, 6, 3, 4, 1, 7, 1, 1, 1],
#         [1, 3, 1, 9, 1, 2, 8, 1, 3, 7],
#         [1, 3, 5, 9, 9, 1, 2, 4, 2, 1],
#         [3, 1, 2, 5, 4, 2, 1, 6, 3, 9],
#         [1, 2, 9, 3, 1, 3, 8, 5, 2, 1],
#         [2, 3, 1, 1, 9, 4, 4, 5, 8, 1]
#     ]
# path_matrix = []
# for row in cave_matrix:
#     path_column = []
#     for number in row:
#         path_column.append(str(number)) # for later path visualization
#     if cave_column != []:
#         path_matrix.append(path_column) # for later path visualization

path_graph = {} # n*m_max + m equals to the idices
x_max = len(cave_matrix[0]) - 1
y_max = len(cave_matrix) - 1
for y in range(y_max + 1):
    for x in range(x_max + 1):
        # print(y, x)
        path_graph[y*(x_max+1) + x] = []
        # x + 1
        if x < x_max: path_graph[y*(x_max+1) + x].append((y*(x_max+1) + x+1, cave_matrix[y][x+1]))
        # x - 1
        if x > 0: path_graph[y*(x_max+1) + x].append((y*(x_max+1) + x-1, cave_matrix[y][x-1]))
        # y + 1
        if y < y_max: path_graph[y*(x_max+1) + x].append(((y+1)*(x_max+1) + x, cave_matrix[y+1][x]))
        # y - 1
        if y > 0: path_graph[y*(x_max+1) + x].append(((y-1)*(x_max+1) + x, cave_matrix[y-1][x]))


start = 0
end = y_max*(x_max+1) + x_max
find_end = djikstra(path_graph, 0, end)

print(f"It takes a total risk of {find_end[end][0]} to reach the end with the minimal risk.")
print("Here is a visualization of that path:")

# all following code for coloring the path taken
x_max = len(path_matrix[0])
y_max = len(path_matrix)

# color end node
y, x = end // (y_max), end % (x_max)
path_matrix[y][x] = Fore.RED + path_matrix[y][x] + Fore.RESET

prev_node = find_end[end]
while prev_node[1] != start:
    y, x = prev_node[1] // (y_max), prev_node[1] % (x_max)
    path_matrix[y][x] = Fore.YELLOW + path_matrix[y][x] + Fore.RESET
    prev_node = find_end[prev_node[1]]
else:
    # color start node
    y, x = prev_node[1] // (y_max), prev_node[1] % (x_max)
    path_matrix[y][x] = Fore.GREEN + path_matrix[y][x] + Fore.RESET

for line in path_matrix:
    for point in line:
        print(point, end="")
    print()
# end of code for coloring the path teken
