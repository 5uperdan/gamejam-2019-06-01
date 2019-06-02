from gameobjects import Cell, Road, Neutral, Capitalist, Socialist
from players import Player
import random


class Engine():
    """ Main game engine """

    def __init__(self):
        """ Setup game engine """
        # load level
        self.cells = {}
        for x in range(10):
            for y in range(10):
                self.cells[(x, y)] = Neutral((x, y))

        self.cells[(2, 2)] = Socialist((2, 2))
        self.cells[(3, 3)] = Road((3, 3))
        self.cells[(5, 5)] = Capitalist((5, 5))
        self.cells[(7, 7)] = Neutral((7, 7))

        Engine.build_boundary(self.cells)
        
        # initialise 2 players
        #player1_start_cell = random.choice(x for cells in self.cells.values)

        #while player1_start_cell.is_navigable is False:
        #    player1_start_cell = random.choice(self.cells)

        self.capitalist = Player([60, 60])

        #player2_start_cell = random.choice(x for cells in self.cells.values)

        #while player2_start_cell.is_navigable is False:
        #    player2_start_cell = random.choice(self.cells)

        self.socialist = Player([30, 30])

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

        self.capitalist.tick(p1_inputs, self.cells)
        self.socialist.tick(p2_inputs, self.cells)
        print(self.capitalist.get_grid_ref())

        for reference, cell in self.cells.items():
            cell.tick()
