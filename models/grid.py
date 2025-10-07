from models.node import Node
from models.coordinate import get_coordinate
from models.stack import Stack
from utils.alphabet import random_letter


class Grid:
    def __init__(self, length: int = 4):
        self.length = length
        self.nodes: list[list[Node]] = []
        self.__generate_nodes()

    def __repr__(self):
        return "\n".join(str(node) for col in self.nodes for node in col)

    def __str__(self):
        table = []
        for col in range(0, self.length):
            table.append(" ".join(str(self.nodes[col][row]) for row in range(0, self.length)))
        return "\n".join(row_str for row_str in table)

    def __generate_nodes(self):
        for x in range(0, self.length):
            col = []
            for y in range(0, self.length):
                col.append(Node(random_letter(), get_coordinate(x, y)))
            self.nodes.append(col)

    def get_node(self, x: int, y: int) -> Node:
        return self.nodes[x][y]

    def get_neighbours(self, x: int, y: int) -> list[Node]:
        coordinate = get_coordinate(x, y)
        c_neighbours = coordinate.get_neighbours()

        neighbours = []

        for neighbour in c_neighbours:
            neighbours.append(self.get_node(neighbour.x, neighbour.y))

        return neighbours

    def depth_first_search(self, x: int, y: int):
        pass


grid = Grid(4)
print(grid)
