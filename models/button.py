from typing import Callable

import pygame
from pygame import Color, Rect, Surface, event, key

from utils.colour import darken


class Button:
    def __init__(self, rect: Rect, colour: Color, on_click: Callable):
        self.rect = rect
        self.screen = Surface((rect.width, rect.height))

        self.held_down = False

        self.fill = colour
        self.hover_colour = darken(colour)

        self.on_click = on_click

    def process(self, events: list[event.Event], pressed_keys: key.ScancodeWrapper):
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            self.screen.fill(self.hover_colour)
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.held_down = True

                elif event.type == pygame.MOUSEBUTTONUP:
                    if self.held_down:
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
