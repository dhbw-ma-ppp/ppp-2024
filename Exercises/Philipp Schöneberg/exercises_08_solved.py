import numpy as np
from collections import defaultdict


# - Solve the exercise described at https://adventofcode.com/2021/day/15 using the data at `data/exercise_cave.txt` as input. Prepare a PR as usual.
#
# - Prepare for next Friday by forming groups of 2 (4 with task splitting), and deciding on the rough outline of the analytical app you'd like to build.
#   - Take a look at the datasets available e.g. at
#     - https://www.kaggle.com/datasets
#     - https://archive.ics.uci.edu/datasets
#     - https://scikit-learn.org/1.5/datasets/toy_dataset.html
#   - Have some initial idea of what you want to achieve
#   - No need to prepare any code yet. You will have the entire lecture on Friday to start working.

risk_map_list: list[list[int]] = [[1, 1, 6, 3, 7, 5, 1, 7, 4, 2],
                                  [1, 3, 8, 1, 3, 7, 3, 6, 7, 2],
                                  [2, 1, 3, 6, 5, 1, 1, 3, 2, 8],
                                  [3, 6, 9, 4, 9, 3, 1, 5, 6, 9],
                                  [7, 4, 6, 3, 4, 1, 7, 1, 1, 1],
                                  [1, 3, 1, 9, 1, 2, 8, 1, 3, 7],
                                  [1, 3, 5, 9, 9, 1, 2, 4, 2, 1],
                                  [3, 1, 2, 5, 4, 2, 1, 6, 3, 9],
                                  [1, 2, 9, 3, 1, 3, 8, 5, 2, 1],
                                  [2, 3, 1, 1, 9, 4, 4, 5, 8, 1]]


def read_file(input_file: str) -> list[list[int]]:
    """
    Creates and returns a list of integers from a given file.
    """
    risk_map_list: list[list[int]] = []
    with open(input_file, "r") as f:
        for line in f:
            line_list: list[int] = []
            line = line.strip()
            for char in line:
                line_list.append(int(char))
            risk_map_list.append(line_list)
    return risk_map_list


def create_adjacency_list(risk_map_list: list) -> dict[int, list[tuple]]:
    """
    Generates an adjacency list of a graph given as a list of list of integers.
    Each node is herby connected to the one above and below it, as well as to
    each node next to it.
    """
    risk_map_adjacency_list: dict[tuple[int, int], list[tuple]] = defaultdict(list)
    lines = len(risk_map_list)
    columns = len(risk_map_list[0])
    for line in range(lines):
        for column in range(columns):
            node_number: int = line*columns+column
            node_value: int = risk_map_list[line][column]
            if line > 0:
                # Has top-neighbour
                risk_map_adjacency_list[(node_number, node_value)].append(((line-1)*columns+column, risk_map_list[line-1][column]))
            if line < lines-1:
                # Has bottom-neighbour
                risk_map_adjacency_list[(node_number, node_value)].append(((line+1)*columns+column, risk_map_list[line+1][column]))
            if column > 0:
                # Has left-neighbour
                risk_map_adjacency_list[(node_number, node_value)].append((line*columns+column-1, risk_map_list[line][column-1]))
            if column < columns-1:
                # Has right-neighbour
                risk_map_adjacency_list[(node_number, node_value)].append((line*columns+column+1, risk_map_list[line][column+1]))
    return risk_map_adjacency_list


def dijkstra_search(risk_map_adjacency_list: dict[int, list[tuple]], start: tuple[int, int], aim: tuple[int, int]) -> tuple[int, list[int]]:
    """
    Searches for a given node within a given adjacency list of a weighted
    graph and returns the distance given by the weights of the links, as well
    as the list of nodes on the path from the starting node to the target node.
    """
    def search(risk_map_adjacency_list: dict[int, list[tuple]], nodes_to_go: list[int], node: tuple[int, int]) -> list[int]:
        """
        Visits the givin node and fetches the dist_to, edge_to and visited
        dictionaries, as well as the nodes_to_go list.
        """
        visited[node] = True
        for elem in risk_map_adjacency_list[node]:
            if visited[elem] is False:
                if dist_to[elem] > dist_to[node]+elem[1]:
                    dist_to[elem] = dist_to[node]+elem[1]
                    edge_to[elem] = node
                nodes_to_go.append(elem)
        return nodes_to_go

    def calculate_edges(edges: list[int], edge_to: dict[int, int], aim: tuple[int, int]) -> list[int]:
        """
        Fills the edge list with the weight of each node on the way from the
        start to the target node.
        """
        if edge_to[aim]:
            edges = calculate_edges(edges, edge_to, edge_to[aim])
        edges.append(aim[1])
        return edges

    dist_to: dict[tuple[int, int], int] = defaultdict(lambda: np.inf)
    edge_to: dict[tuple[int, int], tuple[int, int]] = defaultdict(lambda: None)
    visited: dict[tuple[int, int], bool] = defaultdict(bool)
    nodes_to_go: list[tuple[int, int]] = []
    edges: list[int] = []

    dist_to[start] = 0
    nodes_to_go = search(risk_map_adjacency_list, nodes_to_go, start)
    while nodes_to_go:
        node = nodes_to_go.pop(0)
        if visited[node] is False:
            nodes_to_go = search(risk_map_adjacency_list, nodes_to_go, node)
        if visited[aim] is True:
            break
    edges = calculate_edges(edges, edge_to, aim)
    return dist_to[aim], edges


def test():
    """
    Tests the functionality of the programme.
    """
    lines = len(risk_map_list)
    columns = len(risk_map_list[0])
    risk_map_adjacency_list = create_adjacency_list(risk_map_list)
    assert 40, [1, 1, 2, 1, 3, 6, 5, 1, 1, 1, 5, 1, 1, 3, 2, 3, 2, 1, 1] == dijkstra_search(risk_map_adjacency_list, (0, risk_map_list[0][0]), (len(risk_map_adjacency_list)-1, risk_map_list[lines-1][columns-1]))
    print("The test was successful!")


test()

risk_map_list = read_file("exercise_cave.txt")

distance: int
edges: list[int]
lines: int = len(risk_map_list)
columns: int = len(risk_map_list[0])
risk_map_adjacency_list: dict[int, list[tuple]]

risk_map_adjacency_list = create_adjacency_list(risk_map_list)
distance, edges = dijkstra_search(risk_map_adjacency_list, (0, risk_map_list[0][0]), (len(risk_map_adjacency_list)-1, risk_map_list[lines-1][columns-1]))
print(f"The best path contains a risk of {distance} and has a risk path as follows:\n{edges}.")
