import pygame
from pygame import Color, Rect, Surface, event, key

from utils.colour import darken


class Hoverable:
    def __init__(
        self,
        rect: Rect,
        colour: Color,
        text: str | None = None,
        text_colour: Color = Color("white"),
        padding: int = 8,
    ):
        self.rect = rect
        self.screen = Surface((rect.width, rect.height), pygame.SRCALPHA)

        self.fill = colour
        self.hover_colour = darken(colour)

        self.text = text
        self.text_colour = text_colour
        self.padding = padding

        self._text_surface: Surface | None = None
        if text:
            self._render_text()

    def _render_text(self):
        max_width = self.rect.width - self.padding * 2
        max_height = self.rect.height - self.padding * 2

        font_size = max_height
        while font_size > 5:
            font = pygame.font.Font(None, font_size)
            surf = font.render(self.text, True, self.text_colour)
            if surf.get_width() <= max_width and surf.get_height() <= max_height:
                self._text_surface = surf
                return
            font_size -= 1

        self._text_surface = None

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

        if self._text_surface:
            text_rect = self._text_surface.get_rect(
                center=self.screen.get_rect().center
            )
            self.screen.blit(self._text_surface, text_rect)

    def render(self, screen: Surface):
        screen.blit(self.screen, self.rect)
