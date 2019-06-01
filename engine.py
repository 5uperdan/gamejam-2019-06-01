from gameobjects import Road, Neutral, Capitalist, Socialist
from players import Player
import random


class Engine():
    """ Main game engine """

    def __init__(self):
        """ Setup game engine """
        # initialise all game cells
        self.cells = {}
        for x in range(10):
            for y in range(10):
                self.cells[(x, y)] = Neutral((x, y))

        self.cells[(2, 2)] = Socialist((2, 2))
        self.cells[(3, 3)] = Road((3, 3))
        self.cells[(5, 5)] = Capitalist((5, 5))
        self.cells[(7, 7)] = Neutral((7, 7))

        # initialise 2 players
        #player1_start_cell = random.choice(x for cells in self.cells.values)

        #while player1_start_cell.is_navigable is False:
        #    player1_start_cell = random.choice(self.cells)

        self.capitalist = Player([60, 60])

        #player2_start_cell = random.choice(x for cells in self.cells.values)

        #while player2_start_cell.is_navigable is False:
        #    player2_start_cell = random.choice(self.cells)

        self.socialist = Player([30, 30])

    def tick(self, p1_inputs, p2_inputs):
        """ Progresses the game one tick forward """

        # player only needs to know about the cell they are in and adjacent ones
        # to check for collision.
        self.capitalist.tick(p1_inputs, self.cells)
        self.socialist.tick(p2_inputs, self.cells)

        for reference, cell in self.cells.items():
            cell.tick()
