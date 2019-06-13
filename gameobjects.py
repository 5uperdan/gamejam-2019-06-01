""" Our game objects """
from pygame import Rect
import math
from game_enums import Team, Cell_Tick_Return


class Cell():
    def __init__(self, grid):
        """
        grid: tuple of grid location (x, y)
        """
        self.grid = grid
        self._size = (60, 60)
        self.position = (grid[0] * 60, grid[1] * 60)
        self.rect = Rect(self.position, self._size)

    @property
    def centre(self):
        """ returns centre position """
        return (self.position[0] + self._size[0] // 2,
                self.position[1] + self._size[1] // 2)

    @property
    def is_complete(self):
        return False

    def is_navigable(self, player_team):
        return False

    def tick(self, capitalist=None, socialist=None):
        return


class Road_Cell(Cell):
    def __init__(self, grid):
        super().__init__(grid)

    def is_navigable(self, player_team):
        return True


class Rock_Cell(Cell):
    def __init__(self, grid):
        super().__init__(grid)

    def is_navigable(self, player_team):
        return False


class Neutral_Cell(Cell):
    def __init__(self, grid):
        super().__init__(grid)

    def is_navigable(self, player_team):
        return True


class Captured_Cell(Cell):
    def __init__(self, grid, goal):
        self._progress = 0
        self.goal = goal
        self._is_complete = False
        self.is_hindered = False

        super().__init__(grid)

    @property
    def is_complete(self):
        return self._is_complete

    @property
    def is_destroyable(self):
        return self.progress < 0.5

    @property
    def progress(self):
        """ returns fraction of completeness (1 is complete) """
        return self._progress / self.goal

    def is_navigable(self, player_team):
        """ shouldn't be called """
        raise NotImplementedError()

    def tick(self):
        """ returns True if type complete """
        if self.is_complete:
            return Cell_Tick_Return.Other

        if self.is_hindered:
            self._progress -= 0.5
        else:
            self._progress += 0.5

        if self._progress >= self.goal:
            self._progress = self.goal
            self._is_complete = True
            return Cell_Tick_Return.Completed

        if self._progress <= 0:
            return Cell_Tick_Return.Destroyed

        return Cell_Tick_Return.Other


class Capitalist_Cell(Captured_Cell):
    def __init__(self, grid):
        super().__init__(grid, goal=600)

    def tick(self):
        return super().tick()

    def is_navigable(self, player_team):
        return False


class Socialist_Cell(Captured_Cell):
    def __init__(self, grid):
        super().__init__(grid, goal=400)

    def tick(self):
        return super().tick()

    def is_navigable(self, player_team):
        if player_team == Team.Capitalist:
            return False
        else:  # player_team == Team.Socialist:
            return True
