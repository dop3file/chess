import os
import pygame

from engine.board import Board
from engine.headers import Coordinates, Turn, Move
from engine.figure import Figure
import gui.utils
import config



class Game:
	def __init__(self, board):
		self.board = board

		self.WIDTH, self.HEIGHT = config.BOARD_WIDTH, config.BOARD_HEIGHT
		self.BASE_IMAGE_DIR = config.BASE_IMAGE_DIR
		self.TILE = 100
		self.GAME_RES = self.WIDTH * self.TILE, self.HEIGHT * self.TILE + 125
		self.PIECE_WIDTH, self.PIECE_HEIGHT = 90, 90
		self.FPS = config.FPS
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
		self.INFO_PANEL_POS_X = 800
		self.DEAD_FIGURES_PADDING = 25

		pygame.init()
		pygame.font.init()
		self.screen = pygame.display.set_mode(self.GAME_RES)

		self.colors = {
			'white': (238,238,213),
			'black': (125,148,93),
			'green': (124,252,0),
			'orange': (255,127,80),
		}

		self.count_dead_black_figures = self.count_dead_white_figures = 1
		self.available_moves_highlight: list[Move] = []
		self.select_piece = None
		self.is_roll = False

		self.font = pygame.font.Font(f'{self.BASE_IMAGE_DIR}/arcadeclassic.regular.ttf', 58)
		self.timer_font = pygame.font.SysFont('Arial', 24)

		pygame.display.set_caption('Chess')
		pygame.display.set_icon(pygame.image.load(f'{self.BASE_IMAGE_DIR}/knight_black.png'))
		self.clock = pygame.time.Clock()
		self.screen.fill(self.colors['white'])

	@staticmethod
	def init_game(board: Board = None) -> None:
		if board is None:
			board = Board()
			board.set_defautl_board()
		game = Game(board)
		game.start_game()

	def draw_roll_board_button(self) -> None:
		roll_board_btn = pygame.image.load(os.path.join(f'{self.BASE_IMAGE_DIR}/reload.png'))
		roll_board_btn = pygame.transform.scale(roll_board_btn, (64,64))
		roll_board_btn.convert()
		self.screen.blit(roll_board_btn, (0, self.HEIGHT * self.TILE + 5))

	def draw_timer_text(self, color: tuple[int, int, int], start_time_ticks: int, font: pygame.font.Font) -> None:
		position = (self.WIDTH * self.TILE - 270, self.HEIGHT * self.TILE + 50)
		rect = pygame.Surface((300, 200))
		rect.fill(color)
		self.screen.blit(rect, position)
		count_seconds = round(start_time_ticks / 1000 % 60, 2)
		count_minutes = int(start_time_ticks / 60000 % 24)
		turn_count_text = font.render(f'{"0" if count_minutes < 10 else ""}{count_minutes}:{count_seconds}', True, (0,0,0))
		self.screen.blit(turn_count_text, position)

	def draw_check_mate_info(self, color: tuple[int, int, int], font: pygame.font.Font) -> None:
		position = (self.WIDTH * self.TILE - 790, self.HEIGHT * self.TILE + 65)
		rect = pygame.Surface((200, 100))
		rect.fill(color)
		self.screen.blit(rect, position)
		if self.board.check_turn or self.board.is_check_mate:
			is_check_text = font.render("Check" if self.board.check_turn and not self.board.is_check_mate else "Check Mate", True, (0,0,0))
			self.screen.blit(is_check_text, position)
	
	def draw_count_turns_text(self, color: tuple[int, int, int], font: pygame.font.Font) -> None:
		position = (self.WIDTH * self.TILE - 270, self.HEIGHT * self.TILE)
		rect = pygame.Surface((300, 200))
		rect.fill(color)
		self.screen.blit(rect, position)
		turn_count_text = font.render(f'Turn  {self.board.count_turn}', True, (0,0,0))
		self.screen.blit(turn_count_text, position)

	def draw_highlights_moves(self) -> None:
		for move_hightlight in self.available_moves_highlight:
			surface = pygame.Surface((100, 100))
			surface.set_alpha(self.HIGHLIGHT_OPACITY)
			surface.fill(self.colors['orange'])
			if self.is_roll:
				bias_factor = -200 if move_hightlight.figure.type_ == Turn.white.value else 200
				self.screen.blit(surface, (move_hightlight.position.y * self.TILE, move_hightlight.position.x * self.TILE + bias_factor))
			else:
				self.screen.blit(surface, (move_hightlight.position.y * self.TILE, move_hightlight.position.x * self.TILE))

	def draw_dead_figures(self) -> None:
		for figure in self.board.dead_figures:
			piece = self.PIECE_IMAGES[f'{figure.name}_{figure.type_}']
			piece = pygame.transform.scale(piece, (self.PIECE_WIDTH / 4, self.PIECE_HEIGHT / 4))
			piece.convert()
			if figure.type_ == Turn.white.value:
				self.screen.blit(piece, (self.TILE + (self.count_dead_white_figures * self.DEAD_FIGURES_PADDING), self.HEIGHT * self.TILE + 35))
				self.count_dead_white_figures += 1
			else:
				self.screen.blit(piece, (self.TILE + (self.count_dead_black_figures * 25), self.HEIGHT * self.TILE + 10))
				self.count_dead_black_figures += 1
		
	def draw_figure(self, figure: Figure, x: int , y: int) -> None:
		piece = self.PIECE_IMAGES[f'{figure.name}_{figure.type_}']
		piece = pygame.transform.scale(piece, (self.PIECE_WIDTH,self.PIECE_WIDTH))
		piece.convert()
		self.screen.blit(piece, (y * self.TILE + 5, x * self.TILE + 5))

	def draw_figures(self) -> None:
		for x, line in enumerate(self.board.board[::-1] if self.is_roll else self.board.board):
				for y, cell in enumerate(line):
					if cell:
						self.draw_figure(cell, x, y)

	def draw_board(self) -> None:
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

	def is_click_on_roll_button(self, click_position: tuple[int, int]) -> bool | None:
		if click_position[1] > self.INFO_PANEL_POS_X:
			if 0 <= click_position[0] <= 75 and 750 <= click_position[1] <= 850:
				return not self.is_roll
		return None

	def is_click_on_board(self, click_position: tuple[int, int]) -> bool:
		return True if abs(click_position[1]) <= self.WIDTH * self.TILE and abs(click_position[0]) <= self.HEIGHT * self.TILE else False

	def is_valid_piece(self, click_position: tuple[int, int]) -> Figure | None:
		piece = self.board.board[int(click_position[1] / self.TILE)][int(click_position[0] / self.TILE)]
		if piece is not None and self.select_piece is None and piece.type_ == self.board.turn:
			return piece
		return None

	def display_fps(self) -> None:
		print(f'FPS {self.clock.get_fps()}')

	def start_game(self):
		while True:
			pygame.display.flip()
			self.clock.tick(self.FPS)

			self.display_fps()	
			self.draw_board()
			self.draw_highlights_moves()
			self.draw_figures()

			self.count_dead_black_figures = self.count_dead_white_figures = 1
			self.draw_dead_figures()

			self.draw_count_turns_text(self.colors['white'], self.font)
			self.draw_timer_text(self.colors['white'], pygame.time.get_ticks(), self.timer_font)
			self.draw_roll_board_button()
			self.draw_check_mate_info(self.colors['white'], self.font)
				
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONDOWN and not self.board.is_check_mate:
					click_position = pygame.mouse.get_pos()
					
					if (is_click := self.is_click_on_roll_button(click_position)) is not None:
						self.is_roll = is_click
					else:
						if self.is_roll:
							click_position = (click_position[0], -click_position[1] - self.TILE)
						if self.select_piece and self.select_piece.type_ == self.board.turn:
							self.select_piece.move(position=Coordinates(x=int(click_position[1] / self.TILE) if not self.is_roll else int(click_position[1] / self.TILE) + self.HEIGHT, y=int(click_position[0] / self.TILE)))
							self.select_piece = None
							self.available_moves_highlight = []
						if self.is_click_on_board(click_position) and (piece := self.is_valid_piece(click_position)):
							self.select_piece = piece
							self.available_moves_highlight = []
							for move in self.select_piece.get_available_moves(is_check_call=True):
								move_highlight = Move(position=move, figure=piece)
								self.available_moves_highlight.append(move_highlight)

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						gui.utils.startup_menu()

				if event.type == pygame.QUIT:
					exit()