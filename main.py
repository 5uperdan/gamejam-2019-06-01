import pygame
import pyglet

def __main__():
    pygame.init()
    pygame.mouse.set_visible(0)
    clock = pyglet.clock.Clock()
    clock.set_fps_limit(30)

    screen = pygame.display.set_mode((600, 600))
    running = True

    # main game loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))

        # updates game screen
        pygame.display.flip()
        clock.tick()

    pygame.quit()
    return True

__main__()