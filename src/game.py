import os
from select import select
from headers import Coordinates, Turn

import pygame


class Game:
	def __init__(self, board):
		self.board = board
		self.original_board = board
		self.WIDTH, self.HEIGHT = 8, 8
		self.BASE_IMAGE_DIR = "../static"
		self.TILE = 100
		self.GAME_RES = self.WIDTH * self.TILE, self.HEIGHT * self.TILE + 125
		self.FPS = 30
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
		self.PIECE_WIDTH, self.PIECE_HEIGHT = 90, 90

	def draw_board(self):
		pygame.init()
		pygame.font.init()

		white, black = (238,238,213), (125,148,93)
		font = pygame.font.Font(f'{self.BASE_IMAGE_DIR}/arcadeclassic.regular.ttf', 58)

		screen = pygame.display.set_mode(self.GAME_RES)
		pygame.display.set_caption('Chess')
		pygame.display.set_icon(pygame.image.load(f'{self.BASE_IMAGE_DIR}/knight_black.png'))

		screen.fill(white)

		clock = pygame.time.Clock()

		select_piece = None
		is_roll = False

		while True:
			pygame.display.flip()
			clock.tick(self.FPS)

			# рисуем сетку
			for num in range(self.WIDTH ** 2):
				surface = pygame.Surface((100, 100))
				if int(num / 8) % 2 == 0:
					if num % 2 == 0:
						surface.fill(white)
					else:
						surface.fill(black)
				else:
					if num % 2 == 0:
						surface.fill(black)
					else:
						surface.fill(white)
				screen.blit(surface, (num * self.TILE if num < 8 else (num - int(num / 8) * 8) * self.TILE, int(num / 8) * self.TILE))

			if is_roll:
				self.board.roll_board()
				is_roll = False

			# рисуем фигуры
			for x, line in enumerate(self.board.board):
				for y, cell in enumerate(line):
					if cell:
						piece = self.PIECE_IMAGES[f'{cell.name}_{cell.type_}']
						piece = pygame.transform.scale(piece, (self.PIECE_WIDTH,self.PIECE_WIDTH))
						piece.convert()
						screen.blit(piece, (y * self.TILE + 5, x * self.TILE + 5))

			white_figures_count, black_figures_count = 0, 0

			# рисуем "мертвые" фигуры
			for figure in self.board.dead_figures:
				piece = self.PIECE_IMAGES[f'{figure.name}_{figure.type_}']
				piece = pygame.transform.scale(piece, (self.PIECE_WIDTH / 4, self.PIECE_HEIGHT / 4))
				piece.convert()
				if figure.type_ == Turn.white.value:
					screen.blit(piece, (100 + (white_figures_count * 25), self.HEIGHT * self.TILE + 35))
					white_figures_count += 1
				else:
					screen.blit(piece, (100 + (black_figures_count * 25), self.HEIGHT * self.TILE + 10))
					black_figures_count += 1

			# рисуем текст количества ходов
			position = (self.WIDTH * self.TILE - 270, self.HEIGHT * self.TILE)
			rect = pygame.Surface((300, 200))
			rect.fill(white)
			screen.blit(rect, position)
			turn_count_text = font.render(f'Turn  {self.board.count_turn}', True, (0,0,0))
			screen.blit(turn_count_text, position)

			# кнопка для переворота поля
			roll_board_btn = pygame.image.load(os.path.join(f'{self.BASE_IMAGE_DIR}/reload.png'))
			roll_board_btn = pygame.transform.scale(roll_board_btn, (64,64))
			roll_board_btn.convert()
			screen.blit(roll_board_btn, (0, self.HEIGHT * self.TILE + 5))

			# шах, шах и мат
			position = (self.WIDTH * self.TILE - 790, self.HEIGHT * self.TILE + 65)
			rect = pygame.Surface((200, 100))
			rect.fill(white)
			screen.blit(rect, position)
			if self.board.is_check:
				is_check_text = font.render("Check", True, (0,0,0))
				screen.blit(is_check_text, position)

			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONDOWN:
					click_position = pygame.mouse.get_pos()
					if click_position[1] > 800:
						if click_position[0] in list(range(0,75)) and click_position[1] in list(range(750, 850)):
							is_roll = True
					else:
						if select_piece and select_piece.type_ == self.board.turn:
							select_piece.move(position=Coordinates(x=int(click_position[1] / 100) , y=int(click_position[0] / 100)))
							select_piece = None
						if (piece := self.board.board[int(click_position[1] / 100)][int(click_position[0] / 100)]) is not None and select_piece is None and piece.type_ == self.board.turn:
							select_piece = piece
							print(select_piece)
							print(select_piece.get_available_moves())
							
				if event.type == pygame.QUIT:
					exit()
				

