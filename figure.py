from abc import ABC, abstractmethod
from zoneinfo import available_timezones
from headers import Coordinates 


class Figure(ABC):
    def __init__(self, position: Coordinates, name: str, board, type_):
        self.position = position
        self.name = name
        self.board = board
        self.type_ = type_

    @abstractmethod
    def move(self, position):
        pass

    @abstractmethod
    def get_avialable_moves(self):
        pass

    def __repr__(self):
        return f'{self.name} x={self.position.x} y={self.position.y}'

    def __str__(self):
        return self.name


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
        if position in self.get_avialable_moves():
            self.board.drag_figure(self.position, position)
            self.position = position

    def get_avialable_moves(self):
        available_moves = []
        check_front = (self.board.board[(x := self.position.x + (1 * self.type_))][(y := self.position.y)])

        if check_front == None:
            available_moves.append(Coordinates(x=x, y=y))

        if self.position == self.default_position and (self.board.board[(x := self.position.x + (2 * self.type_))][self.position.y]) == None and check_front == None:
            available_moves.append(Coordinates(x=x, y=y))

        return available_moves

    def kill_figure(self, position):
        pass