import pygame
import math

# Classe representant la grenade
class Explosion(pygame.sprite.Sprite):
    
    def __init__(self, x, y):
        super().__init__()
        # Image
        self.scale = 1.5
        self.frame_index = 0
        self.images = []
        self.image = self.animation()
        
        # Position
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        # Animation
        self.counter = 0
    
    def update(self, screen_scroll):
        explosion_speed = 4
        
        # scroll
        self.rect.x += screen_scroll

        # Mettre a jour l'animation d'explosion
        self.counter += 1
        
        if self.counter >= explosion_speed:
            self.counter = 0
            self.frame_index += 1
            #if the animation is complete then delete the explosion
            if self.frame_index >= len(self.images):
            	self.kill()
            else:
            	self.image = self.images[self.frame_index]
    
    def animation(self):
        # Mettre toute les images dans animation_list
        for i in range(1, 6):
            image = pygame.image.load(f'img/explosion/exp{i}.png').convert_alpha()
            image = pygame.transform.scale(image, (math.ceil(image.get_width() * self.scale), math.ceil(image.get_height() * self.scale)))
            self.images.append(image)
        
        return self.images[self.frame_index]