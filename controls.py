import pygame
from game_enums import Inputs

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

def get_inputs_from_joystick(joystick):
    """ converts joystick inputs into game inputs """
    inputs = []

    if joystick.get_button(1):
        inputs.append(Inputs.ACTION)

    if joystick.get_axis(0) < 0:
        inputs.append(Inputs.LEFT)
    elif joystick.get_axis(0) > 0:
        inputs.append(Inputs.RIGHT)
    
    if joystick.get_axis(1) < 0:
        inputs.append(Inputs.UP)
    elif joystick.get_axis(1) > 0:
        inputs.append(Inputs.DOWN)

    return inputs