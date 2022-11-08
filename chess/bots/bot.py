from abc import abstractmethod, ABC
import random
from collections import namedtuple

from engine.headers import Turn, Coordinates
from engine.board import Board
from gui.game import Game


class Bot(ABC):
    @abstractmethod
    def init_bot(self):
        ...
    
    @abstractmethod
    def move(self):
        ...

    def start_game(self):
        board = BotBoard(self)
        board.set_defautl_board()
        Game.init_game(board=board)


class BotBoard(Board):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    def drag_figure(self, figure, new_coordinate: Coordinates):
        super().drag_figure(figure, new_coordinate)
        if self.count_turn % 2 != 0:
            self.bot.move(self)

class EasyBot(Bot):
    @staticmethod
    def get_figure_with_random_move(board: Board):
        figure = EasyBot.get_random_figure(board.board, BOT_TURN)
        return namedtuple("figure", "figure move")(figure=figure, move=random.choice(figure.get_available_moves()))
        
    @staticmethod
    def get_random_figure(board: list[list], turn):
        return random.choice([figure for line in board for figure in line if figure and figure.type_ == turn and figure.get_available_moves()])
    
    @staticmethod
    def init_bot():
        bot = EasyBot()
        bot.start_game()

    @staticmethod
    def move(board):
        (move := EasyBot.get_figure_with_random_move(board)).figure.move(move.move)

class MediumBot(Bot):
    @staticmethod
    def init_bot():
        bot = MediumBot()
        bot.start_game()

    @staticmethod
    def move():
        ...


BOT_TURN = Turn.black.value