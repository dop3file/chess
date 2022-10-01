from board import Board, Pawn
from headers import Coordinates, Turn
from game import Game


def main():
    board = Board()
    board.set_defautl_board()
    game = Game(board)
    game.draw_board()


if __name__ == '__main__':
    main()