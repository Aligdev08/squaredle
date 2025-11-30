from pygame import Surface, event, key

from scenes.scene import BaseScene


class TitleScene(BaseScene):
    def __init__(self):
        super().__init__()

    def process(self, events: list[event.Event], pressed_keys: key.ScancodeWrapper):
        pass

    def update(self):
        pass

    def render(self, screen: Surface):
        pass
