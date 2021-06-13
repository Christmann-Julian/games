import pygame

# Classe representant le tir
class Bullet(pygame.sprite.Sprite):
    
    def __init__(self, x, y, direction):
        super().__init__()
        # Image
        self.image = pygame.image.load('img/icons/bullet.png').convert_alpha()
        # Position
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # Direction
        self.direction = direction
        # Vitesse
        self.speed = 5
    
    def update(self, player, enemy, bullet_group, enemy_group, world, screen_scroll):
        # deplacement des tirs
        self.rect.x += (self.direction * self.speed) + screen_scroll

        # Verifier les collisions des balles avec la map
        for tile in world.obstacle_list:
        	if tile[1].colliderect(self.rect):
        		self.kill()

        # verifier si le tir sort de l'ecran
        if self.rect.right < 0 or self.rect.left > 800:
            self.kill()
        
        # Verifier collision entre tir et perso
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                player.health -= 10
                self.kill()
        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, bullet_group, False):
                if enemy.alive:
                    enemy.health -= 25
                    self.kill()