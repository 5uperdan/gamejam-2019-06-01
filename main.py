import os
# hide the pygame console message
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
import pygame
import pyglet
from engine import Engine, GameState
from sound import Tune
from controls import get_inputs, get_inputs_from_joystick
from gameobjects import Road_Cell, Rock_Cell, Capitalist_Cell, Socialist_Cell, Neutral_Cell
from pygame.mixer import Sound, get_init, pre_init
import time
from game_enums import Team


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
BLUE = (0, 0, 255)

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

tune_alt1 = Tune()

tune_alt2 = Tune()

tune_alt1.sequence_a = [
    'c2n', 'b2n', 'a2n', 'g1n',
    'b2n', 'a2n', 'g1n', 'f1n',
    'a2n', 'g1n', 'f1n', 'e1n',
    'g1n'
    ]

tune_alt2.sequence_a = [
    'c1n', 'd1n', 'e1n', 'f1n',
    'd1n', 'e1n', 'f1n', 'g1n',
    'e1n', 'f1n', 'g1n', 'a2n',
    'c2n'
    ]

tune_alt1.lengths = tune_alt2.lengths = [
    1.2, 1.2, 1.2, 1.2,
    1.2, 1.2, 1.2, 1.2,
    1.2, 1.2, 1.2, 1.2,
    4.8
]
tune_alt1.pauses = tune_alt2.pauses = tune_alt1.lengths
tune_alt1.speed = tune_alt2.speed = 5.0


def draw_progress_bar(screen, cell):
    if cell.is_complete:
        colour = GREEN
    elif cell.is_destroyable:
        colour = RED
    else:  # regular
        colour = ORANGE

    pygame.draw.rect(
        screen,
        colour,
        (cell.position, (60 * cell.progress, 5)))


def draw_score_bars(screen, capitalist_completion, socialist_completion):
    """ draws score bars on the edges of the screen
        Args:
            capitalist_completion: decimal 0-1
            socialist_completion: decimal 0-1
    """
    pygame.draw.rect(
        screen,
        RED,
        ((0, 600), (20, -600 * socialist_completion)))

    pygame.draw.rect(
        screen,
        BLUE,
        ((620, 600), (20, - 600 * capitalist_completion)))


def splash_screen():
    screen = pygame.display.set_mode((600, 600))  # , pygame.FULLSCREEN)
    screen.blit(get_image('new/splash_screen.png'), (0, 0))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                return pygame.key.get_pressed()


def draw_winning_team(winning_team):
    screen = pygame.display.set_mode((600, 600))  #, pygame.FULLSCREEN)

    myfont = pygame.font.SysFont('Comic Sans MS', 35)
    text = 'The {} state has been knocked down!'.format(
        'capitalist' if winning_team == GameState.SOCIALIST_WIN else 'socialist'
    )

    text = myfont.render(
        'The capitalist state has been knocked down!: ',
        False,
        (0, 255, 0))

    screen.blit(text, (15, 15))
    pygame.display.flip()

    time.sleep(3)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                return pygame.key.get_pressed()


def initialise():
    """ Sets up things that are only required once per application load """
    # sound system
    pre_init(44100, -16, 1, 1024)
    pygame.init()
    pygame.font.init()
    pygame.mouse.set_visible(0)


def setup_joystick():
    """ returns a joystick if one has been successfully initialised """
    try:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        return joystick
    except expression as identifier:
        pass
    return None


def run_game():
    """ Plays a single instance of the game, returns the winning team """
    # setup fps limit
    clock = pyglet.clock.Clock()
    clock.set_fps_limit(60)

    # screen parameters
    screen = pygame.display.set_mode((640, 600))
    gameplay_surface = pygame.Surface((600, 600))

    # create game engine
    engine = Engine()

    joystick = setup_joystick()

    melody_tick_count = 0
    running = True

    # main game loop
    while running:
        melody_tick_count += 1
        # playing the background melody in two keys
        if melody_tick_count == 1:
            tune.play('a')
        elif melody_tick_count == 1150:
            tune.play('b')
        elif melody_tick_count >= 2300:
            melody_tick_count = 0
        tune.tick()
        clock.tick()

        # clear event queue and check for exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
        # handle inputs
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_ESCAPE]:
            running = False

        p1_inputs, p2_inputs = get_inputs(pressed)

        if joystick is not None:
            p2_inputs = get_inputs_from_joystick(joystick)

        # progress game by one tick and check for exit
        game_state = engine.tick(p1_inputs, p2_inputs)

        if game_state != GameState.RUNNING:
            return game_state

        # clear gameplay surface
        gameplay_surface.fill((0, 0, 0))

        # draw cells
        for _, cell in engine.cell_handler.cells.items():
            if type(cell) is Road_Cell:
                gameplay_surface.blit(get_image('new/road_blank.png'), cell.position)
            elif type(cell) is Rock_Cell:
                gameplay_surface.blit(get_image('new/road_blank.png'), cell.position)
                gameplay_surface.blit(get_image('new/rock.png'), cell.position)
            elif type(cell) is Capitalist_Cell:
                gameplay_surface.blit(get_image('new/neutral.png'), cell.position)
                gameplay_surface.blit(get_image('new/office.png'), cell.position)
                draw_progress_bar(gameplay_surface, cell)
            elif type(cell) is Socialist_Cell:
                gameplay_surface.blit(get_image('new/park-lake.png'), cell.position)
                draw_progress_bar(gameplay_surface, cell)
            elif type(cell) is Neutral_Cell:
                gameplay_surface.blit(get_image('new/neutral.png'), cell.position)
            else:
                continue

        # draw players, action highlights & energy meters
        for capitalist in engine.capitalists:
            gameplay_surface.blit(get_image('new/car.png'), capitalist.position)
            pygame.draw.rect(
                gameplay_surface,
                GREEN if capitalist.meets_action_requirements else RED,
                (capitalist.position, (30 * capitalist.energy_bar, 5)))

            if capitalist.target is not None:
                targetted_cell = engine.cell_handler.cells[capitalist.target]
                pygame.draw.rect(
                    gameplay_surface,
                    BLUE,
                    (targetted_cell.position, (60, 60)),
                    3)  # width of line
                
        
        for socialist in engine.socialists:
            gameplay_surface.blit(get_image('bike_down_1.png'), socialist.position)
            pygame.draw.rect(
                gameplay_surface,
                GREEN if socialist.meets_action_requirements else RED,
                (socialist.position, (30 * socialist.energy_bar, 5)))

            if socialist.target is not None:
                targetted_cell = engine.cell_handler.cells[socialist.target]
                pygame.draw.rect(
                    gameplay_surface,
                    RED,
                    (targetted_cell.position, (60, 60)),
                    2)  # width of line

        # add gameplay surface to screen
        screen.blit(gameplay_surface, (20, 0))

        # draw score bars outside gameplay surface
        draw_score_bars(
            screen,
            engine.get_score_completion(Team.Capitalist),
            engine.get_score_completion(Team.Socialist))

        # updates game screen
        pygame.display.flip()

    # if we've fallen out of the main game loop then quit
    return GameState.QUIT


def __main__():
    """ Entry point for application """
    initialise()
    # hold at splash screen until user input
    pressed = splash_screen()

    while True:
        if pressed[pygame.K_ESCAPE]:
            pygame.quit()
            return  # exit game
        if pressed[pygame.K_a]:
            game_state = run_game()  # two player
        elif pressed[pygame.K_b]:
            game_state = run_game()  # four player
        else:
            game_state = run_game()  # just start the game

        if game_state == GameState.QUIT:
            return
        else:
            # without clearing the screen buffer, draw the winning team
            pressed = draw_winning_team(game_state)

__main__()