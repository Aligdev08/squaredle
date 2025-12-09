from pygame import Color, Rect, Surface, event, key

from models.button import Button
from scenes.scene import BaseScene
from utils.alignment import centre_x, centre_y


class LoginScene(BaseScene):
    def __init__(self):
        super().__init__()
        self.text = self.heading_one.render("Login", True, Color(0, 0, 0))

    def process(self, events: list[event.Event], pressed_keys: key.ScancodeWrapper):
        pass

    def update(self):
        pass

    def render(self, screen: Surface):
        screen.fill((255, 255, 255))

        screen.blit(self.text, (centre_x(screen, self.text), 20))
