from typing import NamedTuple
from enum import Enum


class Coordinates(NamedTuple):
    x: int
    y: int


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