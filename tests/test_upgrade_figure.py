from _test_utils import add_chess_module
from engine.board import Board
from engine.headers import Coordinates
import pytest


board = Board()
board.set_defautl_board()


def test_upgrade_figure():
    pawn = board.board[6][3]
    pawn.move(
        Coordinates(x=4, y=3)
    )
    board.board[1][4].move(
        Coordinates(x=3, y=4)
    )
    pawn.move(
        Coordinates(x=3, y=4)
    )
    board.board[1][5].move(
        Coordinates(x=2, y=5)
    )
    pawn.move(
        Coordinates(x=2, y=5)
    )
    board.board[1][0].move(
        Coordinates(x=1, y=2)
    )
    pawn.move(
        Coordinates(x=1, y=6)
    )
    board.board[1][1].move(
        Coordinates(x=2, y=2)
    )
    pawn.move(
        Coordinates(x=0, y=7)
    )
    
    rock = board.board[0][7]
    assert rock.name == 'rook'