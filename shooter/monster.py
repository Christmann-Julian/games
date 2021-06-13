import pygame
import random
import animation

# Classe representant le monstre
class Monster(animation.AnimateSprite):
    
    def __init__(self, game, screen, name, size, offsets=0, rect_x=1000 + random.randint(0, 300) ):
        super().__init__(name, size)
        self.name = name
        # Surface
        self.screen = screen
        # Classe game
        self.game = game
        # Sante
        self.health = 100
        self.max_health = 100
        # Attaque
        self.attack = 0.3
        # Position
        self.rect = self.image.get_rect()
        self.rect.x = rect_x
        self.rect_start = rect_x
        self.rect.y = 540 - offsets
        # Animation
        self.start_animation()
        # Score pour le monstre
        self.loot_amount = 0
        # Niveau
        self.level = 1
    
    def set_speed(self, speed):
        self.default_speed = speed
        # Vitesse
        self.velocity = random.randint(1,3)
    
    def set_loot_amount(self, amount):
        self.loot_amount = amount
    
    def forward_right(self):
        # Condition de collision avec joueur
        if not self.game.check_collision(self, self.game.all_players) and self.name == "alien":
            self.rect.x += self.velocity
        elif not self.game.check_collision(self, self.game.all_players):
            self.rect.x -= self.velocity
        else:
            self.game.player.damage(self.attack)
        
    def update_health_bar(self, surface):
        # Dessiner la bar de vie
        pygame.draw.rect(surface, (60, 63, 60), [self.rect.x + 10, self.rect.y - 20, self.max_health, 5])
        pygame.draw.rect(surface, (111, 210, 46), [self.rect.x + 10, self.rect.y - 20, self.health, 5])
    
    def update_animation(self):
        self.animate(loop=True)
    
    def damage(self, attack):
        # Enlever les degats infliges
        self.health -= attack
        # Condition de reapparition du monstre
        if self.health <= 0:
            self.rect.x = self.rect_start
            self.health = self.max_health
            self.velocity = random.randint(1, self.default_speed)
            # Ajouter points au score
            self.game.add_score(self.loot_amount)

            # Condition de barre a 100%
            if self.game.comet_event.is_full_loaded():
                # Supprimer monstre
                self.game.all_monsters.remove(self)
                # Essayer d'activer pluie de cometes
                self.game.comet_event.attempt_fall(self.screen)
    

# Classe representant la momie
class Mummy(Monster):
    
    def __init__(self, game, screen):
        super().__init__(game, screen, "mummy", (130, 130))
        self.set_speed(3)
        self.set_loot_amount(20)

# Classe representant l'alien
class Alien(Monster):
    
    def __init__(self, game, screen):
        super().__init__(game, screen, "alien", (300, 300), 130, 0 - random.randint(0, 300))
        self.health = 200
        self.max_health = 200
        self.attack = 0.8
        self.set_speed(1)
        self.set_loot_amount(50)