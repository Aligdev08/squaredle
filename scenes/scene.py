from abc import abstractmethod

from pygame import Surface, event, font, key, mouse

from models.stack import Stack
from utils.alignment import (
    centre_x_values,
    centre_y_values,
    get_relative_sub_screen_height,
    get_relative_sub_screen_width,
)


class BaseScene:
    def __init__(self):
        self.next = self
        self.sub_scenes = Stack(10)  # maximum of 10 sub scenes
        self.heading_one = font.Font("media/mont-heavy.ttf", 32)

    @abstractmethod
    def process(self, events: list[event.Event], pressed_keys: key.ScancodeWrapper):
        pass

    def process_all(self, events: list[event.Event], pressed_keys: key.ScancodeWrapper):
        top_sub_scene = self.sub_scenes.peek()

        if top_sub_scene is not None:
            top_sub_scene.process(
                events, pressed_keys
            )  # only process inputs for the top sub_scene
        else:
            self.process(events, pressed_keys)

    @abstractmethod
    def update(self):
        pass

    def update_all(self):
        self.update()
        for sub_scene in self.sub_scenes.array:
            if sub_scene is not None:
                sub_scene.update()

    @abstractmethod
    def render(self, screen: Surface):
        pass

    def render_all(self, screen: Surface):
        self.render(screen)

        sub_screen_width = get_relative_sub_screen_width(screen)
        sub_screen_height = get_relative_sub_screen_height(screen)

        sub_screen = Surface(
            (sub_screen_width, sub_screen_height),
        )
        sub_screen = sub_screen.convert_alpha()
        sub_screen.fill((0, 0, 0, 0))

        for sub_scene in self.sub_scenes.array:
            if sub_scene is not None:
                if sub_scene.next is not None:
                    sub_scene.render(sub_screen)

        screen.blit(
            sub_screen,
            (
                centre_x_values(screen.width, sub_screen_width),
                centre_y_values(screen.height, sub_screen_height),
            ),
        )

    def add_sub_scene(self, sub_scene: "type[BaseScene]") -> int:
        self.sub_scenes.push(sub_scene)
        return len(self.sub_scenes) - 1

    def close_top_sub_scene(self) -> None:
        self.sub_scenes.pop()

    def switch_scene(self, next_scene: "type[BaseScene]"):
        self.next = next_scene

    def terminate(self):
        self.switch_scene(None)
