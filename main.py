import pygame

game_surface = pygame.display.set_mode([500, 500])

running = True

while running:
    game_surface.fill((255, 255, 255))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock = pygame.time.Clock()
    clock.tick(60)
