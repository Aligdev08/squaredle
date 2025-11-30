import pygame

from scenes.title.title import TitleScene

game_surface = pygame.display.set_mode([500, 500])
pygame.display.set_icon(pygame.image.load("media/logo.jpg"))
pygame.display.set_caption("Squaredle NEA - Ali Ghali")

running = True

active_scene = TitleScene()

while active_scene is not None:
    game_surface.fill((255, 255, 255))

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

    active_scene.process(filtered_events, pressed_keys)
    active_scene.update()
    active_scene.render(game_surface)

    active_scene = active_scene.next

    pygame.display.flip()

    clock = pygame.time.Clock()
    clock.tick(60)
