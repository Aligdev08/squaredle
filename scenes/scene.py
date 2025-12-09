from abc import abstractmethod

from pygame import Surface, event, font, key


class BaseScene:
    def __init__(self):
        self.next = self
        self.heading_one = font.Font("media/mont-heavy.ttf", 32)

    @abstractmethod
    def process(self, events: list[event.Event], pressed_keys: key.ScancodeWrapper):
        pass

    def process_all(self, events: list[event.Event], pressed_keys: key.ScancodeWrapper):
        self.process(events, pressed_keys)
        for sub_scene in self.sub_scenes:
            sub_scene.process()

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def render(self, screen: Surface):
        pass

    def switch_scene(self, next_scene: "type[BaseScene]"):
        self.next = next_scene

    def terminate(self):
        self.switch_scene(None)
