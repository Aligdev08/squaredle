class Coordinate:
    def __init__(self, x: int, y: int):
        if x < 0 or y < 0:
            raise ValueError("x and y coordinates must be a natural number.")
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
            (self.x + 1, self.y - 1),
        ]:
            if not any(coord < 0 for coord in (x, y)):
                neighbours.append(Coordinate(x, y))
        return neighbours

    @classmethod
    def from_dict(cls, data: dict):
        x = data.get("x", -1)
        y = data.get("y", -1)
        return cls(x, y)


class CornerCoordinate(Coordinate):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)


class EdgeCoordinate(Coordinate):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)


class CentreCoordinate(Coordinate):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)


def get_coordinate_from_values(
    x: int, y: int
) -> CentreCoordinate | EdgeCoordinate | CornerCoordinate:
    return get_coordinate(Coordinate(x, y))


def get_coordinate(
    coordinate: Coordinate,
) -> CentreCoordinate | EdgeCoordinate | CornerCoordinate:
    x, y = coordinate.x, coordinate.y
    neighbours = coordinate.get_neighbours()
    match len(neighbours):
        case 8:
            return CentreCoordinate(x, y)
        case 5:
            return EdgeCoordinate(x, y)
        case 3:
            return CornerCoordinate(x, y)
