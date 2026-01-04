from pygame import Color, Rect, Surface, event, key, mouse

from models.button import Button
from scenes.scene import BaseScene
from utils.alignment import centre_x


class LoginScene(BaseScene):
    def __init__(self):
        super().__init__()
        self.text = self.heading_one.render("Login", True, Color(0, 0, 0))

        self.quit_button = Button(
            Rect(950, 0, 50, 50), Color(255, 255, 255), self.terminate, "x", "red"
        )

    def process(self, events: list[event.Event], pressed_keys: key.ScancodeWrapper):
        self.quit_button.process(events, pressed_keys, mouse.get_pos())

    def update(self):
        pass

    def render(self, screen: Surface):
        screen.fill((255, 255, 255))

        screen.blit(self.text, (centre_x(screen, self.text), 20))

        self.quit_button.render(screen)
