from pygame import SRCALPHA, Color, Surface, draw, font

from models.coordinate import (
    CentreCoordinate,
    Coordinate,
    CornerCoordinate,
    EdgeCoordinate,
    get_coordinate,
)
from utils.alignment import centre_x, centre_y


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
        self.container: Surface = None
        self.content: Surface = None
        self.letter_surface: Surface = None
        self.font: font.Font = None

    def __str__(self):
        return f"{str(self.letter)}"

    def set_surfaces(self, square_length: int):
        self.container = Surface((square_length, square_length))
        self.content = Surface(
            (int(square_length * 0.9), int(square_length * 0.9)), SRCALPHA
        )

        font_height = self.container.get_height() // 2
        if self.font is None or self.font.get_height() != font_height:
            self.font = font.Font("media/mont-heavy.ttf", font_height)

        self.letter_surface = self.font.render(self.letter, True, Color(0, 0, 0))

    def render_surfaces(self):
        self.container.fill((255, 255, 255))
        self.content.fill((0, 0, 0, 0))  # transparent

        radius = int(self.content.get_width() * 0.2)

        rect = self.content.get_rect()

        draw.rect(
            self.content,
            (150, 150, 150),
            rect,
            border_radius=radius,
        )

        # border on top
        draw.rect(
            self.content,
            (120, 120, 120),
            rect,
            width=5,
            border_radius=radius,
        )

        self.content.blit(
            self.letter_surface,
            (
                centre_x(self.content, self.letter_surface),
                centre_y(self.content, self.letter_surface),
            ),
        )

        self.container.blit(
            self.content,
            (
                centre_x(self.container, self.content),
                centre_y(self.container, self.content),
            ),
        )

    @classmethod
    def from_dict(cls, data: dict) -> "Node":
        letter = data.get("letter", "")
        coordinate = get_coordinate(Coordinate.from_dict(data.get("coordinate", {})))
        return cls(letter, coordinate)
