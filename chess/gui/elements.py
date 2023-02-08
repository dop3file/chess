from abc import ABC, abstractmethod

import pygame

import config
from engine.figure import Figure
from engine.utils import Coordinates


class GUIElement(ABC):
    @abstractmethod
    def process(self):
        ...
    
class Button(GUIElement):
    def __init__(self, x, y, width, height, button_text, on_click_func, screen, image=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.button_text = button_text
        self.on_click_func = on_click_func
        self.image = image
        self.screen = screen

        self.button_surface = pygame.Surface((self.width, self.height))
        self.button_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        font = pygame.font.Font(f'{config.BASE_IMAGE_DIR}/arcadeclassic.regular.ttf', 58)
        self.text_surface = font.render(self.button_text, True, (20, 20, 20))

        self.background_colors = {
            'normal': '#e6e6e6',
            'hover': '#b3b3b3',
            'pressed': '#333333',
        }

    def process(self, mouse_pos):
        self.button_surface.fill(self.background_colors['normal'])
        if self.button_rect.collidepoint(pygame.mouse.get_pos()):
            self.button_surface.fill(self.background_colors['hover'])
            if pygame.mouse.get_pressed()[0]:
                self.button_surface.fill(self.background_colors['pressed'])
                self.on_click_func()

        self.button_surface.blit(self.text_surface, [
            self.button_rect.width/2 - self.text_surface.get_rect().width/2,
            self.button_rect.height/2 - self.text_surface.get_rect().height/2
        ])
        self.screen.blit(self.button_surface, self.button_rect)


class MoveHighlight:
    def __init__(self, position: Coordinates, figure: Figure):
        self.position = position
        self.figure = figure