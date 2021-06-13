from monster import Alien, Mummy, Monster
import pygame
import random

class Comet(pygame.sprite.Sprite):

    def __init__(self, screen, commet_event):
        super().__init__()
        # Classe comet_event
        self.comet_event = commet_event
        # Surface
        self.screen = screen
        # Image
        self.image = pygame.image.load('assets/comet.png')
        # Position
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(20, self.screen.get_width())
        self.rect.y = random.randint(0, self.screen.get_height() - 400)
        # Attaque
        self.attack = 20
        # Vitesse
        self.velocity = random.randint(1, 3)
        

    def fall(self):
        self.rect.y += self.velocity

        # Comete touche le sol
        if self.rect.y >= 500:
            # Retirer boule de feu
            self.remove()

            if len(self.comet_event.all_comets) == 0:
                self.comet_event.percent = 0
                self.comet_event.fall_mode = False
        
        if self.comet_event.game.check_collision(self, self.comet_event.game.all_players):
            self.remove()
            self.comet_event.game.player.damage(self.attack)
        
    def remove(self):
        self.comet_event.all_comets.remove(self)
        # jouer le son
        self.comet_event.game.sound_manager.play('meteorite')

        # Verifier le nombre de comete
        if len(self.comet_event.all_comets) == 0:
            # Remetre la barre a 0
            self.comet_event.percent = 0
            # Faire apparaitre les monstres
            if self.comet_event.level == 1:
                # Niveau 2: 1 alien
                self.comet_event.game.spawn_monster(Alien)
                self.comet_event.level += 1
            elif self.comet_event.level == 2:
                # Niveau 3: 1 momie et 1 alien
                self.comet_event.game.spawn_monster(Mummy)
                self.comet_event.game.spawn_monster(Alien)
                self.comet_event.level += 1
            elif self.comet_event.level == 3:
                # Niveau 3: 6 momies
                number_monsters = 0
    
                while number_monsters <= 6:
                    self.comet_event.game.spawn_monster(Mummy)
                    number_monsters += 1
                
                self.comet_event.level += 1
            elif self.comet_event.level == 4:
                # Niveau 4: 2 aliens
                number_monsters = 0
    
                while number_monsters < 2:
                    self.comet_event.game.spawn_monster(Alien)
                    number_monsters += 1
                
                self.comet_event.level += 1
            elif self.comet_event.level >= 5:
                # Niveau 4: 1 aliens et 2 momies
                number_monsters = 0
    
                while number_monsters <= 2:
                    self.comet_event.game.spawn_monster(Mummy)
                    number_monsters += 1
                
                self.comet_event.game.spawn_monster(Alien)
                
                self.comet_event.level += 1
