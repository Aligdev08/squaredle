class Coordinate:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def get_neighbours(self) -> list["Coordinate"]:
        neighbours = []
        for x, y in [
            (self.x - 1, self.y),
            (self.x + 1, self.y),
            (self.x, self.y - 1),
            (self.x, self.y + 1),
            (self.x - 1, self.y - 1),
            (self.x - 1, self.y + 1),
            (self.x + 1, self.y + 1),
            (self.x + 1, self.y - 1)
        ]:
            if not any(coord < 0 for coord in [self.x, self.y]):
                neighbours.append(Coordinate(x, y))
        return neighbours


class CornerCoordinate(Coordinate):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)


class EdgeCoordinate(Coordinate):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)


class CentreCoordinate(Coordinate):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)


def get_coordinate(x: int, y: int) -> CentreCoordinate | EdgeCoordinate | CornerCoordinate:
    coordinate = Coordinate(x, y)
    neighbours = coordinate.get_neighbours()
    match len(neighbours):
        case 8:
            return CentreCoordinate(x, y)
        case 5:
            return EdgeCoordinate(x, y)
        case 3:
            return CornerCoordinate(x, y)
