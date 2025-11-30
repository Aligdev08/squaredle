from abc import abstractmethod

from pygame import Surface, event, key


class BaseScene:
    def __init__(self):
        self.next = self

    @abstractmethod
    def process(self, events: list[event.Event], pressed_keys: key.ScancodeWrapper):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def render(self, screen: Surface):
        pass

    def switch_scene(self, next_scene: "BaseScene"):
        self.next = next_scene

    def terminate(self):
        self.switch_scene(None)
