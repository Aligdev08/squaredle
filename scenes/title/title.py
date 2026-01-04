from pygame import Color, Rect, Surface, display, event, key

from models.button import Button
from models.grid import Grid
from scenes.login.login import LoginScene
from scenes.puzzle.puzzle import PuzzleScene
from scenes.scene import BaseScene
from utils.alignment import (
    centre_x,
    centre_x_values,
    centre_y,
    centre_y_values,
    get_relative_sub_screen_height,
    get_relative_sub_screen_width,
)


class TitleScene(BaseScene):
    def __init__(self):
        super().__init__()
        self.text = self.heading_one.render("Squaredle", True, Color(0, 0, 0))

        self.previews_bg = Surface((1000, 250))
        self.previews_bg.fill(Color(200, 200, 200))

        self.login_button = Button(
            Rect(900, 0, 100, 50), Color(50, 50, 50), self.__add_login_scene, "Login"
        )

        self.generate_button = Button(
            Rect(400, 450, 200, 100),
            Color(200, 200, 200),
            self.__add_puzzle_scene,
            "Generate Puzzle",
            Color("black"),
        )

    def __add_login_scene(self):
        self.sub_scenes.push(LoginScene())

    def __add_puzzle_scene(self):
        self.sub_scenes.push(PuzzleScene())

    def process(self, events: list[event.Event], pressed_keys: key.ScancodeWrapper):
        self.login_button.process(events, pressed_keys)
        self.generate_button.process(events, pressed_keys)

    def update(self):
        pass

    def render(self, screen: Surface):
        screen.fill((255, 255, 255))

        screen.blit(self.text, (centre_x(screen, self.text), 20))

        screen.blit(self.previews_bg, (0, centre_y(screen, self.previews_bg)))

        self.login_button.render(screen)
        self.generate_button.render(screen)
