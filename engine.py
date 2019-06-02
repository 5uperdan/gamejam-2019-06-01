from gameobjects import (Cell, Road_Cell, Neutral_Cell,
                         Capitalist_Cell, Socialist_Cell)
from players import Capitalist, Socialist
import random


class Engine():
    """ Main game engine """

    def __init__(self):
        """ Setup game engine """
        # load level
        self.cells = {}

        load_level(self.cells)

        Engine.build_boundary(self.cells)
        
        self.socialist = Socialist([75, 75])

        self.capitalist = Capitalist([550, 75])

    @classmethod
    def build_boundary(self, cells):
        """ builds the game boundary """
        # left and right boundary columns
        for x in (-1, 10):
            for y in range(-1, 11):
                cells[(x, y)] = Cell((x, y), is_navigable=False)

        # top and bottom boundary columns
        for x in range(10):
            for y in (-1, 10):
                cells[(x, y)] = Cell((x, y), is_navigable=False)


    def tick(self, p1_inputs, p2_inputs):
        """ Progresses the game one tick forward """

        self.capitalist.tick(
            inputs=p1_inputs,
            cells=self.cells,
            opponent_grid_ref=self.socialist.get_grid_ref())

        self.socialist.tick(
            inputs=p2_inputs,
            cells=self.cells,
            opponent_grid_ref=self.capitalist.get_grid_ref())

        if self.capitalist.rect.colliderect(self.socialist.rect):
            self.capitalist.killed_socialist()
            self.socialist.killed()

        for reference, cell in self.cells.items():
            cell.tick(self.capitalist, self.socialist)

def load_level(cells):
    for grid in [(0, 0)]:
        self.cells[grid] = Socialist_Cell(grid)
    for grid in [(0, 1), (0, 5), (0, 7)]:
        self.cells[grid] = Road_Cell(grid)
