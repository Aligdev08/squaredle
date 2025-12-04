from pygame import Surface


def centre_x(container: Surface, content: Surface) -> int:
    return (container.width - content.width) // 2


def centre_y(container: Surface, content: Surface) -> int:
    return (container.height - content.height) // 2


def final_x(container: Surface, content: Surface) -> int:
    return container.width - content.width


def final_y(container: Surface, content: Surface) -> int:
    return container.height - content.height
