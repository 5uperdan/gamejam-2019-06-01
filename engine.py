from players import Capitalist, Socialist
import random
from cell_handler import Cell_Handler
from game_enums import GameState, Inputs, Team


class Engine():
    """ Main game engine """

    WINNING_SCORE = 5000

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
        self.cell_handler.tick(self.scores)

        # collisions between players and environment
        # we handle and correct for adjacent cells first because it usually gets
        # the desired effect without getting 'caught' on multiple blocks
        for player, p_grid in zip(self.players, starting_player_grids):
            adjacent_grids = Cell_Handler.get_adjacent_grids(p_grid)
            self.handle_environment_collisions(adjacent_grids, player, p_grid, player.team)
            diagonal_grids = Cell_Handler.get_diagonal_grids(p_grid)
            self.handle_environment_collisions(diagonal_grids, player, p_grid, player.team)

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
        if self.scores[Team.Capitalist] >= Engine.WINNING_SCORE:
            return GameState.CAPITALIST_WIN
        elif self.scores[Team.Socialist] >= Engine.WINNING_SCORE:
            return GameState.SOCIALIST_WIN

        return GameState.RUNNING

    def handle_environment_collisions(self, grids, player, p_starting_grid, p_team):
        """ handles environment collisions with a list of given grids """
        for grid in grids:
            cell = self.cell_handler.cells.get(grid, None)
            if cell is None or cell.is_navigable(p_team):
                continue
            elif player.rect.colliderect(cell.rect):
                player.correct_for_collision(p_starting_grid, cell)

    def get_score_completion(self, team):
        """ """
        return self.scores[team] / Engine.WINNING_SCORE
