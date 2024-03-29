from engine.headers import Coordinates, Turn
from engine.figure import Pawn, Rook, Knight, Bishop, Queen, King
from engine.utils import check_diagonal_line, check_vertical_line, check_horizontal_line
from engine.figure import Figure

import config


class Board:
    def __init__(self):
        self.board = [[None for _ in range(config.BOARD_WIDTH)] for _ in range(config.BOARD_HEIGHT)]
        self.turn = Turn.white.value
        self.dead_figures = []
        self.count_turn = 0
        self.check_turn = None
        self.is_check_mate = False

    def set_defautl_board(self) -> None:
        self.board[6][:] = [Pawn(position=Coordinates(x=6, y=y_coordinate), board=self, type_=Turn.white.value) for y_coordinate in list(range(config.BOARD_WIDTH))]
        self.board[1][:] = [Pawn(position=Coordinates(x=1, y=y_coordinate), board=self, type_=Turn.black.value) for y_coordinate in list(range(config.BOARD_WIDTH))]
        
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

    def is_king_cell(self, coordinates: Coordinates) -> bool:
        if (cell := self.board[coordinates.x][coordinates.y]) and cell.name == 'king':
            return True
        return False

    def verify_move_availability(self, figure: Figure, new_coordinate: Coordinates) -> bool:
        if self.check_turn == self.turn and new_coordinate not in self.get_available_moves_without_stalemate():
            return False

        if self.is_king_cell(new_coordinate):
            return False

        return True

    def drag_figure(self, figure: Figure, new_coordinate: Coordinates, is_castling=False) -> None:
        if not self.verify_move_availability(figure, new_coordinate):
            return

        old_position = figure.position
        old_cell = self.board[new_coordinate.x][new_coordinate.y]
        
        self.board[new_coordinate.x][new_coordinate.y] = self.board[figure.position.x][figure.position.y]
        self.board[figure.position.x][figure.position.y] = None
        figure.position = new_coordinate

        if self.verify_check(self.board) and self.turn == self.verify_check(self.board).type_:
            self.board[old_position.x][old_position.y] = figure
            self.board[new_coordinate.x][new_coordinate.y] = old_cell
            if old_cell is not None:
                old_cell.position = new_coordinate
            figure.position = old_position
            
        else:
            if old_cell is not None:
                self.dead_figures.append(old_cell)
            self.change_turn()

            self.check_turn = self.turn if self.verify_check(self.board) else None
            self.count_turn += 1

        if not self.get_available_moves_without_stalemate():
            self.is_check_mate = True
        
    def change_turn(self) -> None:
        self.turn = Turn.white.value if self.turn != Turn.white.value else Turn.black.value

    def verify_check(self, board: list[list]) -> Figure | None:
        '''
        Метод возвращает короля под шахом если такой имеется
        '''
        kings = [figure for line in board for figure in line if figure and figure.name == 'king']
        for king in kings:
            figures = [figure_ for line in board for figure_ in line if figure_ and figure_.type_ != king.type_]
            for figure_ in figures:
                match figure_.name:
                    case 'knight':
                        if king.position in figure_.get_available_moves():
                            return king
                    case 'bishop':
                        available_moves = [
                            check_diagonal_line(board, figure_, True), 
                            check_diagonal_line(board, figure_, False)
                        ]
                        for moves in available_moves:
                            if king.position in moves:
                                return king
                    case 'rook':
                        available_moves = [
                            check_horizontal_line(board, figure_, True), 
                            check_horizontal_line(board, figure_, False),
                            check_vertical_line(board, figure_, True), 
                            check_vertical_line(board, figure_, False)
                        ]
                        for moves in available_moves:
                            if king.position in moves:
                                return king
                    case 'queen':
                        available_moves = [
                            check_diagonal_line(board, figure_, True), 
                            check_diagonal_line(board, figure_, False), 
                            check_vertical_line(board, figure_, True), 
                            check_vertical_line(board, figure_, False), 
                            check_horizontal_line(board, figure_, True), 
                            check_horizontal_line(board, figure_, False)
                        ]
                        for moves in available_moves:
                            if king.position in moves:
                                return king

                    case 'pawn':
                        if king.position in figure_.get_available_moves() and figure_.position.y != king.position.y:
                            return king

                    case 'king':
                        for moves in figure_.get_available_moves():
                            if king.position in moves:
                                return king
        
    def get_available_moves_without_stalemate(self, select_figure: Figure = None) -> list[Coordinates]:
        available_moves = []

        iter_target = [figure_ for line in self.board for figure_ in line if figure_ and figure_.type_ == self.turn] if select_figure is None else [select_figure]

        for figure in iter_target:
            for move_coord in figure.get_available_moves():
                old_position = figure.position
                old_cell = self.board[move_coord.x][move_coord.y]
                figure.move(move_coord, is_check_call=True)
                if self.verify_check(self.board) is None or self.verify_check(self.board).type_ != self.turn:
                    available_moves.append(move_coord)
                figure.move(old_position, is_check_call=True)
                self.board[move_coord.x][move_coord.y] = old_cell
                self.board[old_position.x][old_position.y] = figure
                figure.position = old_position
                
        return available_moves

    def get_figure_name(self, name: str) -> Figure:
        figures = {
            'pawn': Pawn,
            'rook': Rook,
            'king': King,
            'queen': Queen,
            'knight': Knight,
            'bishop': Bishop
        }
        return figures[name]
