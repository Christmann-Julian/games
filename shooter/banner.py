import pygame
import math

class Banner:

    def __init__(self, screen):
        self.screen = screen
        # Banniere
        self.banner = pygame.image.load('assets/banner.png')
        self.banner = pygame.transform.scale(self.banner, (500, 500))
        self.banner_rect = self.banner.get_rect()
        self.banner_rect.x = math.ceil(self.screen.get_width() / 4)
        
        # Bouton pour commencer partie
        self.play_button = pygame.image.load('assets/button.png')
        self.play_button = pygame.transform.scale(self.play_button, (400, 150))
        self.play_button_rect = self.play_button.get_rect()
        self.play_button_rect.x = math.ceil(self.screen.get_width() / 3.33)
        self.play_button_rect.y = math.ceil(self.screen.get_height() / 2)
        
    
    def get_banner(self):
        self.screen.blit(self.banner, self.banner_rect)
    
    def get_play_button(self):
        self.screen.blit(self.play_button, self.play_button_rect)