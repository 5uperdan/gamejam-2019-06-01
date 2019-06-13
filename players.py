import pygame
from controls import Inputs
import math
from random import choice
from game_enums import Headings, Team


class Player():
    """ represents a player """
    MAX_ENERGY = 300

    def __init__(self, position, size, headings, max_speed, team, action_energy):
        """
        position: list [x,y]
        size: tuple (width, height)
        headings: list [HeadingEnums, ...]
        max_speed: int
        team: Team enum
        action_energy: energy required to complete 'action'
        """
        self.position = position
        self._size = size
        self.headings = headings
        self.MAX_SPEED = max_speed
        self.team = team
        self.action_energy = action_energy

        self.energy = 300
        self._velocity = [0, 0]
        self.target = None
        self.ticks_since_action = 1000

    @property
    def meets_action_requirements(self):
        """ returns a boolean """
        return (self.action_energy <= self.energy
                and self.ticks_since_action > 30)

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
    def grid(self):
        """ returns the tuple grid location of the centre of the player """
        centre_of_player = self.centre
        return (math.floor(centre_of_player[0] / 60),
                math.floor(centre_of_player[1] / 60))

    @property
    def position_in_cell(self):
        """ returns the players relative position within a cell """
        centre_of_player = self.centre
        return centre_of_player[0] % 60, centre_of_player[1] % 60

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
        """ Accelerates player """
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

    def set_target(self, grid):
        """ Sets the target grid """
        self.target = grid

    def action_completed(self):
        """ reduces player energy by the amount used by an action """
        self.energy -= self.action_energy
        self.ticks_since_action = 0
        self.target = None

    def correct_for_collision(self, player_grid, obj):
        """ corrects player's position after collision with object
            player_grid: (x,y)
            object: object that player has collided with
        """
        if obj.grid[0] > player_grid[0]:  # push left
            self.position[0] = obj.position[0] - self._size[0]
            self._velocity[0] = 0
        if obj.grid[0] < player_grid[0]:  # push right
            self.position[0] = obj.position[0] + obj._size[0]
            self._velocity[0] = 0
        if obj.grid[1] > player_grid[1]:  # push up
            self.position[1] = obj.position[1] - self._size[1]
            self._velocity[1] = 0
        if obj.grid[1] < player_grid[1]:  # push down
            self.position[1] = obj.position[1] + obj._size[1]
            self._velocity[1] = 0
        self._damp()

    def tick(self, inputs):
        """ Processes one tick for the player """
        if self.energy < Player.MAX_ENERGY:
            self.energy += 1

        self._handle_movement_inputs(inputs)

        self._move()

        self.ticks_since_action += 1


class Capitalist(Player):

    def __init__(self, position):
        super().__init__(
            position,
            size=(30, 30),
            headings=[Headings.North],
            max_speed=4,
            team=Team.Capitalist,
            action_energy=120)


class Socialist(Player):

    def __init__(self, position):
        super().__init__(
            position,
            size=(15, 15),
            headings=[Headings.South],
            max_speed=2.5,
            team=Team.Socialist,
            action_energy=100)

    def killed(self):
        """ return to one of the hospitals """
        self.position = [15, 15]