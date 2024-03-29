import config
import pygame
import pyautogui

from gui.elements import Button
from gui.game import Game
from bots.bot import EasyBot
from server.client import init_client


class Menu:
    def __init__(self):
        self.FPS = config.FPS
        self.GAME_RES = (800, 600)
        self.BASE_IMAGE_DIR = config.BASE_IMAGE_DIR

    def start_main_menu(self):
        pygame.init()
        pygame.font.init()
        
        screen = pygame.display.set_mode(self.GAME_RES)
        pygame.display.set_caption('Chess')
        pygame.display.set_icon(pygame.image.load(f'{self.BASE_IMAGE_DIR}/knight_black.png'))
        clock = pygame.time.Clock()

        pygame.mixer.music.load(f'{self.BASE_IMAGE_DIR}/track.mp3')
        pygame.mixer.music.play(-1)

        white = (238,238,213)

        screen.fill(white)

        gui_elements = []
        gui_elements.append(Button(250, 150, 300, 75, 'Play', Game.init_game, screen))
        gui_elements.append(Button(250, 250, 300, 75, 'Bot', self.start_bot_menu, screen))
        gui_elements.append(Button(250, 350, 300, 75, 'Online', init_client, screen))

        while True:
            for gui_el in gui_elements:
                gui_el.process(pygame.mouse.get_pos())

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            pygame.display.flip()
            clock.tick(self.FPS)
            
            screen.fill(white)

    def start_bot_menu(self):
        pygame.init()
        pygame.font.init()
        
        screen = pygame.display.set_mode(self.GAME_RES)
        pygame.display.set_caption('Chess')
        pygame.display.set_icon(pygame.image.load(f'{self.BASE_IMAGE_DIR}/knight_black.png'))
        clock = pygame.time.Clock()

        white = (238,238,213)

        screen.fill(white)

        gui_elements = []
        gui_elements.append(Button(250, 100, 300, 75, 'Easy', EasyBot.init_bot, screen))
        gui_elements.append(Button(250, 200, 300, 75, 'Medium', EasyBot.init_bot, screen))
        gui_elements.append(Button(250, 300, 300, 75, 'Hard', EasyBot.init_bot, screen))


        while True:
            for gui_element in gui_elements:
                gui_element.process(pygame.mouse.get_pos())

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            pygame.display.flip()
            clock.tick(self.FPS)
            
            screen.fill(white)
    
            

            