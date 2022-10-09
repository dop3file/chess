import copy
from headers import board_width, board_height, Coordinates, Turn
from figure import Pawn, Rook, Knight, Bishop, Queen, King
from utils import check_diagonal_line, check_vertical_line, check_horizontal_line


class Board:
    def __init__(self):
        self.board = [[None for _ in range(board_width)] for _ in range(board_height)]
        self.turn = Turn.white.value
        self.dead_figures = []
        self.count_turn = 0
        self.check_turn = None
        self.is_check_mate = None

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

    def drag_figure(self, figure, new_coordinate: Coordinates):
        if self.check_turn == self.turn and new_coordinate not in self.get_available_moves_without_stalemate():
            return

        self.board[new_coordinate.x][new_coordinate.y] = self.board[figure.position.x][figure.position.y]
        self.board[figure.position.x][figure.position.y] = None
        figure.position = new_coordinate
        self.change_turn()
        self.check_turn = self.turn if self.verify_check(self.board) else None
        self.count_turn += 1

        if not self.get_available_moves_without_stalemate():
            print("Мат")
            self.is_check_mate = True
        
    def change_turn(self):
        self.turn = Turn.white.value if self.turn != Turn.white.value else Turn.black.value

    def verify_check(self, board):
        kings = [figure for line in board for figure in line if figure and figure.name == 'king']
        for king in kings:
            figures = [figure_ for line in board for figure_ in line if figure_ and figure_.type_ != king.type_]
            for figure_ in figures:
                if figure_.name == 'knight':
                    if Coordinates(x=king.position.x, y=king.position.y) in figure_.get_available_moves():
                        return True
                if figure_.name == 'bishop':
                    available_moves = [
                        check_diagonal_line(board, figure_, True), 
                        check_diagonal_line(board, figure_, False)
                    ]
                    for moves in available_moves:
                        if Coordinates(x=king.position.x, y=king.position.y) in moves:
                            return True
                if figure_.name == 'rook':
                    available_moves = [
                        check_horizontal_line(board, figure_, True), 
                        check_horizontal_line(board, figure_, False),
                        check_vertical_line(board, figure_, True), 
                        check_vertical_line(board, figure_, False)
                    ]
                    for moves in available_moves:
                        if Coordinates(x=king.position.x, y=king.position.y) in moves:
                            return True
                if figure_.name == 'queen':
                    available_moves = [
                        check_diagonal_line(board, figure_, True), 
                        check_diagonal_line(board, figure_, False), 
                        check_vertical_line(board, figure_, True), 
                        check_vertical_line(board, figure_, False), 
                        check_horizontal_line(board, figure_, True), 
                        check_horizontal_line(board, figure_, False)
                    ]
                    for moves in available_moves:
                        if Coordinates(x=king.position.x, y=king.position.y) in moves:
                            return True
                if figure_.name == 'pawn':
                    if Coordinates(x=king.position.x, y=king.position.y) in figure_.get_available_moves() and figure_.position.y != king.position.y:
                        return True
        return False
        
    def get_available_moves_without_stalemate(self):
        new_board = Board()
        new_board.board = self.board
        available_moves = []

        for figure in [figure_ for line in self.board for figure_ in line if figure_ and figure_.type_ == self.turn]:
            for move_coord in figure.get_available_moves():
                old_position = figure.position
                old_cell = self.board[move_coord.x][move_coord.y]
                figure.move(move_coord, is_check_call=True)
                if not self.verify_check(self.board):
                    available_moves.append(move_coord)
                figure.move(old_position, is_check_call=True)
                self.board[move_coord.x][move_coord.y] = old_cell
                self.board[old_position.x][old_position.y] = figure
                figure.position = old_position

        print(available_moves)
        return available_moves
        
    def draw_board(self):
        for el in self.board:
            for zel in el:
                text = '-' if zel is None else str(zel)[0]
                print(f'{text} ', end='')
            print('')

    def roll_board(self):
        ...
        # self.board = self.board[::-1]
        # for line_index, line in enumerate(self.board):
        #     for cell_index, cell in enumerate(line):
        #         if cell:
        #             cell.postion = Coordinates(x=line_index, y=cell_index)
        #             cell.type_ = Turn.white.value if cell.type_ == Turn.black.value else Turn.black.value
