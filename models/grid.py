from utils.alphabet import random_letter
import time

from models.coordinate import Coordinate, get_coordinate, get_coordinate_from_values
from models.node import Node


class Grid:
    def __init__(self, length: int = 4, nodes=None):
        if nodes is None:
            nodes = []

        self.length = length
        self.nodes: list[list[Node]] = nodes
        if not nodes:
            self.__generate_nodes()

    def __repr__(self):
        return "\n".join(str(node) for col in self.nodes for node in col)

    def __str__(self):
        table = []
        for col in range(0, self.length):
            table.append(
                " ".join(str(self.nodes[col][row]) for row in range(0, self.length))
            )
        return "\n".join(row_str for row_str in table)

    def __generate_nodes(self):
        for x in range(0, self.length):
            col = []
            for y in range(0, self.length):
                col.append(Node(random_letter(), get_coordinate(Coordinate(x, y))))
            self.nodes.append(col)

    def get_node(self, x: int, y: int) -> Node:
        return self.nodes[x][y]

    def get_neighbours(self, x: int, y: int, limit=None) -> list[Node]:
        coordinate = get_coordinate_from_values(x, y)
        c_neighbours = coordinate.get_neighbours(limit)

        neighbours = []

        for neighbour in c_neighbours:
            neighbours.append(self.get_node(neighbour.x, neighbour.y))

        return neighbours

    def depth_first_search(
        self, x, y, combinations, max_length, visited=None, path=None
    ):
        if visited is None:
            visited = set()  # ensure these exist on initial call
        if path is None:
            path = []  # ensure these exist on initial call

        node = self.get_node(x, y)
        path.append(node.letter)
        visited.add((x, y))

        combinations.append("".join(path))

        if len(path) < max_length:  # early stopping
            for neighbour in self.get_neighbours(x, y, self.length - 1):
                if (neighbour.coordinate.x, neighbour.coordinate.y) not in visited:
                    self.depth_first_search(
                        neighbour.coordinate.x,
                        neighbour.coordinate.y,
                        combinations,
                        max_length,
                        visited,
                        path,
                    )  # recursive call within function

        visited.remove((x, y))
        path.pop()

    def get_all_combinations(self, max_length) -> set[str]:
        combinations = []

        for col in self.nodes:
            for node in col:
                self.depth_first_search(
                    node.coordinate.x, node.coordinate.y, combinations, max_length
                )  # depth first search for every node as root

        return set(combinations)  # unique combinations only

    @classmethod
    def from_dict(cls, data: dict) -> "Grid":
        nodes_dict = data.get("nodes", [[]])
        nodes = []

        for x in range(0, len(nodes_dict)):
            x: int
            col_dict: list[dict] = nodes_dict[x]

            col: list[Node] = []
            for y in col_dict:
                y: dict
                col.append(Node.from_dict(y))
            nodes.insert(x, col)

        return cls(len(nodes), nodes)


grid = Grid()
print(grid)


def test(max_length):
    start = time.time()
    combs = grid.get_all_combinations(max_length)
    end = time.time()
    print(f"{max_length}. {len(combs):,} letter combinations in {end - start:.5f}s")


test(1)
test(2)
test(3)
test(4)
test(5)
test(6)
test(7)
test(8)
