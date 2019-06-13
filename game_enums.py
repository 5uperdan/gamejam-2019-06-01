from enum import Enum


class Inputs(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    ACTION = 4


class GameState(Enum):
    QUIT = 0
    CAPITALIST_WIN = 1
    SOCIALIST_WIN = 2
    RUNNING = 3


class Headings(Enum):
    North = 0
    East = 1
    South = 2
    West = 3


class Team(Enum):
    Capitalist = 0
    Socialist = 1
    Neutral = 2


class Cell_Tick_Return(Enum):
    Completed = 1
    Destroyed = 2
    Other = 3