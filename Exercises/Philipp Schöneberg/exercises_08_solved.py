import numpy as np
import numpy.typing as npt
from typing import Generator
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

cave_risklevels_list: npt.NDArray
cave_risklevels_list = np.array([
                                [1, 1, 6, 3, 7, 5, 1, 7, 4, 2],
                                [1, 3, 8, 1, 3, 7, 3, 6, 7, 2],
                                [2, 1, 3, 6, 5, 1, 1, 3, 2, 8],
                                [3, 6, 9, 4, 9, 3, 1, 5, 6, 9],
                                [7, 4, 6, 3, 4, 1, 7, 1, 1, 1],
                                [1, 3, 1, 9, 1, 2, 8, 1, 3, 7],
                                [1, 3, 5, 9, 9, 1, 2, 4, 2, 1],
                                [3, 1, 2, 5, 4, 2, 1, 6, 3, 9],
                                [1, 2, 9, 3, 1, 3, 8, 5, 2, 1],
                                [2, 3, 1, 1, 9, 4, 4, 5, 8, 1]])


class Node:
    value: int

    def __init__(self, value: int, node_top = None, node_bottom = None, node_left = None, node_right = None) -> None:
        """
        Creates a node with a maximum of four other nodes connected to it. The
        node will also contain a value representing the weight of all links
        going to it.
        """
        self.value = value
        self.node_top: Node = node_top
        self.node_bottom: Node = node_bottom
        self.node_left: Node = node_left
        self.node_right: Node = node_right
        self.neighbours: list[Node] = []
        if node_top:
            self.neighbours.append(node_top)
        if node_bottom:
            self.neighbours.append(node_bottom)
        if node_left:
            self.neighbours.append(node_left)
        if node_right:
            self.neighbours.append(node_right)


class weightedGraph:
    nodes: list[list[Node]]

    def __init__(self, lines: int, columns: int) -> None:
        """
        Creates an empty 2D array to hold any nodes added in the future.
        """
        self.nodes = np.empty((lines, columns), object)

    def __iter__(self) -> Generator[int, None, None]:
        """
        Returns every node of the weightedGraph instance, going through every
        row and within every row, through every column and so covering every
        element.
        """
        for line in range(len(self.nodes)):
            for column in range(len(self.nodes[line])):
                yield self.nodes[line][column]

    def addNode(self, line: int, column: int, node_value: int, has_top_neighbour: bool, has_left_neighbour: bool) -> None:
        """
        Adds a node to the weightedGraph instance in the order given by the 2D
        array created by initialising.
        """
        if has_top_neighbour and has_left_neighbour:
            newNode = Node(node_value, self.nodes[line-1][column], None, self.nodes[line][column-1], None)
            self.nodes[line-1][column].node_bottom = newNode
            self.nodes[line-1][column].neighbours.append(newNode)
            self.nodes[line][column-1].node_right = newNode
            self.nodes[line][column-1].neighbours.append(newNode)
        elif has_top_neighbour:
            newNode = Node(node_value, self.nodes[line-1][column], None, None, None)
            self.nodes[line-1][column].node_bottom = newNode
            self.nodes[line-1][column].neighbours.append(newNode)
        elif has_left_neighbour:
            newNode = Node(node_value, None, None, self.nodes[line][column-1], None)
            self.nodes[line][column-1].node_right = newNode
            self.nodes[line][column-1].neighbours.append(newNode)
        else:
            newNode = Node(node_value, None, None, None, None)
        self.nodes[line][column] = newNode


def dijkstra_search(graph: weightedGraph, aim: Node) -> tuple[int, list[Node]]:
    """
    Searches for a given node inside a given weightedGraph instance and
    returns the distance given by the weights of the connections as well as a
    list of nodes on the path from the root of the graph to the targeted node.
    """
    def search(nodes_to_go: list[Node], node: Node) -> list:
        """
        Visits the givin node and fetches the dist_to, edge_to and visited
        dictionaries, as well as the nodes_to_go list.
        """
        visited[node] = True
        for elem in node.neighbours:
            if visited[elem] is False:
                if dist_to[elem] > dist_to[node]+elem.value:
                    dist_to[elem] = dist_to[node]+elem.value
                    edge_to[elem] = node
                nodes_to_go.append(elem)
        return nodes_to_go

    def calculate_edges(edges: list[int], edge_to: dict[Node, Node], aim) -> list[int]:
        """
        Fills the edges list with every node from the root to the target.
        """
        if edge_to[aim]:
            edges = calculate_edges(edges, edge_to, edge_to[aim])
        edges.append(aim.value)
        return edges

    dist_to: dict[Node, int] = defaultdict(lambda: np.inf)
    edge_to: dict[Node, Node] = defaultdict(lambda: None)
    visited: dict[Node, bool] = defaultdict(bool)
    nodes_to_go: list[Node] = []
    nodes: list[Node] = []
    edges: list[int] = []
    for elem in graph:
        nodes.append(elem)
    dist_to[nodes[0]] = 0
    search(nodes_to_go, nodes[0])
    while nodes_to_go:
        nodes_to_go = search(nodes_to_go, nodes_to_go.pop(0))
    edges = calculate_edges(edges, edge_to, aim)
    return dist_to[aim], edges


def create_weighted_graph(cave_risklevels_list: list[int]) -> weightedGraph:
    """
    Creates a weightedGraph instance of the same size as a given 2D list. Each
    node is connected to the one above and below it, as well as to each node
    next to it.

    Attention! This list must be able to be converted to a numpy array.
    """
    lines = len(cave_risklevels_list)
    columns = len(cave_risklevels_list[0])
    cave_risklevels__weighted_graph = weightedGraph(lines, columns)
    for line in range(lines):
        for column, elem in enumerate(cave_risklevels_list[line]):
            has_left_neighbour: bool = False
            has_top_neighbour: bool = False
            if line > 0:
                has_top_neighbour = True
            if column > 0:
                has_left_neighbour = True
            cave_risklevels__weighted_graph.addNode(line, column, elem, has_top_neighbour, has_left_neighbour)
    return cave_risklevels__weighted_graph


cave_risklevels_weighted_graph = create_weighted_graph(cave_risklevels_list)
distance, edges = dijkstra_search(cave_risklevels_weighted_graph, cave_risklevels_weighted_graph.nodes[len(cave_risklevels_list)-1][len(cave_risklevels_list[0])-1])
print(f"The best way contains a risk of {distance} and has a risk path as follows: {edges}.")
