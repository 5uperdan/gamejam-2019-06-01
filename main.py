import os
import pygame
import pyglet
from engine import Engine
from controls import get_inputs
from gameobjects import Road_Cell, Neutral_Cell, Capitalist_Cell, Socialist_Cell

_image_library = {}


def get_image(path):
    """ It's v inefficient to keep reloading images that are already loaded
        so we manage them with a dictionary instead to avoid reloading.
        The same is true of sounds.
    """
    global _image_library
    image = _image_library.get(path)
    if image is None:
        canonicalized_path = "assets/" + path.replace("/", os.sep).replace("\\", os.sep)
        image = pygame.image.load(canonicalized_path)
        _image_library[path] = image
    return image


RED = (255, 0, 0)
ORANGE = (255, 165, 0)
GREEN = (0, 255, 100)


def draw_progress_bar(screen, cell):
    if cell.is_complete:
        colour = GREEN
    elif cell.is_hindered:
        colour = RED
    else:  # regular
        colour = ORANGE

    pygame.draw.rect(
        screen,
        colour,
        (cell.position, (60 * cell.get_progress(), 5)))


def __main__():
    pygame.init()
    pygame.mouse.set_visible(0)
    clock = pyglet.clock.Clock()
    clock.set_fps_limit(30)

    screen = pygame.display.set_mode((600, 600))
    engine = Engine()
    running = True

    # main game loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))

        pressed = pygame.key.get_pressed()
        p1_inputs, p2_inputs = get_inputs(pressed)

        engine.tick(p1_inputs, p2_inputs)

        # draw cells
        for _, cell in engine.cells.items():
            if type(cell) is Road_Cell:
                screen.blit(get_image('test/road.png'), cell.position)
            elif type(cell) is Neutral_Cell:
                screen.blit(get_image('test/neutral.png'), cell.position)
            elif type(cell) is Capitalist_Cell:
                screen.blit(get_image('test/capitalist.png'), cell.position)
                draw_progress_bar(screen, cell)
            elif type(cell) is Socialist_Cell:
                screen.blit(get_image('test/socialist.png'), cell.position)
            else:
                continue
                
        # draw players
        screen.blit(get_image('car_down.png'), engine.capitalist.position)
        screen.blit(get_image('bike_down_1.png'), engine.socialist.position)

        # updates game screen
        pygame.display.flip()
        clock.tick()


    pygame.quit()
    return True

__main__()