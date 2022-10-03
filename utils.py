from re import I
from headers import Coordinates


def end_of_loop():
    raise StopIteration


def check_horizontal_line(board, figure, factor: bool):
    '''
    Функция возвращает возможные ходы по горизонтали
    board - двумерный массив из экземпляра доски
    figure - экземпляр фигуры
    factor - направление
    '''
    available_moves = []
    for y in range(figure.position.y + 1, 8) if factor else range(figure.position.y - 1, -1, -1):
        if board[figure.position.x][y] is not None:
            if figure.type_ != board[figure.position.x][y].type_: 
                available_moves.append(Coordinates(x=figure.position.x, y=y))
            break
        available_moves.append(Coordinates(x=figure.position.x, y=y))

    return available_moves


def check_vertical_line(board, figure, factor: bool):
    '''
    Функция возвращает возможные ходы по вертикали
    '''
    available_moves = []
    for x in range(figure.position.x + 1, 8) if factor else range(figure.position.x - 1, -1, -1):
        if board[x][figure.position.y] is not None:
            if figure.type_ != board[x][figure.position.y].type_: 
                available_moves.append(Coordinates(x=x, y=figure.position.y))
            break
        available_moves.append(Coordinates(x=x, y=figure.position.y))

    return available_moves


def check_diagonal_line(board, figure, factor: bool):
    '''
    Функция возвращает возможные ходы по диагонали
    '''
    available_moves = []
    for x, y in zip(range(figure.position.x + 1, 8), range(figure.position.y + 1, 8)) if factor else zip(range(figure.position.x - 1, -1, -1), range(figure.position.y - 1, -1, -1)) :
        if board[x][y] is not None:
            if figure.type_ != board[x][y].type_:
                available_moves.append(Coordinates(x=x, y=y))
            break
        available_moves.append(Coordinates(x=x, y=y))

    for x, y in zip(range(figure.position.x + 1, 8), range(figure.position.y - 1, -1, -1)) if factor else zip(range(figure.position.x - 1, -1, -1), range(figure.position.y + 1, 8)) :
        if board[x][y] is not None:
            if figure.type_ != board[x][y].type_:
                available_moves.append(Coordinates(x=x, y=y))
            break
        available_moves.append(Coordinates(x=x, y=y))

    return available_moves


def check_knight_avialable_moves(board, figure):
    '''
    Функция возвращает возможные ходы в виде буквы Г(для коня)
    '''
    avialable_moves = []
    avialable_coords = [
        [figure.position.x - 2, figure.position.y - 1],
        [figure.position.x - 2, figure.position.y + 1],
        [figure.position.x + 2, figure.position.y + 1],
        [figure.position.x + 2, figure.position.y - 1],
        [figure.position.x - 1, figure.position.y - 2],
        [figure.position.x - 1, figure.position.y - 2],
        [figure.position.x + 1, figure.position.y - 2],
        [figure.position.x - 1, figure.position.y + 2],
        [figure.position.x + 1, figure.position.y + 2]
    ]
    for x, y in avialable_coords:
        if 0 <= x < 8 and 0 <= y < 8:
            if board[x][y] is None or (board[x][y].type_ != figure.type_):
                avialable_moves.append(Coordinates(x=x, y=y))
                
    return avialable_moves


def check_king_avialable_moves(board, figure):
    '''
    Функция возвращает возможные ходы для короля
    '''
    avialable_moves = []
    avialable_moves.extend([(coord := Coordinates(figure.position.x + 1, y)) for y in [figure.position.y - 1, figure.position.y, figure.position.y + 1]])
    avialable_moves.extend([(coord := Coordinates(figure.position.x, y)) for y in [figure.position.y - 1, figure.position.y, figure.position.y + 1]])
    avialable_moves.extend([(coord := Coordinates(figure.position.x - 1, y)) for y in [figure.position.y - 1, figure.position.y, figure.position.y + 1]])

    return [move for move in avialable_moves if (-1 < move.x < 8) and (-1 < move.y < 8) and ((board[move.x][move.y] is None) or (board[move.x][move.y] is not None and board[move.x][move.y].type_ != figure.type_))]


def check_king_check(board, figure):
    '''
    Функция возвращает под шахом ли король
    '''
    figures = [figure_ for line in board for figure_ in line if figure_ and figure_.type_ != figure.type_]
    for figure_ in figures:
        if figure_.name == 'knight':
            if Coordinates(x=figure.position.x, y=figure.position.y) in check_knight_avialable_moves(board, figure_):
                return True
        if figure_.name == 'bishop':
            available_moves = [
                check_diagonal_line(board, figure_, True), 
                check_diagonal_line(board, figure_, False)
            ]
            for moves in available_moves:
                if Coordinates(x=figure.position.x, y=figure.position.y) in moves:
                    return True
        if figure_.name == 'rook':
            available_moves = [
                check_vertical_line(board, figure_, True), 
                check_vertical_line(board, figure_, False)
            ]
            for moves in available_moves:
                if Coordinates(x=figure.position.x, y=figure.position.y) in moves:
                    return True
        if figure_.name == 'queen':
            available_moves = [
                check_diagonal_line(board, figure_, True), 
                check_diagonal_line(board, figure_, False), 
                check_vertical_line(board, figure_, False), 
                check_vertical_line(board, figure_, True), 
                check_horizontal_line(board, figure_, True), 
                check_horizontal_line(board, figure_, False)
            ]
            for moves in available_moves:
                if Coordinates(x=figure.position.x, y=figure.position.y) in moves:
                    return True
    
    return False
        
            