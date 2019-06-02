""" Our game objects """
from enum import Enum
from pygame import Rect
import math


class Owner(Enum):
    Capitalist = 0
    Socialist = 1
    Neutral = 2


class Cell():
    def __init__(self, grid_ref, is_navigable=True):
        """
        grid: tuple of grid_ref location (x, y)
        """
        self.grid = grid_ref
        self._size = (60, 60)
        self.is_navigable = is_navigable
        self.position = (grid_ref[0] * 60, grid_ref[1] * 60)
        self.rect = Rect(self.position, self._size)

    def tick(self):
        return


class Road_Cell(Cell):
    def __init__(self, grid_ref):
        super().__init__(grid_ref, is_navigable=True)


class Neutral_Cell(Cell):
    def __init__(self, grid_ref):
        self.owner = Owner.Neutral
        super().__init__(grid_ref, is_navigable=True)


class Capturable_Cell(Cell):
    def __init__(self, grid_ref, goal):
        self.progress = 0
        self.goal = goal
        self.is_complete = False
        self.is_hindered = False

        super().__init__(grid_ref, is_navigable=False)

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


class Capitalist_Cell(Capturable_Cell):
    def __init__(self, grid_ref):
        self.owner = Owner.Capitalist

        super().__init__(grid_ref, goal=2000)


class Socialist_Cell(Capturable_Cell):
    def __init__(self, grid_ref):
        self.owner = Owner.Socialist
        super().__init__(grid_ref, goal=1000)
