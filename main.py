import os
import pygame
import pyglet
from engine import Engine
from sound import Tune
from controls import get_inputs
from gameobjects import Road_Cell, Rock_Cell, Capitalist_Cell, Socialist_Cell, Neutral_Cell
from pygame.mixer import Sound, get_init, pre_init
import time

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

tune = Tune()
tune.sequence_a = ['c1n','d1n','c1n','e1n','e1n','d1n','c1n',
                   'c1n','d1n','c1n','e1n','e1n','d1n','c1n',
                   'f1n','g1n','f1n','a2n','a2n','g1n','f1n',
                   'c1n','d1n','c1n','e1n','e1n','d1n','c1n',
                   'g1n','a2n','g1n','b2n','b2n','a2n','g1n',
                   'a2n','a2n','g1n','f1n','f1n','e1n','d1n','c1n']
tune.sequence_b = ['c1n','d1n','c1n','d1+','d1+','d1n','c1n',
                  'c1n','d1n','c1n','d1+','d1+','d1n','c1n',
                  'f1n','g1n','f1n','g1+','g1+','g1n','f1n',
                  'c1n','d1n','c1n','d1+','d1+','d1n','c1n',
                  'g1n','a2n','g1n','a2+','a2+','a2n','g1n',
                  'g1+','g1+','g1n','f1n','f1n','d1+','d1n','c1n']
tune.lengths = [0.6, 0.6, 0.6, 0.3, 1.2, 0.6, 5.4,
                0.6, 0.6, 0.6, 0.3, 1.2, 0.6, 5.4,
                0.6, 0.6, 0.6, 0.3, 1.2, 0.6, 5.4,
                0.6, 0.6, 0.6, 0.3, 1.2, 0.6, 5.4,
                0.6, 0.6, 0.6, 0.3, 1.2, 0.6, 5.4,
                0.6, 0.6, 0.6, 0.3, 1.2, 0.6, 2.5, 2.5]
tune.pauses = [0.8, 0.8, 0.8, 1.6, 1.6, 0.8, 6.0,
               0.8, 0.8, 0.8, 1.6, 1.6, 0.8, 6.0,
               0.8, 0.8, 0.8, 1.6, 1.6, 0.8, 6.0,
               0.8, 0.8, 0.8, 1.6, 1.6, 0.8, 6.0,
               0.8, 0.8, 0.8, 1.6, 1.6, 0.8, 6.0,
               0.8, 0.8, 0.8, 1.6, 1.6, 0.8, 3.0, 3.0]
tune.speed = 6.0

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


def splash_screen(screen, clock):
    screen.blit(get_image('new/splash_screen.png'), (0,0))
    pygame.display.flip()
    for n in range(270):
        clock.tick()
    return


def __main__():
    pre_init(44100, -16, 1, 1024)
    pygame.init()
    pygame.font.init()
    pygame.mouse.set_visible(0)
    clock = pyglet.clock.Clock()
    clock.set_fps_limit(30)

    screen = pygame.display.set_mode((600, 600), pygame.FULLSCREEN)
    splash_screen(screen, clock)
    engine = Engine()
    running = True

    # main game loop
    melody_loop_count = 0
    
    while running:
        # playing the background melody in two keys
        if melody_loop_count == 0:
            tune.play('a')
        elif melody_loop_count == 1150:
            tune.play('b')
        elif melody_loop_count >= 2300:
            melody_loop_count = -1
        Tune.tick()
        melody_loop_count += 1
        clock.tick()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
        screen.fill((0, 0, 0))

        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_ESCAPE]:
            return

        p1_inputs, p2_inputs = get_inputs(pressed)

        if engine.tick(p1_inputs, p2_inputs) == 'c':
            myfont = pygame.font.SysFont('Comic Sans MS', 35)
            capitalist_score_text = myfont.render('The socialist state has been knocked down!', False, (0, 255, 0))
            screen.blit(capitalist_score_text, (15, 15))
            pygame.display.flip()
            time.sleep(5)
            engine = Engine()


        elif engine.tick(p1_inputs, p2_inputs) == 's':
            myfont = pygame.font.SysFont('Comic Sans MS', 35)
            capitalist_score_text = myfont.render('The capitalist state has been knocked down!: ', False, (0, 255, 0))
            screen.blit(capitalist_score_text, (15, 15))
            pygame.display.flip()
            time.sleep(5)
            engine = Engine()
        
        # draw cells
        for _, cell in engine.cells.items():
            if type(cell) is Road_Cell:
                screen.blit(get_image('new/road_blank.png'), cell.position)
            elif type(cell) is Rock_Cell:
                screen.blit(get_image('new/rock.png'), cell.position)
            elif type(cell) is Capitalist_Cell:
                screen.blit(get_image('new/office.png'), cell.position)
                draw_progress_bar(screen, cell)
            elif type(cell) is Socialist_Cell:
                screen.blit(get_image('new/park-lake.png'), cell.position)
                draw_progress_bar(screen, cell)
            elif type(cell) is Neutral_Cell:
                screen.blit(get_image('new/neutral.png'), cell.position)
            else:
                continue

        # draw players
        screen.blit(get_image('new/car.png'), engine.capitalist.position)
        screen.blit(get_image('bike_down_1.png'), engine.socialist.position)

        # draw energy meters
        pygame.draw.rect(
            screen,
            GREEN,
            (engine.capitalist.position, (30 * engine.capitalist.energy_bar, 5)))

        pygame.draw.rect(
            screen,
            GREEN,
            ((engine.socialist.position[0] - 15, engine.socialist.position[1]), (30 * engine.socialist.energy_bar, 5)))

        # draw scores
        myfont = pygame.font.SysFont('Comic Sans MS', 20)
        capitalist_score_text = myfont.render('Capitalism: ' + str(engine.capitalist.score), False, (0, 255, 0))
        screen.blit(capitalist_score_text, (15, 15))

        socialist_score_text = myfont.render('Socialism: ' + str(engine.socialist.score), False, (255, 0, 0))
        screen.blit(socialist_score_text, (15, 45))
        
        # updates game screen
        pygame.display.flip()

    pygame.quit()
    return True

__main__()