from abc import ABC, abstractmethod
from headers import Coordinates
from utils import check_horizontal_line, check_horizontal_line, check_vertical_line


class Figure(ABC):
    def __init__(self, position: Coordinates, name: str, board, type_):
        self.position = position
        self.name = name
        self.board = board
        self.type_ = type_

    @abstractmethod
    def move(self, position: Coordinates):
        pass

    @abstractmethod
    def get_available_moves(self):
        pass

    def __repr__(self):
        return f'{self.name} x={self.position.x} y={self.position.y}'

    def __str__(self):
        return f'{self.name} {self.position}'


class Pawn(Figure):
    def __init__(self, position, name, board, type_):
        super().__init__(
            position=position,
            name=name,
            board=board,
            type_=type_
        )
        self.default_position = position

    def move(self, position):
        if position in self.get_available_moves():
            if position.y != self.position.y:
                self.kill_figure(position)
            else:
                self.board.drag_figure(self.position, position)
                self.position = position

    def get_available_moves(self):
        available_moves = []
        check_front = (self.board.board[(x := self.position.x + (1 * self.type_))][(y := self.position.y)])

        if check_front == None:
            available_moves.append(Coordinates(x=x, y=y))

        if self.position == self.default_position and (self.board.board[(x := self.position.x + (2 * self.type_))][self.position.y]) == None and check_front == None:
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
            self.board.drag_figure(self.position, position)
            self.position = Coordinates(x=position.x, y=position.y)


class Rook(Figure):
    def __init__(self, position, name, board, type_):
        super().__init__(
            position=position,
            name=name,
            board=board,
            type_=type_
        )
        
    def move(self, position):
        if position in self.get_available_moves():
            if self.board.board[position.x][position.y] is not None:
                self.board.dead_figures.append(self.board.board[position.x][position.y])
            self.board.drag_figure(self.position, position)
            self.position = position

    def get_available_moves(self):
        available_moves = []
        available_moves.extend(check_horizontal_line(self.board.board, self, True))
        available_moves.extend(check_horizontal_line(self.board.board, self, False))
        available_moves.extend(check_vertical_line(self.board.board, self, True))
        available_moves.extend(check_vertical_line(self.board.board, self, False))

        return available_moves
            

