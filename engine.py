from gameobjects import (Cell, Road_Cell, Rock_Cell, Capturable_Cell,
                         Capitalist_Cell, Socialist_Cell, Neutral_Cell)
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
            self.socialist.killed()
            self.capitalist.score += 200

        for reference, cell in self.cells.items():
            cell.tick(self.capitalist, self.socialist)

def load_level(cells):
    for grid in [(0, 0), (6, 6)]:
        cells[grid] = Socialist_Cell(grid)
    for grid in [(9, 5), (2, 8)]:
        cells[grid] = Capitalist_Cell(grid)
    for grid in [(5,2),(5,3),(7,3),(2,4),(4,5),(3,6),(4,6),(3,7),(4,7),(9,8),(0,9)]:
        cells[grid] = Rock_Cell(grid)
    for grid in [(1, 0), (5, 0), (7, 0),
                 (0, 1), (1, 1), (2, 1), (3, 1), (4, 1),
                 (5, 1), (6, 1), (7, 1), (8, 1), (9, 1),
                 (1, 2), (4, 2), (7, 2), (8, 2),
                 (1, 3), (4, 3), (8, 3),
                 (0, 4), (1, 4), (3, 4), (4, 4),
                 (5, 4), (7, 4), (8, 4), (9, 4),
                 (1, 5), (2, 5), (5, 5), (6, 5), (7, 5), (8, 5),
                 (1, 6), (5, 6), (8, 6), (9, 6),
                 (1, 7), (5, 7), (8, 7),
                 (0, 8), (1, 8), (4, 8), (5, 8), (6, 8), (7, 8), (8, 8),
                 (1, 9), (2, 9), (3, 9), (4, 9), (8, 9), (9, 9)]:
        cells[grid] = Road_Cell(grid)

        for x in range(10):
            for y in range(10):
                if (x, y) not in cells:
                    cells[(x, y)] = Neutral_Cell((x, y))
