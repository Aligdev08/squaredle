from models.coordinate import CentreCoordinate, EdgeCoordinate, CornerCoordinate


class Node:
    def __init__(self, letter: str, coordinate: CentreCoordinate | EdgeCoordinate | CornerCoordinate):
        self.letter = letter
        self.selected = False
        self.coordinate = coordinate

    def __str__(self):
        return f"{str(self.letter)}"
