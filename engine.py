from players import Capitalist, Socialist
import random
from cell_handler import Cell_Handler
from game_enums import GameState, Inputs

class Engine():
    """ Main game engine """

    def __init__(self):
        """ Setup game engine """
        self.cell_handler = Cell_Handler()

        self.socialists = [Socialist([75, 75])]
        self.capitalists = [Capitalist([550, 75])]
        self.players = self.socialists + self.capitalists



    def tick(self, p1_inputs, p2_inputs, p3_inputs=None, p4_inputs=None):
        """ Progresses the game one tick forward """
        all_inputs = (p1_inputs, p2_inputs, p3_inputs, p4_inputs)

        # get player's starting grid references before they move
        players_grid_refs = [player.grid_ref for player in self.players]

        # handle action requests from players
        for player, inputs in zip(self.players, all_inputs):
            if Inputs.ACTION in inputs:
                handle_action_input(player)

        # apply a tick to each player
        for player, inputs in zip(self.players, all_inputs):
            player.tick(inputs)

        # apply tick to cells in gameplay area
        self.cell_handler.tick()

        # collisions between players and environment
        for player, p_grid_ref in zip(self.players, players_grid_refs):
            unnav_sur_cells = self.cell_handler.get_surrounding_unnavigable_cells(
                p_grid_ref, player.team)
            for cell in unnav_sur_cells:
                if player.rect.colliderect(cell.rect):
                    player.correct_for_collision(p_grid_ref, cell.grid)

        # collisions between opposing players
        for socialist in self.socialists:
            for capitalist in self.capitalists:
                if socialist.rect.colliderect(capitalist):
                    socialist.killed()
                    capitalist.score += 200

        # collisions between friendly players
        if len(self.socialists) > 1:
            # do something
            pass

        # check for win conditions
        #if self.capitalist.score >= 1000:
        #    return GameState.CAPITALIST_WIN

        #if self.socialist.score >= 1000:
        #    return GameState.SOCIALIST_WIN

        return GameState.RUNNING


    def handle_actions():
        for grid_ref in target_grid_refs:
            if self.energy > 150:
                if capitalise_cell(cells, grid_ref):
                    self.energy -= 150

        for grid_ref in target_grid_refs:
            if self.energy > 100:
                if socialise_cell(cells, grid_ref):
                    self.energy -= 100


    def handle_action_input(self, player_grid_ref, opponent_grid_ref, cells):
        target_grid_refs = Player.get_target_grid_refs(
            player_grid_ref,
            self.headings)
        if opponent_grid_ref in target_grid_refs:
            target_grid_refs.remove(opponent_grid_ref)

        self.action(cells, target_grid_refs=target_grid_refs)