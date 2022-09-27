from headers import board_width, board_height, Coordinates, Turn
from figure import Pawn, Rook, Knight, Bishop, Queen, King


class Board:
    def __init__(self):
        self.board = [[None for _ in range(board_width)] for _ in range(board_height)]
        self.turn = Turn.white.value
        self.dead_figures = []

    def set_defautl_board(self):
        self.board[6][:] = [Pawn(position=Coordinates(x=6, y=y_coordinate), board=self, type_=Turn.white.value) for y_coordinate in list(range(8))]
        self.board[1][:] = [Pawn(position=Coordinates(x=1, y=y_coordinate), board=self, type_=Turn.black.value) for y_coordinate in list(range(8))]
        
        self.board[0][0] = Rook(position=Coordinates(x=0,y=0), board=self, type_=Turn.black.value)
        self.board[0][7] = Rook(position=Coordinates(x=0,y=7), board=self, type_=Turn.black.value)
        self.board[7][0] = Rook(position=Coordinates(x=7,y=0), board=self, type_=Turn.white.value)
        self.board[7][7] = Rook(position=Coordinates(x=7,y=7), board=self, type_=Turn.white.value)
    
        self.board[0][1] = Knight(position=Coordinates(x=0, y=1), board=self, type_=Turn.black.value)
        self.board[0][6] = Knight(position=Coordinates(x=0, y=6), board=self, type_=Turn.black.value)
        self.board[7][1] = Knight(position=Coordinates(x=7, y=1), board=self, type_=Turn.white.value)
        self.board[7][6] = Knight(position=Coordinates(x=7, y=6), board=self, type_=Turn.white.value)

        self.board[0][2] = Bishop(position=Coordinates(x=0, y=2), board=self, type_=Turn.black.value)
        self.board[0][5] = Bishop(position=Coordinates(x=0, y=5), board=self, type_=Turn.black.value)
        self.board[7][2] = Bishop(position=Coordinates(x=7, y=2), board=self, type_=Turn.white.value)
        self.board[7][5] = Bishop(position=Coordinates(x=7, y=5), board=self, type_=Turn.white.value)

        self.board[0][3] = Queen(position=Coordinates(x=0, y=3), board=self, type_=Turn.black.value)
        self.board[7][3] = Queen(position=Coordinates(x=7, y=3), board=self, type_=Turn.white.value)

        self.board[0][4] = King(position=Coordinates(x=0, y=4), board=self, type_=Turn.black.value)
        self.board[7][4] = King(position=Coordinates(x=7, y=4), board=self, type_=Turn.white.value)

    def drag_figure(self, figure_coordinate: Coordinates, new_coordinate: Coordinates):
        self.board[new_coordinate.x][new_coordinate.y] = self.board[figure_coordinate.x][figure_coordinate.y]
        self.board[figure_coordinate.x][figure_coordinate.y] = None
        self.change_turn()

    def change_turn(self):
        self.turn = Turn.white.value if self.turn != Turn.white.value else Turn.black.value

    def draw_board(self):
        for el in self.board:
            for zel in el:
                text = '-' if zel is None else str(zel)[0]
                print(f'{text} ', end='')
            print('')