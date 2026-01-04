from pygame import (
    MOUSEBUTTONDOWN,
    MOUSEBUTTONUP,
    SRCALPHA,
    Color,
    Rect,
    Surface,
    draw,
    event,
    key,
    mouse,
)

from models.grid import Grid
from models.node import Node
from models.stack import Stack
from scenes.scene import BaseScene


class PuzzleScene(BaseScene):
    def __init__(self, grid: Grid):
        super().__init__()
        self.grid = grid
        self.grid_surface = Surface((500, 500))
        self.letter_font = None
        self.path = Stack(self.grid.length**2)

        self.square_length = self.grid_surface.get_width() // self.grid.length

        self.initiate_nodes()

        self.dragging = False

    def initiate_nodes(self):
        for row in range(self.grid.length):
            for col in range(self.grid.length):
                node = self.grid.get_node(row, col)
                node.set_surfaces(self.square_length)

    def process(self, events: list[event.Event], pressed_keys: key.ScancodeWrapper):
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
                    print(letters)
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
            return

        if node == last:
            return

        prev = self.path.peek(2) if not len(self.path) < 2 else None
        if prev is not None and node == prev:
            self.path.pop()
            return

        if node.coordinate in last.coordinate.get_neighbours():
            if not node in self.path.to_list():
                self.path.push(node)

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

            draw.lines(overlay, (255, 255, 10, 160), False, points, 6)

            for p in points:
                draw.circle(overlay, (255, 255, 20, 200), p, 8)

            self.grid_surface.blit(overlay, (0, 0))

        screen.blit(self.grid_surface, (250, 50))
