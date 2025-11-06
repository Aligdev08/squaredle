from models.grid import Grid
from pygame import Surface
import time


class PuzzlePreview:
    def __init__(self, name: str, grid: Grid, preview_image: Surface):
        self.name = name
        self.grid = grid
        self.loaded_at: float = time.time()
        self.preview_image = preview_image
