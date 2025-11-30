from models.coordinate import (
    CentreCoordinate,
    Coordinate,
    CornerCoordinate,
    EdgeCoordinate,
    get_coordinate,
)


class Node:
    def __init__(
        self,
        letter: str,
        coordinate: CentreCoordinate | EdgeCoordinate | CornerCoordinate,
    ):
        if len(letter) != 1:
            raise ValueError(f"Letter must be one character long.")
        self.letter = letter
        self.selected = False
        self.coordinate = coordinate

    def __str__(self):
        return f"{str(self.letter)}"

    @classmethod
    def from_dict(cls, data: dict) -> "Node":
        letter = data.get("letter", "")
        coordinate = get_coordinate(Coordinate.from_dict(data.get("coordinate", {})))
        return cls(letter, coordinate)
