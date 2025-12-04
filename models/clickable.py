from typing import Callable

import pygame
from pygame import Color, Rect, Surface, event, key
from models.hoverable import Hoverable

from utils.colour import darken


class Clickable(Hoverable):
    def __init__(self, rect: Rect, colour: Color):
        super().__init__(rect, colour)

    def __mouse_down(self):
        self.held_down = True

    def __mouse_up(self):
        pass

    def _handle_event(self, e: event.Event):
        if e.type == pygame.MOUSEBUTTONDOWN:
            self.held_down = True

        elif e.type == pygame.MOUSEBUTTONUP:
            if self.rect.collidepoint(mouse_pos) and self.held_down:
                self.held_down = False

    def process(self, events: list[event.Event], pressed_keys: key.ScancodeWrapper):
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            self.screen.fill(self.hover_colour)
            for _event in events:
                if _event.type == pygame.MOUSEBUTTONDOWN:
                    self.__button_down()

                elif _event.type == pygame.MOUSEBUTTONUP:
                    if self.rect.collidepoint(mouse_pos) and self.held_down:
                        self.held_down = False
                        self.on_click()
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
