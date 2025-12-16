from pygame import Surface


def centre_x(container: Surface, content: Surface) -> int:
    return (container.width - content.width) // 2


def centre_y(container: Surface, content: Surface) -> int:
    return (container.height - content.height) // 2


def centre_x_values(container_width: int, content_width: int) -> int:
    return (container_width - content_width) // 2


def centre_y_values(container_height: int, content_height: int) -> int:
    return (container_height - content_height) // 2


def final_x(container: Surface, content: Surface) -> int:
    return container.width - content.width


def final_y(container: Surface, content: Surface) -> int:
    return container.height - content.height


def get_relative_sub_screen_width(parent_screen: Surface) -> int:
    return int(parent_screen.width * 0.7)


def get_relative_sub_screen_height(parent_screen: Surface) -> int:
    return int(parent_screen.height * 0.7)
