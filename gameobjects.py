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
        self.is_navigable = is_navigable
        self.position = (grid_ref[0] * 60, grid_ref[1] * 60)
        self.rect = Rect(self.position, (59, 59))


    def tick(self):
        return


class Road(Cell):
    def __init__(self, grid_ref):
        super().__init__(grid_ref, is_navigable=True)


class Neutral(Cell):
    def __init__(self, grid_ref):
        self.owner = Owner.Neutral
        super().__init__(grid_ref, is_navigable=True)


class Capitalist(Cell):
    def __init__(self, grid_ref):
        self.owner = Owner.Capitalist
        super().__init__(grid_ref, is_navigable=False)


class Socialist(Cell):
    def __init__(self, grid_ref):
        self.owner = Owner.Socialist
        super().__init__(grid_ref, is_navigable=False)
