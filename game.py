import os
from headers import Coordinates

import pygame


class Game:
	def __init__(self, board):
		self.board = board
		self.WIDTH, self.HEIGHT = 8, 8
		self.TILE = 100
		self.GAME_RES = self.WIDTH * self.TILE, self.HEIGHT * self.TILE
		self.FPS = 30
		self.PIECE_IMAGES = {
			'pawn_-1': pygame.image.load(os.path.join("static/pawn.png")),
			'pawn_1': pygame.image.load(os.path.join("static/pawn_black.png")),
			'rook_-1': pygame.image.load(os.path.join("static/rock.png")),
			'rook_1': pygame.image.load(os.path.join("static/rock_black.png")),
			'knight_-1': pygame.image.load(os.path.join("static/knight.png")),
			'knight_1': pygame.image.load(os.path.join("static/knight_black.png")),
			'bishop_1': pygame.image.load(os.path.join("static/bishop_black.png")),
			'bishop_-1': pygame.image.load(os.path.join("static/bishop.png")),
			'queen_-1': pygame.image.load(os.path.join("static/queen.png")),
			'queen_1': pygame.image.load(os.path.join("static/queen_black.png")),
			'king_-1': pygame.image.load(os.path.join("static/king.png")),
			'king_1': pygame.image.load(os.path.join("static/king_black.png")),
		}
		self.PIECE_WIDTH, self.PIECE_HEIGHT = 90, 90

	def draw_board(self):
		pygame.init()

		white, black = (238,238,213), (125,148,93)

		screen = pygame.display.set_mode(self.GAME_RES)

		screen.fill(white)

		clock = pygame.time.Clock()

		select_piece = None

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

			# рисуем фигуры
			for x, line in enumerate(self.board.board):
				for y, cell in enumerate(line):
					if cell:
						piece = self.PIECE_IMAGES[f'{cell.name}_{cell.type_}']
						piece = pygame.transform.scale(piece, (self.PIECE_WIDTH,self.PIECE_WIDTH))
						piece.convert()
						screen.blit(piece, (y * self.TILE + 5, x * self.TILE + 5))

			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONDOWN:
					click_position = pygame.mouse.get_pos()
					if select_piece and select_piece.type_ == self.board.turn:
						select_piece.move(position=Coordinates(x=int(click_position[1] / 100), y=int(click_position[0] / 100)))
						select_piece = None
					if (piece := self.board.board[int(click_position[1] / 100)][int(click_position[0] / 100)]) is not None and select_piece is None and piece.type_ == self.board.turn:
						select_piece = piece
						
				if event.type == pygame.QUIT:
					exit()
				

