from gameobjects import Player, Cell
import random


class Engine():
    """ Main game engine """

    def __init__(self):
        """ Setup game engine """
        # initialise all game cells
        self.cells = {}
        for x, y in zip(range(10), range(10)):
            self.cells[(x, y)] = Cell()

        # initialise 2 players
        #player1_start_cell = random.choice(x for cells in self.cells.values)

        #while player1_start_cell.is_navigable is False:
        #    player1_start_cell = random.choice(self.cells)

        self.player1 = Player([60, 60])

        #player2_start_cell = random.choice(x for cells in self.cells.values)

        #while player2_start_cell.is_navigable is False:
        #    player2_start_cell = random.choice(self.cells)

        self.player2 = Player([30, 30])

    def tick(self, p1_inputs, p2_inputs):
        """ Progresses the game one tick forward """

        self.player1.tick(p1_inputs)
        self.player2.tick(p2_inputs)

        # handle action buttons
        # if action button pushed,
        # check player direction and action the adjacent cell in that direction
        # player direction button must be pushed

        for reference, cell in self.cells.items():
            cell.tick()
