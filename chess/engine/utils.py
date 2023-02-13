from engine.headers import Coordinates


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
        
            