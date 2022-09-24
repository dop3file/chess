from board import Board
from headers import Coordinates


def main():
    board = Board()
    board.set_defautl_board()
    pow = board.board[6][0]
    pow.move(Coordinates(x=5, y=0))
    board.draw_board()

if __name__ == '__main__':
    main()