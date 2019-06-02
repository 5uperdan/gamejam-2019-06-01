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
        for x in range(10):
            for y in range(10):
                self.cells[(x, y)] = Neutral_Cell((x, y))

        self.cells[(2, 2)] = Socialist_Cell((2, 2))
        self.cells[(3, 3)] = Road_Cell((3, 3))
        self.cells[(5, 5)] = Capitalist_Cell((5, 5))

        Engine.build_boundary(self.cells)
        
        # initialise 2 players
        #player1_start_cell = random.choice(x for cells in self.cells.values)

        #while player1_start_cell.is_navigable is False:
        #    player1_start_cell = random.choice(self.cells)

        self.capitalist = Capitalist([60, 60])

        #player2_start_cell = random.choice(x for cells in self.cells.values)

        #while player2_start_cell.is_navigable is False:
        #    player2_start_cell = random.choice(self.cells)

        self.socialist = Socialist([30, 30])

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
            cell.tick()
