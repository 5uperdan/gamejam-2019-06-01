""" Our game objects """
from enum import Enum
from pygame import Rect
import math


class Owner(Enum):
    Capitalist = 0
    Socialist = 1
    Neutral = 2


class Cell():
    def __init__(self, grid, is_navigable=True):
        """
        grid: tuple of grid location (x, y)
        """
        self.grid = grid
        self.is_navigable = is_navigable
        self.position = (grid[0] * 60, grid[1] * 60)
        self.rect = Rect(self.position,
                        (self.position[0] + 59, self.position[1] + 59))


    def tick(self):
        return


class Road(Cell):
    def __init__(self, grid):
        super().__init__(grid, is_navigable=True)


class Neutral(Cell):
    def __init__(self, grid):
        self.owner = Owner.Neutral
        super().__init__(grid, is_navigable=True)


class Capitalist(Cell):
    def __init__(self, grid):
        self.owner = Owner.Capitalist
        super().__init__(grid, is_navigable=False)


class Socialist(Cell):
    def __init__(self, grid):
        self.owner = Owner.Socialist
        super().__init__(grid, is_navigable=False)

