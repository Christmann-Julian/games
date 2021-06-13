import pygame
from explosion import Explosion

# Classe representant la grenade
class Grenade(pygame.sprite.Sprite):
    
    def __init__(self, x, y, direction):
        super().__init__()
        # Image
        self.image = pygame.image.load('img/icons/grenade.png').convert_alpha()
        # Position
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        # Direction
        self.direction = direction
        # Vitesse
        self.speed = 5
        self.vel_y = -11
        # Temps
        self.timer = 100
    
    def update(self, gravity, explosion_group, player, enemy_group, tile_size, world, screen_scroll, grenade_fx):
        self.vel_y += gravity
        dx = self.direction * self.speed
        dy = self.vel_y        
        
        # Verifier collision avec la map
        for tile in world.obstacle_list:
        	#c Verifier collision avec mur
        	if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
        		self.direction *= -1
        		dx = self.direction * self.speed
        	# Verifier collision en y
        	if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
        		self.speed = 0
        		# Verifier si jete
        		if self.vel_y < 0:
        			self.vel_y = 0
        			dy = tile[1].bottom - self.rect.top
        		# Verifier si au dessus du sol
        		elif self.vel_y >= 0:
        			self.vel_y = 0
        			dy = tile[1].top - self.rect.bottom	

        # Changer la position de la grenade
        self.rect.x += dx + screen_scroll
        self.rect.y += dy

        # Enlever du temps avant explosion
        self.timer -= 1

        if self.timer <= 0:
            self.kill()
            grenade_fx.play()
            explosion = Explosion(self.rect.x, self.rect.y)
            explosion_group.add(explosion)

            # Enlever degats
            if abs(self.rect.centerx - player.rect.centerx) < tile_size * 2 and abs(self.rect.centery - player.rect.centery) < tile_size * 2:
                player.health -= 50
            for enemy in enemy_group:
                if abs(self.rect.centerx - enemy.rect.centerx) < tile_size * 2 and abs(self.rect.centery - enemy.rect.centery) < tile_size * 2:
                    enemy.health -= 50