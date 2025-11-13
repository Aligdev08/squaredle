from scenes.title.puzzle_preview import PuzzlePreview
from pygame import image
from models.grid import Grid
import os


class PreviewsManager:
    def __init__(self):
        self.previews: list[PuzzlePreview] = []

    def load_preview(self, data: dict):
        name = data.get("name", "")
        grid = data.get("grid", {})
        preview_image = image.load(os.path.join("media", "preview_images", name))

        self.previews.append(PuzzlePreview(name, Grid.from_dict(grid), preview_image))
