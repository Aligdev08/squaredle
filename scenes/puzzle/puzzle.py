from pygame import Color, Rect, Surface, event, key

from models.grid import Grid
from scenes.scene import BaseScene


class PuzzleScene(BaseScene):
    def __init__(self, grid: Grid):
        super().__init__()

    def process(self, events: list[event.Event], pressed_keys: key.ScancodeWrapper):
        pass

    def update(self):
        pass

    def render(self, screen: Surface):
        screen.fill((255, 255, 255))
