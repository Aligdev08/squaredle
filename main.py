import pygame

pygame.init()

from scenes.title.title import TitleScene

game_surface = pygame.display.set_mode([1000, 600])
pygame.display.set_icon(pygame.image.load("media/logo.jpg"))
pygame.display.set_caption("Squaredle NEA - Ali Ghali")

running = True

active_scene = TitleScene(0, 0)

while active_scene is not None:

    pressed_keys = pygame.key.get_pressed()

    filtered_events = []
    for event in pygame.event.get():
        quit_attempt = False
        if event.type == pygame.QUIT:
            quit_attempt = True
        elif event.type == pygame.KEYDOWN:
            alt_pressed = pressed_keys[pygame.K_LALT] or pressed_keys[pygame.K_RALT]
            if event.key == pygame.K_ESCAPE:
                quit_attempt = True
            elif event.key == pygame.K_F4 and alt_pressed:
                quit_attempt = True

        if quit_attempt:
            active_scene.terminate()
        else:
            filtered_events.append(event)

    active_scene.process_all(filtered_events, pressed_keys)
    active_scene.update_all()
    active_scene.render_all(game_surface)

    active_scene = active_scene.next

    pygame.display.flip()

    clock = pygame.time.Clock()
    clock.tick(60)
