from headers import board_width, board_height, Coordinates, Turn
from figure import Pawn, Rook


class Board:
    def __init__(self):
        self.board = [[None for _ in range(board_width)] for _ in range(board_height)]
        self.turn = Turn.white.value
        self.dead_figures = []

    def set_defautl_board(self):
        self.board[6][:] = [Pawn(position=Coordinates(x=6, y=y_coordinate), name='pawn', board=self, type_=Turn.white.value) for y_coordinate in list(range(8))]
        self.board[1][:] = [Pawn(position=Coordinates(x=1, y=y_coordinate), name='pawn', board=self, type_=Turn.black.value) for y_coordinate in list(range(8))]
        self.board[0][0] = Rook(position=Coordinates(x=0,y=0), name='rook', board=self, type_=Turn.black.value)
        self.board[0][7] = Rook(position=Coordinates(x=0,y=7), name='rook', board=self, type_=Turn.black.value)
        self.board[7][0] = Rook(position=Coordinates(x=7,y=0), name='rook', board=self, type_=Turn.white.value)
        self.board[7][7] = Rook(position=Coordinates(x=7,y=7), name='rook', board=self, type_=Turn.white.value)
   
    def drag_figure(self, figure_coordinate: Coordinates, new_coordinate: Coordinates):
        self.board[new_coordinate.x][new_coordinate.y] = self.board[figure_coordinate.x][figure_coordinate.y]
        self.board[figure_coordinate.x][figure_coordinate.y] = None
        self.turn = Turn.black.value if self.turn == Turn.white.value else Turn.white.value

    def draw_board(self):
        for el in self.board:
            for zel in el:
                text = '-' if zel is None else str(zel)[0]
                print(f'{text} ', end='')
            print('')