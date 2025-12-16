from pygame import Color, Rect, Surface, event, key, display

from models.button import Button
from scenes.login.login import LoginScene
from scenes.scene import BaseScene
from utils.alignment import (
    centre_x,
    centre_y,
    centre_x_values,
    centre_y_values,
    get_relative_sub_screen_width,
    get_relative_sub_screen_height,
)


class TitleScene(BaseScene):
    def __init__(self, top: int, left: int):
        super().__init__(top, left)
        self.text = self.heading_one.render("Squaredle", True, Color(0, 0, 0))

        self.previews_bg = Surface((1000, 250))
        self.previews_bg.fill(Color(200, 200, 200))

        self.login_button = Button(
            Rect(0, 0, 50, 50), Color(200, 0, 0), self.__add_login_scene
        )

    def __add_login_scene(self):
        screen = display.get_surface()
        self.sub_scenes.push(
            LoginScene(
                centre_x_values(screen.width, get_relative_sub_screen_width(screen)),
                centre_y_values(screen.height, get_relative_sub_screen_height(screen)),
            )
        )

    def process(self, events: list[event.Event], pressed_keys: key.ScancodeWrapper):
        self.login_button.process(events, pressed_keys)

    def update(self):
        pass

    def render(self, screen: Surface):
        screen.fill((255, 255, 255))

        screen.blit(self.text, (centre_x(screen, self.text), 20))

        screen.blit(self.previews_bg, (0, centre_y(screen, self.previews_bg)))

        self.login_button.render(screen)
