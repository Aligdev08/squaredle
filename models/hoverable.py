import pygame
from pygame import Color, Rect, Surface, event, key

from utils.colour import darken


class Hoverable:
    def __init__(self, rect: Rect, colour: Color):
        self.rect = rect
        self.screen = Surface((rect.width, rect.height))

        self.fill = colour
        self.hover_colour = darken(colour)

    def _mouse_up(self):
        pass  # do nothing as hover-able only

    def _mouse_down(self, mouse_pos: tuple[int, int]):
        pass  # do nothing as hover-able only

    def __handle_event(self, e: event.Event, mouse_pos: tuple[int, int]):
        if e.type == pygame.MOUSEBUTTONDOWN:
            self._mouse_up()

        elif e.type == pygame.MOUSEBUTTONUP:
            self._mouse_down(mouse_pos)

    def process(
        self,
        events: list[event.Event],
        pressed_keys: key.ScancodeWrapper,
        relative_pos: tuple[int, int] = None,
    ):
        pos = relative_pos or pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):

            self.screen.fill(self.hover_colour)
            for _event in events:
                self.__handle_event(_event, pos)
        else:
            self.screen.fill(self.fill)

    def render(self, screen: Surface):
        self.screen.blit(
            self.screen,
            [
                self.rect.width / 2 - self.screen.get_rect().width / 2,
                self.rect.height / 2 - self.screen.get_rect().height / 2,
            ],
        )
        screen.blit(self.screen, self.rect)
