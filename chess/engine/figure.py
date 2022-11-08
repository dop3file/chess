from abc import ABC, abstractmethod
import math
from engine.headers import Coordinates, Turn, figures_ranks
from engine.utils import check_horizontal_line, check_vertical_line, check_diagonal_line
                  


class Figure(ABC):
    def __init__(self, position: Coordinates, board, type_):
        self.position = position
        self.name = self.__class__.__name__.lower()
        self.board = board
        self.type_ = type_
    def move(self, position: Coordinates, is_check_call=False):
        if position in self.get_available_moves() or is_check_call:                
            if is_check_call:
                self.board.board[position.x][position.y] = self.board.board[self.position.x][self.position.y]
                self.board.board[self.position.x][self.position.y] = None
                self.position = position
            else:
                self.board.drag_figure(self, position)

    @abstractmethod
    def get_available_moves(self):
        pass

    def __repr__(self):
        return f'{self.name} x={self.position.x} y={self.position.y} {"black" if self.type_ == Turn.black.value else "white"}'

    def __str__(self):
        return f'{self.name} {self.position} {"black" if self.type_ == Turn.black.value else "white"}'


class Pawn(Figure):
    def __init__(self, position, board, type_):
        super().__init__(
            position=position,
            board=board,
            type_=type_
        )
        self.default_position = position

    def move(self, position, is_check_call=False):
        if position in self.get_available_moves() or is_check_call:
            if position.y != self.position.y:
                self.kill_figure(position, is_check_call)
            else:
                if is_check_call:
                    self.board.board[position.x][position.y] = self.board.board[self.position.x][self.position.y]
                    self.board.board[self.position.x][self.position.y] = None
                    self.position = position
                else:
                    self.board.drag_figure(self, position)

            if (self.type_ == Turn.white.value and self.position.x == 0) or (self.type_ == Turn.black.value and self.position.x == 7):
                self.upgrade_figure()

    def upgrade_figure(self):
        new_figure_name = None
        for name, rank in figures_ranks.items():
            if name in [figure.name for figure in self.board.dead_figures]:
                new_figure_name = name
                
        if new_figure_name is not None:
            self.board.board[self.position.x][self.position.y] = None

        match new_figure_name:
            case 'knight':
                self.board.board[self.position.x][self.position.y] = Knight(position=self.position, board=self.board, type_=self.type_)
            case 'bishop':
                self.board.board[self.position.x][self.position.y] = Bishop(position=self.position, board=self.board, type_=self.type_)
            case 'rook':
                self.board.board[self.position.x][self.position.y] = Rook(position=self.position, board=self.board, type_=self.type_)
            case 'queen':
                self.board.board[self.position.x][self.position.y] = Queen(position=self.position, board=self.board, type_=self.type_)
        

    def get_available_moves(self):
        available_moves = []
        
        if self.position.x not in (0, 7):
            front_cell = (self.board.board[(x := self.position.x + (1 * self.type_))][(y := self.position.y)])

            # проверяем есть ли перед пешкой другая фигура
            if front_cell is None:
                available_moves.append(Coordinates(x=x, y=y))

            if self.position == self.default_position and (self.board.board[(x := self.position.x + (2 * self.type_))][self.position.y]) == None and front_cell == None:
                available_moves.append(Coordinates(x=x, y=y))

            if self.position.y != 7:
                if (cell := self.board.board[(x := self.position.x + (1 * self.type_))][(y := self.position.y + 1)]) is not None:
                    if cell.type_ != self.type_:
                        available_moves.append(Coordinates(x=x, y=y))
            
            if self.position.y != 0:
                if (cell := self.board.board[(x := self.position.x + (1 * self.type_))][(y := self.position.y - 1)]) is not None:
                    if cell.type_ != self.type_:
                        available_moves.append(Coordinates(x=x, y=y))

        return available_moves

    def kill_figure(self, position: Coordinates, is_check_call=False):
        if (piece := self.board.board[position.x][position.y]) and piece.type_ != self.type_:
            if is_check_call:
                self.board.board[position.x][position.y] = self.board.board[self.position.x][self.position.y]
                self.board.board[self.position.x][self.position.y] = None
                self.position = position
            else:
                self.board.drag_figure(self, position)
            


class Rook(Figure):
    def __init__(self, position, board, type_):
        super().__init__(
            position=position,
            board=board,
            type_=type_
        )
        
    def move(self, position, is_check_call=False):
        super().move(position, is_check_call)

    def castling(self, king_position):
        if king_position.y > self.position.y:
            self.board.drag_figure(self, Coordinates(x=self.position.x, y=self.position.y + 2 if abs(self.position.y - king_position.y) == 3 else self.position.y + 3))
        else:
            self.board.drag_figure(self, Coordinates(x=self.position.x, y=self.position.y - 2 if abs(self.position.y - king_position.y) == 3 else self.position.y - 3))

    def get_available_moves(self):
        available_moves = []
        available_moves.extend(check_horizontal_line(self.board.board, self, True))
        available_moves.extend(check_horizontal_line(self.board.board, self, False))
        available_moves.extend(check_vertical_line(self.board.board, self, True))
        available_moves.extend(check_vertical_line(self.board.board, self, False))

        return available_moves


class Knight(Figure):
    def __init__(self, position, board, type_):
        super().__init__(
            position=position,
            board=board,
            type_=type_
        )
        
    def move(self, position, is_check_call=False):
        super().move(position, is_check_call)

    def get_available_moves(self):
        '''
        Функция возвращает возможные ходы в виде буквы Г(для коня)
        '''
        available_moves = []
        available_coords = [
            [self.position.x - 2, self.position.y - 1],
            [self.position.x - 2, self.position.y + 1],
            [self.position.x + 2, self.position.y + 1],
            [self.position.x + 2, self.position.y - 1],
            [self.position.x - 1, self.position.y - 2],
            [self.position.x - 1, self.position.y - 2],
            [self.position.x + 1, self.position.y - 2],
            [self.position.x - 1, self.position.y + 2],
            [self.position.x + 1, self.position.y + 2]
        ]
        for x, y in available_coords:
            if 0 <= x < 8 and 0 <= y < 8 and (self.board.board[x][y] is None or (self.board.board[x][y].type_ != self.type_)):
                available_moves.append(Coordinates(x=x, y=y))
                
        return available_moves


class Bishop(Figure):
    def __init__(self, position, board, type_):
        super().__init__(
            position=position,
            board=board,
            type_=type_
        )
        
    def move(self, position, is_check_call=False):
        super().move(position, is_check_call)

    def get_available_moves(self):
        available_moves = []
        available_moves.extend(check_diagonal_line(self.board.board, self, True))
        available_moves.extend(check_diagonal_line(self.board.board, self, False))

        return available_moves


class Queen(Figure):
    def __init__(self, position, board, type_):
        super().__init__(
            position=position,
            board=board,
            type_=type_
        )
        
    def move(self, position, is_check_call=False):
        super().move(position, is_check_call)

    def get_available_moves(self):
        available_moves = []

        available_moves.extend(check_diagonal_line(self.board.board, self, True))
        available_moves.extend(check_diagonal_line(self.board.board, self, False))
        available_moves.extend(check_horizontal_line(self.board.board, self, True))
        available_moves.extend(check_horizontal_line(self.board.board, self, False))
        available_moves.extend(check_vertical_line(self.board.board, self, True))
        available_moves.extend(check_vertical_line(self.board.board, self, False))

        return available_moves


class King(Figure):
    def __init__(self, position, board, type_):
        super().__init__(
            position=position,
            board=board,
            type_=type_
        )
        self.is_moved = False
        
    def move(self, position, is_check_call=False):
        if position in self.get_available_moves() or is_check_call:                
            if is_check_call:
                self.board.board[position.x][position.y] = self.board.board[self.position.x][self.position.y]
                self.board.board[self.position.x][self.position.y] = None
                self.position = position
            else:
                if (potential_rook := self.board.board[position.x][position.y]) and potential_rook.name == 'rook' and potential_rook.type_ == self.type_:
                    self.castling(position)
                    potential_rook.castling(self.position)
                    self.board.turn = Turn.white.value if self.type_ == Turn.black.value else Turn.black.value
                    self.board.count_turn -= 1
                else: 
                    self.board.drag_figure(self, position)
                self.is_moved = True

    def castling(self, rook_position):
        if rook_position.y > self.position.y:
            self.board.drag_figure(self, Coordinates(x=self.position.x, y=self.position.y + 2))
        else:
            self.board.drag_figure(self, Coordinates(x=self.position.x, y=self.position.y - 2))

    def get_available_moves(self):
        available_moves = []
        available_moves.extend([(coord := Coordinates(self.position.x + 1, y)) for y in [self.position.y - 1, self.position.y, self.position.y + 1]])
        available_moves.extend([(coord := Coordinates(self.position.x, y)) for y in [self.position.y - 1, self.position.y, self.position.y + 1]])
        available_moves.extend([(coord := Coordinates(self.position.x - 1, y)) for y in [self.position.y - 1, self.position.y, self.position.y + 1]])
        
        available_moves = [move for move in available_moves if (-1 < move.x < 8) and (-1 < move.y < 8) and ((self.board.board[move.x][move.y] is None) or (self.board.board[move.x][move.y] and self.board.board[move.x][move.y].type_ != self.type_))]
        if not self.is_moved:
            if (first_rook := self.board.board[7 if self.type_ == Turn.white.value else 0][0]) and first_rook.name == 'rook' or (second_rook := self.board.board[7 if self.type_ == Turn.white.value else 0][7]) and second_rook.name == 'rook':

                for rook in [Coordinates(7,0), Coordinates(7, 7), Coordinates(0,0), Coordinates(0, 7)]:
                    if rook.x == self.position.x:
                        is_castling = True
                        for cell in range(self.position.y + (1 if rook.y == 7 else -1), rook.y, -1 if rook.y == 0 else 1):
                            if self.board.board[self.position.x][cell] is not None:
                                is_castling = False
                                break
                        if is_castling:
                            available_moves.append(rook)
        #print(available_moves)

        return available_moves