""" Contains methods that deal with the cell collections """

from gameobjects import (Capitalist_Cell, Captured_Cell, Road_Cell,
                         Socialist_Cell, Neutral_Cell, Rock_Cell, Cell)
from game_enums import Team, Headings, Cell_Tick_Return


class Cell_Handler():
    """ Handles the cells that make up the game map """

    def __init__(self):
        self.cells = {}

        Cell_Handler.load_test_level(self.cells)
        Cell_Handler.build_boundary(self.cells)

    def tick(self, scores):
        """ 
        Args:
            scores: score dictionary
        """
        for _, cell in self.cells.items():
            cell_tick_rtrn = cell.tick()
            if cell_tick_rtrn == Cell_Tick_Return.Completed:
                if type(cell) is Capitalist_Cell:
                    scores[Team.Capitalist] += 1000
                elif type(cell) is Socialist_Cell:
                    scores[Team.Socialist] += 1000
            elif cell_tick_rtrn == Cell_Tick_Return.Destroyed:
                self.cells[cell.grid] = Neutral_Cell(cell.grid)

    def get_actionable_grid(self, p_grid, p_centre, p_team):
        """ Returns the grid location of the closest actionable grid
            If there is no actionable grid in range, returns None.
            Args:
                p_grid: player's grid
                p_centre: position of player's centre point
                p_team: enum
        """
        surrounding_grids = Cell_Handler.get_surrounding_grids(p_grid)
        player_x, player_y = p_centre
        min_sq_dist = 1_000_000  # any cell should be less distance away
        min_grid = None

        # opposing team's cell type can be hindered, your own may need repair
        opposing_type = Capitalist_Cell if p_team == Team.Socialist else Socialist_Cell
        friendly_type = Capitalist_Cell if p_team == Team.Capitalist else Socialist_Cell

        # select grids which are actionable
        for grid in surrounding_grids:
            candidate_cell = self.cells[grid]

            if candidate_cell.is_complete:
                continue

            if (type(candidate_cell) is Neutral_Cell or
               (type(candidate_cell) is opposing_type and not candidate_cell.is_hindered) or
               type(candidate_cell) is friendly_type and candidate_cell.is_hindered):

                # calculate distance between player centre and cell centre
                cell_x, cell_y = candidate_cell.centre
                sq_distance = (player_x - cell_x) ** 2 + (player_y - cell_y) ** 2

                # keep track of closest one
                if sq_distance < min_sq_dist:
                    min_sq_dist = sq_distance
                    min_grid = grid

        return min_grid

    def action_cell(self, grid, player_team):
        """ Actions a cell, returns True if energy is spent """
        if player_team == Team.Capitalist:
            return self._capitalise_cell(grid)
        else:  # player_team == Team.Socialist:
            return self._socialise_cell(grid)

    def _capitalise_cell(self, grid):
        """ capitalist player has actioned cell,
        returns True if energy was spent """
        cell = self.cells.get(grid, None)
        if cell is None:
            return False

        if type(cell) is Capitalist_Cell:
            self.cells[grid].is_hindered = False
            return True
        if type(cell) is Neutral_Cell:
            self.cells[grid] = Capitalist_Cell(grid)
            return True
        if type(cell) is Socialist_Cell:
            self.cells[grid].is_hindered = True
            return True

    def _socialise_cell(self, grid):
        """ socialist player has actioned cell,
        returns True if energy was spent """
        cell = self.cells.get(grid, None)
        if cell is None:
            return False

        if type(cell) is Socialist_Cell:
            self.cells[grid].is_hindered = False
            return True
        if type(cell) is Neutral_Cell:
            self.cells[grid] = Socialist_Cell(grid)
            return True
        if type(cell) is Capitalist_Cell:
            self.cells[grid].is_hindered = True
            return True

    @staticmethod
    def get_surrounding_grids(grid, include_occupied=False):
        """ Returns a list of tuples [(x,y) ...]
            which are the surrounding grid refs.
            If include_occupied is True then the occupied grid is included
            in the list.
            """
        surrounding_grids = Cell_Handler.get_adjacent_grids(grid)
        surrounding_grids += Cell_Handler.get_diagonal_grids(grid)
        if include_occupied:
            surrounding_grids.append(grid)
        return surrounding_grids

    @staticmethod
    def get_adjacent_grids(grid):
        """ Returns a list of tuples [(x,y) ...]
            which are the adjacent grid refs.
        """
        return [
            Cell_Handler.grid_navigation(grid, [Headings.North]),
            Cell_Handler.grid_navigation(grid, [Headings.East]),
            Cell_Handler.grid_navigation(grid, [Headings.South]),
            Cell_Handler.grid_navigation(grid, [Headings.West])
            ]

    @staticmethod
    def get_diagonal_grids(grid):
        """ Returns a list of tuples [(x,y) ...]
            which are the diagonal grid refs.
        """
        return [
            Cell_Handler.grid_navigation(grid, [Headings.North, Headings.East]),
            Cell_Handler.grid_navigation(grid, [Headings.South, Headings.East]),
            Cell_Handler.grid_navigation(grid, [Headings.South, Headings.West]),
            Cell_Handler.grid_navigation(grid, [Headings.North, Headings.West])
            ]

    @staticmethod
    def grid_navigation(grid, headings):
        """ returns a grid reference after navigating according to the
            headings list, a list of Enums.
        """
        x, y = grid
        if Headings.North in headings:
            y -= 1
        if Headings.East in headings:
            x += 1
        if Headings.South in headings:
            y += 1
        if Headings.West in headings:
            x -= 1

        return x, y


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
        for grid in [(0, 0)]:
            cells[grid] = Socialist_Cell(grid)
            Cell_Handler.make_cell_socialist_respawner(cells[grid])
        #for grid in [(9, 5), (2, 8)]:
        #    cells[grid] = Capitalist_Cell(grid)
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

    @staticmethod
    def make_cell_socialist_respawner(cell):
        """ give the cell the properties of a socialist respawning cell """
        cell._is_complete = True
        cell._progress = cell.goal
