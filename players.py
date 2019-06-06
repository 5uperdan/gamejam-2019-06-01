import pygame
from controls import Inputs
import math
from random import choice
from game_enums import Headings, Team

class Player():
    """ represents a player """
    MAX_ENERGY = 300
    def __init__(self, position, size, headings, max_speed, team):
        """
        position: list [x,y]
        headings: list [HeadingEnums, ...]
        """
        self.score = 0
        self.energy = 300
        self.position = position
        self._size = size
        self.headings = headings
        self._velocity = [0, 0]
        self.MAX_SPEED = max_speed
        self.team = team

    @property
    def energy_bar(self):
        """ returns a decimal of energy completion """
        return self.energy / Player.MAX_ENERGY

    @property
    def rect(self):
        """ returns a rect corresponding to the player object """
        return pygame.Rect(self.position, self._size)

    @property
    def centre(self):
        """ returns centre position """
        return (self.position[0] + self._size[0] // 2,
                self.position[1] + self._size[1] // 2)

    @property
    def grid_ref(self):
        """ returns the tuple grid location of the centre of the player """
        centre_of_player = self.centre
        return (math.floor(centre_of_player[0] / 60),
                math.floor(centre_of_player[1] / 60))

    def _damp(self, damp_x=True, damp_y=True):
        """ Decelerates x and y axis movement """
        if damp_x:
            self._velocity[0] = int(0.7 * self._velocity[0])
        if damp_y:
            self._velocity[1] = int(0.7 * self._velocity[1])

    def _move(self):
        self.position[0] += self._velocity[0]
        self.position[1] += self._velocity[1]

    def _accelerate(self, acceleration):
        """ Increases velocity """
        self._velocity[0] += acceleration[0]
        self._velocity[1] += acceleration[1]

        if self._velocity[0] > self.MAX_SPEED:
            self._velocity[0] = self.MAX_SPEED

        if self._velocity[0] < - self.MAX_SPEED:
            self._velocity[0] = - self.MAX_SPEED

        if self._velocity[1] > self.MAX_SPEED:
            self._velocity[1] = self.MAX_SPEED

        if self._velocity[1] < - self.MAX_SPEED:
            self._velocity[1] = - self.MAX_SPEED

    def _handle_movement_inputs(self, inputs):
        damp_x = True
        damp_y = True

        self.headings = []

        if Inputs.UP in inputs:
            self._accelerate((0, -1))
            self.headings.append(Headings.North)
            damp_y = False

        if Inputs.RIGHT in inputs:
            self._accelerate((1, 0))
            self.headings.append(Headings.East)
            damp_x = False

        if Inputs.DOWN in inputs:
            self._accelerate((0, 1))
            self.headings.append(Headings.South)
            damp_y = False

        if Inputs.LEFT in inputs:
            self._accelerate((-1, 0))
            self.headings.append(Headings.West)
            damp_x = False

        self._damp(damp_x, damp_y)

    def correct_for_collision(self, player_grid_ref, object_grid_ref):
        """ corrects player's position after collision with object """
        if object_grid_ref.grid[0] > player_grid_ref[0]:  # push left
            self.position[0] = object_grid_ref.position[0] - player._size[0]
            self._velocity[0] = 0
        if object_grid_ref.grid[0] < player_grid_ref[0]:  # push right
            self.position[0] = object_grid_ref.position[0] + object_grid_ref._size[0]
            self._velocity[0] = 0
        if object_grid_ref.grid[1] > player_grid_ref[1]:  # push up
            self.position[1] = object_grid_ref.position[1] - player._size[1]
            self._velocity[1] = 0
        if object_grid_ref.grid[1] < player_grid_ref[1]:  # push down
            self.position[1] = object_grid_ref.position[1] + object_grid_ref._size[1]
            self._velocity[1] = 0
        self._damp()


    def tick(self, inputs):
        """ Processes one tick for the player """
        if self.energy < Player.MAX_ENERGY:
            self.energy += 0.5

        self._handle_movement_inputs(inputs)

        self._move()


class Capitalist(Player):

    def __init__(self, position):
        super().__init__(
            position,
            size=(30, 30),
            headings=[Headings.North],
            max_speed=8,
            team=Team.Capitalist)


class Socialist(Player):

    def __init__(self, position):
        super().__init__(
            position,
            size=(15, 15),
            headings=[Headings.South],
            max_speed=5,
            team=Team.Socialist)

    def killed(self):
        """ return to one of the hospitals """
        self.position = choice([[10, 10], [50, 50], [80, 80]])