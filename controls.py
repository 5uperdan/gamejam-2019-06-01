from enum import Enum
import pygame


class Inputs(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    ACTION = 4


def get_inputs(pressed):
    """ Converts pygame inputs to game inputs """
    p1_inputs = []
    if pressed[pygame.K_UP]:
        p1_inputs.append(Inputs.UP)
    if pressed[pygame.K_DOWN]:
        p1_inputs.append(Inputs.DOWN)
    if pressed[pygame.K_LEFT]:
        p1_inputs.append(Inputs.LEFT)
    if pressed[pygame.K_RIGHT]:
        p1_inputs.append(Inputs.RIGHT)
    if pressed[pygame.K_RCTRL]:
        p1_inputs.append(Inputs.ACTION)

    p2_inputs = []
    if pressed[pygame.K_w]:
        p2_inputs.append(Inputs.UP)
    if pressed[pygame.K_s]:
        p2_inputs.append(Inputs.DOWN)
    if pressed[pygame.K_a]:
        p2_inputs.append(Inputs.LEFT)
    if pressed[pygame.K_d]:
        p2_inputs.append(Inputs.RIGHT)
    if pressed[pygame.K_LCTRL]:
        p2_inputs.append(Inputs.ACTION)

    return p1_inputs, p2_inputs
