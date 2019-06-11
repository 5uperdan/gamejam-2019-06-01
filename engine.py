from players import Capitalist, Socialist
import random
from cell_handler import Cell_Handler
from game_enums import GameState, Inputs, Team


class Engine():
    """ Main game engine """

    def __init__(self):
        """ Setup game engine """
        self.cell_handler = Cell_Handler()

        self.socialists = [Socialist([75, 75])]
        self.capitalists = [Capitalist([550, 75])]
        self.players = self.socialists + self.capitalists
        self.scores = {Team.Capitalist: 0, Team.Socialist: 0}

    def tick(self, p1_inputs, p2_inputs, p3_inputs=None, p4_inputs=None):
        """ Progresses the game one tick forward """
        all_inputs = (p1_inputs, p2_inputs, p3_inputs, p4_inputs)

        # get player's starting grid references before they move
        starting_player_grids = [player.grid for player in self.players]

        # handle action requests from players
        for player, inputs in zip(self.players, all_inputs):
            if (Inputs.ACTION in inputs and
               player.meets_action_requirements):
                    result = self.cell_handler.action_cell(player.target, player.team)
                    if result:
                        player.action_completed()

        # apply a tick to each player
        for player, inputs in zip(self.players, all_inputs):
            player.tick(inputs)

        # apply tick to cells in gameplay area
        self.cell_handler.tick()

        # collisions between players and environment
        for player, p_grid in zip(self.players, starting_player_grids):
            unnav_sur_cells = self.cell_handler.get_surrounding_unnavigable_cells(
                p_grid, player.team)
            for cell in unnav_sur_cells:
                if player.rect.colliderect(cell.rect):
                    player.correct_for_collision(p_grid, cell)

        # collisions between opposing players
        for socialist in self.socialists:
            for capitalist in self.capitalists:
                if socialist.rect.colliderect(capitalist):
                    socialist.killed()
                    self.scores[Team.Capitalist] += 500

        # collisions between friendly players
        if len(self.socialists) > 1:
            # do something
            pass

        # set players' target grid
        for player in self.players:
            target = self.cell_handler.get_actionable_grid(
                player.grid,
                player.centre,
                player.team)
            player.set_target(target)

        # check for win conditions
        if self.scores[Team.Capitalist] >= 1000:
            return GameState.CAPITALIST_WIN
        elif self.scores[Team.Socialist] >= 1000:
            return GameState.SOCIALIST_WIN

        return GameState.RUNNING
