from typing import Callable

from pygame import Color, Rect

from models.hoverable import Hoverable


class Button(Hoverable):
    def __init__(self, rect: Rect, colour: Color, on_click: Callable):
        super().__init__(rect, colour)
        self.on_click = on_click

    def _mouse_up(self):
        self.held_down = True

    def _mouse_down(self, mouse_pos: tuple[int, int]):
        if self.rect.collidepoint(mouse_pos) and self.held_down:
            self.held_down = False
            self.on_click()
