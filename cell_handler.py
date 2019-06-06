""" Contains methods that deal with the cell collections """

from gameobjects import (Capitalist_Cell, Captured_Cell, Road_Cell,
                         Socialist_Cell, Neutral_Cell, Rock_Cell, Cell)
from game_enums import Team


class Cell_Handler():
    """ Handles the cells that make up the game map """

    def __init__(self):
        self.cells = {}

        Cell_Handler.load_test_level(self.cells)
        Cell_Handler.build_boundary(self.cells)

    def tick(self):
        for _, cell in self.cells.items():
            cell.tick()

    def get_target_grid_refs(grid_ref, headings):
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

    @staticmethod
    def get_surrounding_grid_refs(grid_ref):
        """ Returns a list of tuples [(x,y) ...]
            which are the surrounding grid refs """
        surrounding_grids = []
        for x in (-1, 0, 1):
            for y in (-1, 0, 1):
                if (x, y) != (0, 0):
                    surrounding_grids.append((grid_ref[0] + x, grid_ref[1] + y))
        return surrounding_grids

    def get_surrounding_unnavigable_cells(self, grid_ref, player_team):
        """ returns a list of cells surrounding the grid_ref
            and are unnavigable
            grid_ref: tuple
            player_team: Team(Enum)
        """
        surrounding_grids = Cell_Handler.get_surrounding_grid_refs(grid_ref)
        unnav_sur_cells = []
        for cell in unnav_sur_cells:
            candidate_cell = self.cells[candidate_grid_ref]

            if not candidate_cell.is_navigable(player_team):
                surrounding_cells.append(candidate_cell)
        return unnav_sur_cells

    def action_cell(grid_ref, player_team):
        """ Actions a cell """
        if player_team == Team.Capitalist:
            _capitalise_cell(grid_ref)
        else:  # player_team == Team.Socialist:
            _socialise_cell(grid_ref)

    def _capitalise_cell(grid_ref):
        """ capitalist player has actioned cell,
        returns True if energy was spent """
        cell = self.cells.get(target_grid_ref, None)
        if cell is None:
            return False

        if type(cell) is Capitalist_Cell:
            return False
        if type(cell) is Neutral_Cell:
            cells[target_grid_ref] = Capitalist_Cell(target_grid_ref)
            return True
        if type(cell) is Socialist_Cell:
            cell.is_hindered = True
            return True

    def _socialise_cell(grid_ref):
        """ capitalisation player has actioned cell,
        returns True if energy was spent """
        cell = self.cells.get(target_grid_ref, None)
        if cell is None:
            return False

        if type(cell) is Socialist_Cell:
            return False
        if type(cell) is Neutral_Cell:
            cells[target_grid_ref] = Socialist_Cell(target_grid_ref)
            return True
        if type(cell) is Capitalist_Cell:
            cell.is_hindered = True
            return True

    @staticmethod
    def build_boundary(cells):
        """ builds a boundary around the gameplay area """
        # left and right boundary columns
        for x in (-1, 10):
            for y in range(-1, 11):
                cells[(x, y)] = Cell((x, y))

        # top and bottom boundary columns
        for x in range(10):
            for y in (-1, 10):
                cells[(x, y)] = Cell((x, y))

    @staticmethod
    def load_test_level(cells):
        """ fills dictionary with cells """
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
