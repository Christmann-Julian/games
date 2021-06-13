import pygame
from projectile import Projectile
import animation

# Classe representant le joueur
class Player(animation.AnimateSprite):
    
    def __init__(self, game):
        super().__init__('player')
        # Classe game
        self.game = game
        # Sante
        self.health = 100
        self.max_health = 100
        # Attaque
        self.attack = 20
        # Image
        #self.image = pygame.image.load('assets/player.png')
        # Position
        self.rect = self.image.get_rect()
        self.rect.x = 425
        self.rect.y = 500
        # Projectile
        self.all_fire_right = pygame.sprite.Group()
        self.all_fire_left = pygame.sprite.Group()
        # Vitesse
        self.velocity = 5
    
    def update_health_bar(self, surface):
        # Dessiner la bar de vie
        pygame.draw.rect(surface, (60, 63, 60), [self.rect.x + 50, self.rect.y + 20, self.max_health, 7])
        pygame.draw.rect(surface, (111, 210, 46), [self.rect.x + 50, self.rect.y + 20, self.health, 7])
    
    def update_animation(self):
        self.animate()
    
    def damage(self, attack):
        # Enlever les degats infliges
        if self.health - attack > attack:
            self.health -= attack
        # Fin de partie
        else:
            self.game.game_over()

    def move_right(self):
        # Condition de collision avec monstre
        if not self.game.check_collision(self, self.game.all_monsters):
            self.rect.x += self.velocity
    
    def move_left(self):
        # Condition de collision avec monstre
        if not self.game.check_collision(self, self.game.all_monsters):
            self.rect.x -= self.velocity

    def fire_right(self):
        projectile = Projectile(self)
        self.all_fire_right.add(projectile)
        # Lancer animation 
        self.start_animation()
        # jouer le son
        self.game.sound_manager.play('tir')

    def fire_left(self):
        projectile = Projectile(self)
        self.all_fire_left.add(projectile)
        # Lancer animation 
        self.start_animation()
        # jouer le son
        self.game.sound_manager.play('tir')
