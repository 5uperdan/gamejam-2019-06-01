from enum import Enum
import pygame
from controls import Inputs
import math
from game_cell_handler import capitalise_cell, socialise_cell
from random import choice


class Headings(Enum):
    North = 0
    East = 1
    South = 2
    West = 3


class Player():
    """ represents a player """

    def __init__(self, position, size, headings, max_speed):
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

    @property
    def rect(self):
        return pygame.Rect(self.position, self._size)

    def get_centre(self):
        """ returns centre position """
        return (self.position[0] + self._size[0] // 2,
                self.position[1] + self._size[1] // 2)

    def get_grid_ref(self):
        """ returns the tuple grid location of the centre of the player """
        centre_of_player = self.get_centre()
        return (math.floor(centre_of_player[0] / 60),
                math.floor(centre_of_player[1] / 60))

    @classmethod
    def get_target_grid_refs(self, player_grid_ref, headings):
        """ returns a list of grid refs of the adjacent cells in the
            direction of the headings """
        adjacent_grid_refs = []

        if Headings.North in headings:
            adjacent_grid_refs.append((player_grid_ref[0], player_grid_ref[1] - 1))
        if Headings.East in headings:
            adjacent_grid_refs.append((player_grid_ref[0] + 1, player_grid_ref[1]))
        if Headings.South in headings:
            adjacent_grid_refs.append((player_grid_ref[0], player_grid_ref[1] + 1))
        if Headings.West in headings:
            adjacent_grid_refs.append((player_grid_ref[0] - 1, player_grid_ref[1]))

        return adjacent_grid_refs

    @classmethod
    def get_surrounding_unnavigable_cells(self, player_grid_ref, cells):
        """ returns a list of cells which surround the player occupied cell
            and are unnavigable
            cells: all game cells
        """
        surrounding_cells = []
        for x in (-1, 0, 1):
            for y in (-1, 0, 1):
                candidate_grid_ref = (
                    player_grid_ref[0] + x,
                    player_grid_ref[1] + y)

                if candidate_grid_ref != player_grid_ref:
                    candidate_cell = cells[candidate_grid_ref]
                    if not candidate_cell.is_navigable:
                        surrounding_cells.append(candidate_cell)
        return surrounding_cells

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

    def _handle_action_input(self, player_grid_ref, opponent_grid_ref, cells):
        target_grid_refs = Player.get_target_grid_refs(
            player_grid_ref,
            self.headings)
        if opponent_grid_ref in target_grid_refs:
            target_grid_refs.remove(opponent_grid_ref)

        self.action(cells, target_grid_refs=target_grid_refs)

    def _handle_environment_collisions(self, player_grid_ref, cells):
        sur_unav_cells = Player.get_surrounding_unnavigable_cells(
            player_grid_ref, cells)

        for cell in sur_unav_cells:
            if self.rect.colliderect(cell.rect):
                if cell.grid[0] > player_grid_ref[0]:
                    # push left
                    self.position[0] = cell.position[0] - self._size[0]
                if cell.grid[0] < player_grid_ref[0]:
                    # push right
                    self.position[0] = cell.position[0] + cell._size[0]
                if cell.grid[1] > player_grid_ref[1]:
                    # push up
                    self.position[1] = cell.position[1] - self._size[1]
                if cell.grid[1] < player_grid_ref[1]:
                    # push down
                    self.position[1] = cell.position[1] + cell._size[1]

    def tick(self, inputs, cells, opponent_grid_ref):
        player_grid_ref = self.get_grid_ref()

        self._handle_movement_inputs(inputs)

        if Inputs.ACTION in inputs:
            self._handle_action_input(player_grid_ref, opponent_grid_ref, cells)

        self._move()

        self._handle_environment_collisions(player_grid_ref, cells)


class Capitalist(Player):

    def __init__(self, position):
        super().__init__(
            position,
            size=(30, 30),
            headings=[Headings.North],
            max_speed=7)

    def action(self, cells, target_grid_refs):
        for grid_ref in target_grid_refs:
            if self.energy > 150:
                if capitalise_cell(cells, grid_ref):
                    self.energy -= 150


class Socialist(Player):

    def __init__(self, position):
        super().__init__(
            position,
            size=(15, 15),
            headings=[Headings.South],
            max_speed=4)

    def action(self, cells, target_grid_refs):
        for grid_ref in target_grid_refs:
            if self.energy > 100:
                if socialise_cell(cells, grid_ref):
                    self.energy -= 100
                

    def killed(self):
        """ return to one of the hospitals """
        self.position = choice([[10, 10], [50, 50], [80, 80]])