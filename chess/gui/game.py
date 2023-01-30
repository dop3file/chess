import os
import pygame

from engine.board import Board
from engine.headers import Coordinates, Turn
import config


class Game:
	def __init__(self, board):
		self.board = board

		self.WIDTH, self.HEIGHT = 8, 8
		self.BASE_IMAGE_DIR = config.BASE_IMAGE_DIR
		self.TILE = 100
		self.GAME_RES = self.WIDTH * self.TILE, self.HEIGHT * self.TILE + 125
		self.PIECE_WIDTH, self.PIECE_HEIGHT = 90, 90
		self.FPS = 60
		self.PIECE_IMAGES = {
			'pawn_-1': pygame.image.load(os.path.join(f"{self.BASE_IMAGE_DIR}/pawn.png")),
			'pawn_1': pygame.image.load(os.path.join(f"{self.BASE_IMAGE_DIR}/pawn_black.png")),
			'rook_-1': pygame.image.load(os.path.join(f"{self.BASE_IMAGE_DIR}/rock.png")),
			'rook_1': pygame.image.load(os.path.join(f"{self.BASE_IMAGE_DIR}/rock_black.png")),
			'knight_-1': pygame.image.load(os.path.join(f"{self.BASE_IMAGE_DIR}/knight.png")),
			'knight_1': pygame.image.load(os.path.join(f"{self.BASE_IMAGE_DIR}/knight_black.png")),
			'bishop_1': pygame.image.load(os.path.join(f"{self.BASE_IMAGE_DIR}/bishop_black.png")),
			'bishop_-1': pygame.image.load(os.path.join(f"{self.BASE_IMAGE_DIR}/bishop.png")),
			'queen_-1': pygame.image.load(os.path.join(f"{self.BASE_IMAGE_DIR}/queen.png")),
			'queen_1': pygame.image.load(os.path.join(f"{self.BASE_IMAGE_DIR}/queen_black.png")),
			'king_-1': pygame.image.load(os.path.join(f"{self.BASE_IMAGE_DIR}/king.png")),
			'king_1': pygame.image.load(os.path.join(f"{self.BASE_IMAGE_DIR}/king_black.png")),
		}
		self.HIGHLIGHT_OPACITY = 75

		pygame.init()
		pygame.font.init()
		self.screen = pygame.display.set_mode(self.GAME_RES)

		self.colors = {
			'white': (238,238,213),
			'black': (125,148,93),
			'green': (124,252,0),
			'orange': (255,127,80),
		}

		self.font = pygame.font.Font(f'{self.BASE_IMAGE_DIR}/arcadeclassic.regular.ttf', 58)
		self.timer_font = pygame.font.Font(f'{self.BASE_IMAGE_DIR}/Ubuntu-LightItalic.ttf', 24)

		pygame.display.set_caption('Chess')
		pygame.display.set_icon(pygame.image.load(f'{self.BASE_IMAGE_DIR}/knight_black.png'))

	@staticmethod
	def init_game(board=None):
		if board is None:
			board = Board()
			board.set_defautl_board()
		game = Game(board)
		game.start_game()

	def draw_roll_board_button(self):
		roll_board_btn = pygame.image.load(os.path.join(f'{self.BASE_IMAGE_DIR}/reload.png'))
		roll_board_btn = pygame.transform.scale(roll_board_btn, (64,64))
		roll_board_btn.convert()
		self.screen.blit(roll_board_btn, (0, self.HEIGHT * self.TILE + 5))

	def draw_timer_text(self, color, start_time_ticks, font):
		position = (self.WIDTH * self.TILE - 270, self.HEIGHT * self.TILE + 50)
		rect = pygame.Surface((300, 200))
		rect.fill(color)
		self.screen.blit(rect, position)
		count_seconds = start_time_ticks / 1000 % 60
		count_minutes = int(start_time_ticks / 60000 % 24)
		turn_count_text = font.render(f'{count_minutes}:{count_seconds}', True, (0,0,0))
		self.screen.blit(turn_count_text, position)

	def draw_check_mate_info(self, color, font):
		position = (self.WIDTH * self.TILE - 790, self.HEIGHT * self.TILE + 65)
		rect = pygame.Surface((200, 100))
		rect.fill(color)
		self.screen.blit(rect, position)
		if self.board.check_turn or self.board.is_check_mate:
			is_check_text = font.render("Check" if self.board.check_turn and not self.board.is_check_mate else "Check Mate", True, (0,0,0))
			self.screen.blit(is_check_text, position)
	
	def draw_count_turns_text(self, color, font):
		position = (self.WIDTH * self.TILE - 270, self.HEIGHT * self.TILE)
		rect = pygame.Surface((300, 200))
		rect.fill(color)
		self.screen.blit(rect, position)
		turn_count_text = font.render(f'Turn  {self.board.count_turn}', True, (0,0,0))
		self.screen.blit(turn_count_text, position)

	def draw_highlights_moves(self, move_hightlight):
		surface = pygame.Surface((100, 100))
		surface.set_alpha(self.HIGHLIGHT_OPACITY)
		surface.fill(self.colors['orange'])
		self.screen.blit(surface, (move_hightlight.y * self.TILE, move_hightlight.x * self.TILE))

	def start_game(self):
		self.screen.fill(self.colors['white'])

		clock = pygame.time.Clock()

		select_piece = None
		is_roll = False

		available_moves_highlight = []

		while True:
			pygame.display.flip()
			clock.tick(self.FPS)

			# рисуем сетку
			for num in range(self.WIDTH ** 2):
				surface = pygame.Surface((100, 100))
				color = None
				if int(num / 8) % 2 == 0:
					if num % 2 == 0:
						color = self.colors['white']
					else:
						color = self.colors['black']
				else:
					if num % 2 == 0:
						color = self.colors['black']
					else:
						color = self.colors['white']
				surface.fill(color)
				self.screen.blit(surface, (num * self.TILE if num < 8 else (num - int(num / 8) * 8) * self.TILE, int(num / 8) * self.TILE))

			# рисуем подсветку возможных ходов
			for move_hightlight in available_moves_highlight:
				self.draw_highlights_moves(move_hightlight)

			# рисуем фигуры
			for x, line in enumerate(self.board.board[::-1] if is_roll else self.board.board):
				for y, cell in enumerate(line):
					if cell:
						piece = self.PIECE_IMAGES[f'{cell.name}_{cell.type_}']
						piece = pygame.transform.scale(piece, (self.PIECE_WIDTH,self.PIECE_WIDTH))
						piece.convert()
						self.screen.blit(piece, (y * self.TILE + 5, x * self.TILE + 5))

			white_figures_count, black_figures_count = 0, 0

			# рисуем "мертвые" фигуры
			for figure in self.board.dead_figures:
				piece = self.PIECE_IMAGES[f'{figure.name}_{figure.type_}']
				piece = pygame.transform.scale(piece, (self.PIECE_WIDTH / 4, self.PIECE_HEIGHT / 4))
				piece.convert()
				if figure.type_ == Turn.white.value:
					self.screen.blit(piece, (100 + (white_figures_count * 25), self.HEIGHT * self.TILE + 35))
					white_figures_count += 1
				else:
					self.screen.blit(piece, (100 + (black_figures_count * 25), self.HEIGHT * self.TILE + 10))
					black_figures_count += 1

			self.draw_count_turns_text(color, self.font)
			self.draw_timer_text(self.colors['white'], pygame.time.get_ticks(), self.timer_font)
			self.draw_roll_board_button()
			self.draw_check_mate_info(color, self.font)
				
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONDOWN and not self.board.is_check_mate:
					click_position = pygame.mouse.get_pos()
					
					if click_position[1] > 800:
						if click_position[0] in list(range(0,75)) and click_position[1] in list(range(750, 850)):
							is_roll = False if is_roll else True
					else:
						try:
							if is_roll:
								click_position = (click_position[0], -click_position[1] - 100)
							if select_piece and select_piece.type_ == self.board.turn:
								select_piece.move(position=Coordinates(x=int(click_position[1] / 100) if not is_roll else int(click_position[1] / 100) + 8, y=int(click_position[0] / 100)))
								select_piece = None
								available_moves_highlight = []
							if (piece := self.board.board[int(click_position[1] / 100)][int(click_position[0] / 100)]) is not None and select_piece is None and piece.type_ == self.board.turn:
								select_piece = piece
								available_moves_highlight = []
								for move in select_piece.get_available_moves():
									available_moves_highlight.append(move)
						except IndexError:
							pass
							
				if event.type == pygame.QUIT:
					exit()