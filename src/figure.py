from abc import ABC, abstractmethod
from headers import Coordinates, Turn, figures_ranks
from utils import check_horizontal_line, check_vertical_line, check_diagonal_line
                  


class Figure(ABC):
    def __init__(self, position: Coordinates, board, type_):
        self.position = position
        self.name = self.__class__.__name__.lower()
        self.board = board
        self.type_ = type_

    def move(self, position: Coordinates):
        if position in self.get_available_moves():
            if self.board.board[position.x][position.y] is not None:
                self.board.dead_figures.append(self.board.board[position.x][position.y])
            self.board.drag_figure(self, position)

    def verify_check(self):
        if self.board.is_check:
            print(1)

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

    def move(self, position):
        if position in self.get_available_moves():
            if position.y != self.position.y:
                self.kill_figure(position)
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

    def kill_figure(self, position: Coordinates):
        if self.board.board[position.x][position.y].type_ != self.type_:
            self.board.dead_figures.append(self.board.board[position.x][position.y])
            self.board.drag_figure(self, position)
            self.position = Coordinates(x=position.x, y=position.y)


class Rook(Figure):
    def __init__(self, position, board, type_):
        super().__init__(
            position=position,
            board=board,
            type_=type_
        )
        
    def move(self, position):
        super().move(position)

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
        
    def move(self, position):
        super().move(position)

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
        
    def move(self, position):
        super().move(position)

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
        
    def move(self, position):
        super().move(position)

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
        
    def move(self, position):
        super().move(position)

    def get_available_moves(self):
        available_moves = []
        available_moves.extend([(coord := Coordinates(self.position.x + 1, y)) for y in [self.position.y - 1, self.position.y, self.position.y + 1]])
        available_moves.extend([(coord := Coordinates(self.position.x, y)) for y in [self.position.y - 1, self.position.y, self.position.y + 1]])
        available_moves.extend([(coord := Coordinates(self.position.x - 1, y)) for y in [self.position.y - 1, self.position.y, self.position.y + 1]])

        return [move for move in available_moves if (-1 < move.x < 8) and (-1 < move.y < 8) and ((self.board.board[move.x][move.y] is None) or (self.board.board[move.x][move.y] is not None and self.board.board[move.x][move.y].type_ != self.type_))]