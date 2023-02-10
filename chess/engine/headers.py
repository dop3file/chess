from typing import NamedTuple
from enum import Enum


class Coordinates(NamedTuple):
    x: int
    y: int


class Move:
    def __init__(self, position: Coordinates, figure):
        self.position = position
        self.figure = figure


class Turn(Enum):
    white = -1
    black = 1


figure_ranks = {
    'pawn': 1,
    'knight': 2,
    'bishop': 3,
    'rook': 4,
    'queen': 5
}