from enum import Enum
import pygame
from controls import Inputs
import math

class Headings(Enum):
    North = 0
    East = 1
    South = 2
    West = 3



class Player():
    """ represents a player """

    MAX_SPEED = 10

    def __init__(self, position):
        """
        position: list [x,y]
        """
        self.position = position
        self._heading = Headings.North
        self._velocity = [0, 0]
        self._size = (15, 15)

    @property
    def rect(self):
        return pygame.Rect(self.position, self._size)

    def get_centre(self):
        """ returns centre position """
        return self.position[0] + 7, self.position[1] + 7

    def get_grid_ref(self):
        """ returns the tuple grid location of the centre of the player """
        return (math.floor((self.position[0] + 7) / 60),
                math.floor((self.position[1] + 7) / 60))

    @classmethod
    def get_surrounding_unnavigable_cells(self, player_grid_ref, cells):
        """ returns a list of cells which surround the player occupied cell
            and are unnavigable
            cells: all game cells
        """
        
        surrounding_cells = []
        for x in (-1, 0, 1):
            for y in (-1, 0, 1):
                if (x, y) != player_grid_ref:
                    candidate_cell = cells[player_grid_ref[0] + x, player_grid_ref[1] + y]
                    if not candidate_cell.is_navigable:
                        surrounding_cells.append(candidate_cell)
        return surrounding_cells

    def _damp(self):
        """ Decelerates x and y axis movement """
        self._velocity[0] = int(0.7 * self._velocity[0])
        self._velocity[1] = int(0.7 * self._velocity[1])

    def _move(self):
        self.position[0] += self._velocity[0]
        self.position[1] += self._velocity[1]

    def tick(self, inputs, cells):
        player_grid_ref = self.get_grid_ref()
        self.handle_inputs(inputs)
        self._move()

        sur_unav_cells = Player.get_surrounding_unnavigable_cells(
            player_grid_ref, cells)

        for cell in sur_unav_cells:
            if self.rect.colliderect(cell.rect):
                self.position = [500, 500]
                self._velocity = [0, 0]
        

    def _accelerate(self, acceleration):
        """ Increases velocity """
        self._velocity[0] += acceleration[0]
        self._velocity[1] += acceleration[1]

        if self._velocity[0] > Player.MAX_SPEED:
            self._velocity[0] = Player.MAX_SPEED

        if self._velocity[0] < - Player.MAX_SPEED:
            self._velocity[0] = - Player.MAX_SPEED

        if self._velocity[1] > Player.MAX_SPEED:
            self._velocity[1] = Player.MAX_SPEED

        if self._velocity[1] < - Player.MAX_SPEED:
            self._velocity[1] = - Player.MAX_SPEED


    def handle_inputs(self, inputs):
        if inputs == [] or inputs == [Inputs.ACTION]:
            self._damp()
            return

        if Inputs.UP in inputs:
            self._accelerate((0, -1))
        if Inputs.RIGHT in inputs:
            self._accelerate((1, 0))
        if Inputs.DOWN in inputs:
            self._accelerate((0, 1))
        if Inputs.LEFT in inputs:
            self._accelerate((-1, 0))
