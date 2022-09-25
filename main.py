from board import Board, Pawn
from headers import Coordinates, Turn
from game import Game


def main():
    board = Board()
    board.set_defautl_board()
    rock = board.board[0][0]
    game = Game(board)
    game.draw_board()
    #board.draw_board()
    


if __name__ == '__main__':
    main()