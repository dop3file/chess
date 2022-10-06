from collections import namedtuple
from enum import Enum


Coordinates = namedtuple("coordinates", ["x", "y"])

board_width = 8
board_height = 8

class Turn(Enum):
    white = -1
    black = 1

figures_ranks = {
    'pawn': 1,
    'knight': 3,
    'bishop': 4,
    'rook': 5,
    'queen': 6
}