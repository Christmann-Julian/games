import pygame
from comet import Comet

class CometFallEvent:

    def __init__(self, game):
        # Pourcentage de la barre
        self.percent = 0
        self.percent_speed = 15
        # Groupe de comete
        self.all_comets = pygame.sprite.Group()
        self.game = game
        # Mode pluie de comete
        self.fall_mode = False
        self.level = 1
    
    def add_percent(self):
        self.percent += self.percent_speed / 100
    
    def is_full_loaded(self):
        # Barre d'evenement a 100%
        return self.percent >= 100
    
    def meteor_fall(self, screen):
        # Apparition boule de feu
        number_comet = 0
        while number_comet <= 15:
            self.all_comets.add(Comet(screen, self))
            number_comet += 1
    
    def attempt_fall(self, screen):
        # Conition de lancement des cometes
        if self.is_full_loaded() and len(self.game.all_monsters) == 0:
            print("pluie de comete")
            self.meteor_fall(screen)
            self.fall_mode = True

    def update_bar(self, screen):
        # Ajouter pourcentage a la barre
        if not self.is_full_loaded():
            self.add_percent()
        # barre de fond noir
        pygame.draw.rect(screen, (0, 0, 0), [(screen.get_width() / 3), 20, (screen.get_width() / 3), 10])
        # barre rouge
        pygame.draw.rect(screen, (111, 210, 46), [(screen.get_width() / 3), 20, ((screen.get_width() / 3) / 100) * self.percent, 10])