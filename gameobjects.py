""" Our game objects """
from pygame import Rect
import math
from game_enums import Team


class Cell():
    def __init__(self, grid_ref):
        """
        grid: tuple of grid_ref location (x, y)
        """
        self.grid = grid_ref
        self._size = (60, 60)
        self.position = (grid_ref[0] * 60, grid_ref[1] * 60)
        self.rect = Rect(self.position, self._size)

    def is_navigable(self, player_team):
        return False

    def tick(self, capitalist=None, socialist=None):
        return


class Road_Cell(Cell):
    def __init__(self, grid_ref):
        super().__init__(grid_ref)

    def is_navigable(self, player_team):
        return True


class Rock_Cell(Cell):
    def __init__(self, grid_ref):
        super().__init__(grid_ref)

    def is_navigable(self, player_team):
        return False


class Neutral_Cell(Cell):
    def __init__(self, grid_ref):
        super().__init__(grid_ref)

    def is_navigable(self, player_team):
        return True


class Captured_Cell(Cell):
    def __init__(self, grid_ref, goal):
        self.progress = 0
        self.goal = goal
        self.is_complete = False
        self.is_hindered = False

        super().__init__(grid_ref)

    def is_navigable(self, player_team):
        """ shouldn't be called """
        raise NotImplementedError()

    def get_progress(self):
        """ returns fraction of completeness (1 is complete) """
        return self.progress / self.goal

    def tick(self):
        if self.is_complete:
            return
        if self.is_hindered:
            self.progress += 1
        else:
            self.progress += 2

        if self.progress >= self.goal:
            self.progress = self.goal
            self.is_complete = True


class Capitalist_Cell(Captured_Cell):
    def __init__(self, grid_ref):
        super().__init__(grid_ref, goal=2000)

    def tick(self):
        super().tick()

    def is_navigable(self, player_team):
        return False


class Socialist_Cell(Captured_Cell):
    def __init__(self, grid_ref):
        super().__init__(grid_ref, goal=1000)

    def tick(self):
        super().tick()

    def is_navigable(self, player_team):
        if player_team == Team.Capitalist:
            return False
        else:  # player_team == Team.Socialist:
            return True
