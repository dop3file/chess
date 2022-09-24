from headers import board_width, board_height, Coordinates, Turn
from figure import Pawn


class Board:
    def __init__(self):
        self.board = [[None for _ in range(board_width)] for _ in range(board_height)]
        self.turn = Turn.white.value

    def set_defautl_board(self):
        self.board[6][:] = [Pawn(position=Coordinates(x=6, y=y_coordinate), name='pawn', board=self, type_=Turn.white.value) for y_coordinate in list(range(8))]
        #self.board[2][0] = Pawn(position=Coordinates(x=2, y=y_coordinate["a"]), name='pawn', board=self, type_=Turn.white.value)
        #self.board[5][0] = Pawn(position=Coordinates(x=4, y=y_coordinate["a"]), name='pawn', board=self, type_=Turn.black.value)
        self.board[1][:] = [Pawn(position=Coordinates(x=1, y=y_coordinate), name='pawn', board=self, type_=Turn.black.value) for y_coordinate in list(range(8))]

    def drag_figure(self, figure_coordinate: Coordinates, new_coordinate: Coordinates):
        self.board[new_coordinate.x][new_coordinate.y] = self.board[figure_coordinate.x][figure_coordinate.y]
        self.board[figure_coordinate.x][figure_coordinate.y] = None
        
    def draw_board(self):
        for el in self.board:
            for zel in el:
                text = '-' if zel is None else str(zel)[0]
                print(f'{text} ', end='')
            print('')