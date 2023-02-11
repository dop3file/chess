from _test_utils import add_chess_module
from engine.board import Board
from engine.headers import Coordinates
import pytest


board = Board()
board.set_defautl_board()


def test_available_moves():
    knight = board.board[7][1]
    assert knight.get_available_moves() == [Coordinates(x=5, y=0), Coordinates(x=5, y=2)]


def test_available_moves():
    queen = board.board[0][3]
    assert queen.get_available_moves() == []


def test_available_moves():
    pawn = board.board[1][1]
    assert pawn.get_available_moves() == [Coordinates(x=2, y=1), Coordinates(x=3, y=1)]