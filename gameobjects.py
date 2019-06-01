""" Our game objects """
from controls import Inputs
from enum import Enum

class Headings(Enum):
    North = 0
    East = 1
    South = 2
    West = 3


class Owner(Enum):
    Player1 = 0
    Player2 = 1
    Neutral = 2


class Cell():
    def __init__(self):
        return

    def is_navigable(self):
        return True

    def tick(self):
        return


class Road(Cell):

    def is_navigable(self):
        return True


class Changeable(Cell):
    def __init__(self):
        self.owner = Owner.Neutral


class Player():
    """ represents a player """

    def __init__(self, position):
        """ 
        position: list [x,y]
        """
        self.position = position
        self._heading = Headings.North
        self._velocity = [0, 0]
        self._size = (15, 15) 

    def _damp(self):
        """ Decelerates x and y axis movement """
        self._velocity[0] = int(0.8 * self._velocity[0])
        self._velocity[1] = int(0.8 * self._velocity[1])

    def _move(self):
        self.position[0] += self._velocity[0]
        self.position[1] += self._velocity[1]

    def tick(self, inputs):
        self.handle_inputs(inputs)
        self._move()

    def handle_inputs(self, inputs):
        if inputs == [] or inputs == [Inputs.ACTION]:
            self._damp()
            return

        if Inputs.UP in inputs:
            self._velocity[1] -= 1
        if Inputs.RIGHT in inputs:
            self._velocity[0] += 1
        if Inputs.DOWN in inputs:
            self._velocity[1] += 1
        if Inputs.LEFT in inputs:
            self._velocity[0] -= 1

    