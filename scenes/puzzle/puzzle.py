from pygame import (
    MOUSEBUTTONDOWN,
    MOUSEBUTTONUP,
    SRCALPHA,
    Color,
    Rect,
    Surface,
    draw,
    event,
    font,
    key,
    mouse,
)

from models.button import Button
from models.grid import Grid
from models.node import Node
from models.stack import Stack
from models.trie import trie
from scenes.scene import BaseScene
from utils.alignment import centre_x


class PuzzleScene(BaseScene):
    def __init__(self):
        super().__init__()

        grids: list[tuple[Grid, list[str]]] = []

        for i in range(10):
            grid = Grid()
            results = grid.solve(6)
            grids.append((grid, results))

        best_grid, answers = max(grids, key=lambda x: x[1])

        self.grid = best_grid
        self.answers = answers
        self.grid_surface = Surface((500, 500))

        self.letter_font = None

        self.path = Stack(self.grid.length**2)

        self.square_length = self.grid_surface.get_width() // self.grid.length

        self.initiate_nodes()

        self.path_color = (255, 255, 0)

        self.quit_button = Button(
            Rect(950, 0, 50, 50), Color(255, 255, 255), self.terminate, "x", "red"
        )

        self.dragging = False

        self.found = set()

        self.list_font = font.Font("media/mont-heavy.ttf", 20)

        self.show_answers = False

        self.answers_button = Button(
            Rect(0, 0, 100, 50),
            Color(230, 230, 230),
            self.toggle_answer_visibility,
            "show answers",
            "black",
        )

    def initiate_nodes(self):
        for row in range(self.grid.length):
            for col in range(self.grid.length):
                node = self.grid.get_node(row, col)
                node.set_surfaces(self.square_length)

    def toggle_answer_visibility(self):
        self.show_answers = not self.show_answers
        self.answers_button.text = "dont " if self.show_answers else "" + "show answers"

    def handle_letters(self, letters: str):
        if len(letters) > 3 and not letters in self.found:
            if trie.search(letters) is True:
                self.path_color = (0, 255, 0)
            else:
                if trie.is_prefix(letters):
                    self.path_color = (255, 255, 0)
                else:
                    self.path_color = (255, 0, 0)
        else:
            self.path_color = self.path_color = (255, 255, 0)

    def submit_word(self, word: str) -> str:
        if trie.search(word) is True:
            self.found.add(word)

    def process(self, events: list[event.Event], pressed_keys: key.ScancodeWrapper):
        self.quit_button.process(events, pressed_keys, mouse.get_pos())
        self.answers_button.process(events, pressed_keys, mouse.get_pos())

        for e in events:
            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                self.dragging = True
                self.path.clear()
                node = self.get_node_at_mouse(mouse.get_pos())
                if node is not None:
                    self.path.push(node)

            elif e.type == MOUSEBUTTONUP and e.button == 1:
                if self.dragging:
                    letters = "".join(n.letter for n in self.path.to_list())
                    self.submit_word(letters)
                    self.path.clear()
                self.dragging = False

        if not self.dragging:
            return

        node = self.get_node_at_mouse(mouse.get_pos())
        if node is None:
            return

        last = self.path.peek() if not len(self.path) < 1 else None
        if last is None:
            self.path.push(node)
            self.handle_letters("".join(n.letter for n in self.path.to_list()))
            return

        if node == last:
            return

        prev = self.path.peek(2) if not len(self.path) < 2 else None
        if prev is not None and node == prev:
            self.path.pop()
            self.handle_letters("".join(n.letter for n in self.path.to_list()))
            return

        if node.coordinate in last.coordinate.get_neighbours():
            if not node in self.path.to_list():
                self.path.push(node)
                self.handle_letters("".join(n.letter for n in self.path.to_list()))

    def get_node_at_mouse(self, mouse_pos: tuple[int, int]) -> Node | None:
        grid_x = mouse_pos[0] - 250
        grid_y = mouse_pos[1] - 50

        if (
            0 <= grid_x < self.grid_surface.get_width()
            and 0 <= grid_y < self.grid_surface.get_height()
        ):
            col = grid_x // self.square_length
            row = grid_y // self.square_length

            local_x = grid_x % self.square_length
            local_y = grid_y % self.square_length

            margin = max(1, int(self.square_length * 0.05))

            if (
                local_x < margin
                or local_x >= self.square_length - margin
                or local_y < margin
                or local_y >= self.square_length - margin
            ):
                return None

            return self.grid.get_node(row, col)

        return None

    def update(self):
        pass

    def render(self, screen: Surface):
        screen.fill((255, 255, 255))
        self.grid_surface.fill(Color(200, 200, 200), Rect(0, 0, 500, 500))

        for row in range(self.grid.length):
            for col in range(self.grid.length):
                node = self.grid.get_node(row, col)

                node.render_surfaces()

                self.grid_surface.blit(
                    node.container, (col * self.square_length, row * self.square_length)
                )

        nodes = self.path.to_list()
        if len(nodes) >= 2:
            overlay = Surface(self.grid_surface.get_size(), flags=SRCALPHA)

            points: list[tuple[int, int]] = []
            half = self.square_length // 2

            for n in nodes:
                r, c = (
                    n.coordinate.x,
                    n.coordinate.y,
                )
                cx = c * self.square_length + half
                cy = r * self.square_length + half
                points.append((cx, cy))

            draw.lines(
                overlay,
                (self.path_color[0], self.path_color[1], self.path_color[2], 160),
                False,
                points,
                6,
            )

            for p in points:
                draw.circle(
                    overlay,
                    (self.path_color[0], self.path_color[1], self.path_color[2], 200),
                    p,
                    8,
                )

            self.grid_surface.blit(overlay, (0, 0))

        self.quit_button.render(screen)
        self.answers_button.render(screen)

        text_surface = self.list_font.render(
            "You have found:\n- " + "\n- ".join(word.lower() for word in self.found),
            True,
            Color(0, 0, 0),
        )

        answers_surface = self.list_font.render(
            "- " + "\n- ".join(word.lower() for word in self.answers),
            True,
            Color(0, 0, 0),
        )

        if self.show_answers is True:
            screen.blit(answers_surface, (10, 60))

        screen.blit(text_surface, (760, 60))

        screen.blit(self.grid_surface, (250, 50))
