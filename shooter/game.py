import pygame
from sounds import SoundManager
from player import Player
from monster import Mummy, Alien
from comet_event import CometFallEvent

class Game:

    def __init__(self, screen):
        # Surface
        self.screen = screen
        # Jeu a commence ?
        self.is_playing = False
        # Chargement du joueur
        self.all_players = pygame.sprite.Group()
        self.player = Player(self)
        self.all_players.add(self.player)
        self.pressed = {}
        # Groupe de monstre
        self.all_monsters = pygame.sprite.Group()
        # Generer evenement
        self.comet_event = CometFallEvent(self)
        # Score
        self.score = 0
        self.font = pygame.font.SysFont("monospace", 25)
        # Gerer le son
        self.sound_manager = SoundManager()

    def start(self):
        print("start game")
        # lance le jeu
        self.is_playing = True
        # Groupe de monstre
        self.spawn_monster(Mummy)
        self.spawn_monster(Mummy)
        self.spawn_monster(Mummy)
    
    def game_over(self):
        print("game over")
        # Recree un groupe de monstres et ecrase le precedant
        self.all_monsters = pygame.sprite.Group()
        # Recree un groupe de cometes et ecrase le precedant
        self.comet_event.all_comets = pygame.sprite.Group()
        # Reinitialise le joueur
        self.player.health = self.player.max_health
        self.player.rect.x = 425
        # Reinitialise la barre temps
        self.comet_event.percent = 0
        # Retourne au menu
        self.is_playing = False
        # Reinitialise le score
        self.score = 0
        # Reinitialise les niveaux
        self.comet_event.level = 1
        # jouer le son
        self.sound_manager.play('game_over')
    
    def add_score(self, points=0):
        self.score += points
    
    def update(self, screen):
        # Mise en place du score
        score_text = self.font.render(f"Score : {self.score}", 1, (255,255,255))
        screen.blit(score_text, (20, 20))

        # Mise en place du joueur
        screen.blit(self.player.image, self.player.rect)
    
        # Actualiser la bar de vie du joueur
        self.player.update_health_bar(screen)

        # Actualiser l'animation joueur
        self.player.update_animation()

        # Actualiser la bar d'evenement du jeu
        self.comet_event.update_bar(screen)
    
        # Recuperer les projectiles
        for projectile in self.player.all_fire_right: 
            projectile.move_right()
    
        for projectile in self.player.all_fire_left:    
            projectile.move_left()
        
        # Recuperer les monstres
        for monster in self.all_monsters: 
            monster.forward_right()
            monster.update_health_bar(screen)
            monster.update_animation()
        
        # Recuperer les cometes
        for comet in self.comet_event.all_comets: 
            comet.fall()
        
        # Mise en place des images du groupe de projectiles
        self.player.all_fire_right.draw(screen)
        self.player.all_fire_left.draw(screen)
    
        # Mise en place des images du groupe de monstres
        self.all_monsters.draw(screen)

        # Mise en place des images de cometes
        self.comet_event.all_comets.draw(screen)
    
        # Quel touche est utilise ?
        if self.pressed.get(pygame.K_RIGHT) and self.player.rect.x + self.player.rect.width < screen.get_width():
            self.player.move_right()
        elif self.pressed.get(pygame.K_LEFT) and self.player.rect.x > 0:
            self.player.move_left()
        
    def spawn_monster(self, monster_name):
        self.all_monsters.add(monster_name.__call__(self, self.screen))
    
    def check_collision(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)