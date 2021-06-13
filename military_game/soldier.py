import pygame
import math
import os
import random
from bullet import Bullet

# Classe representant le joueur
class Soldier(pygame.sprite.Sprite):
    
    def __init__(self, screen, char_type, x, y, ammo = 20, grenade = 0):
        super().__init__()
        # Joueur ou ennemie ?
        self.char_type = char_type
        # Surface
        self.screen = screen
        # Animation
        self.animation_list = []
        self.update_time = pygame.time.get_ticks()
        self.frame_index = 0
        self.action = 0
        # Image
        self.scale = 2
        self.image = self.animation()
        # Position
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        # Vitesse
        self.speed = 5
        self.vel_y = 0
        # Deplacement
        self.direction = 1
        self.flip = False
        # Sante
        self.alive = True
        self.health = 100
        self.max_health = 100
        # Saut
        self.jump = False
        self.in_air = True
        # Tir
        self.shoot_cooldown = 0
        self.ammo = ammo
        self.start_ammo = ammo
        # Grenade
        self.grenade = grenade
        # IA
        self.move_counter = 0
        self.idling = False
        self.idling_counter = 0
        self.vision = pygame.Rect(0, 0, 150, 20)

    def update(self):
        self.update_animation()
        self.check_alive()

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
    
    def draw(self):
        self.screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
    
    def shoot(self, bullet_group, shot_fx):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            # Ajoute un ecart de temps entre chaque tir
            self.shoot_cooldown = 20
            # Positionne le tir
            bullet = Bullet(self.rect.centerx + (0.75 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
            bullet_group.add(bullet)
            # Retire une munition
            self.ammo -= 1
            # Musique
            shot_fx.play()
    

    
    def check_alive(self):
        # verifier la mort
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)
    
    def move(self, move_right, move_left, gravity, world, SCREEN_WIDTH, scroll_thresh, bg_scroll, tile_size, screen_scroll, water_group, exit_group, SCREEN_HEIGHT):
        # Remettre les mouvements a 0
        screen_scroll = 0
        dx = 0
        dy = 0

        # Condition pour assigner mouvement
        # Droite
        if move_right:
            dx = self.speed
            self.direction = 1
            self.flip = False
        # Gauche
        if move_left:
            dx = - self.speed
            self.direction = -1
            self.flip = True
        # Saut
        if self.jump == True and self.in_air == False:
            self.vel_y = -11
            self.jump = False
            self.in_air = True
        
        # Gravite pour le saut
        self.vel_y += gravity
        if self.vel_y > 10:
            self.vel_y
        dy = self.vel_y

        # Verifier collision
        for tile in world.obstacle_list:
            # Verifier collision en x
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
            	dx = 0
            # Verifier collision en y
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
            	# Verifier collision avec le plafond pendant un saut
            	if self.vel_y < 0:
            		self.vel_y = 0
            		dy = tile[1].bottom - self.rect.top
            	# Verifier collision avec 
            	elif self.vel_y >= 0:
            		self.vel_y = 0
            		self.in_air = False
            		dy = tile[1].top - self.rect.bottom
        
        # Verifier collission avec l'eau
        if pygame.sprite.spritecollide(self, water_group, False):
        	self.health = 0

		# Verifier collission avec panneau de fin
        level_complete = False
        if pygame.sprite.spritecollide(self, exit_group, False):
            level_complete = True

		# verifier si tomber hors de la map
        if self.rect.bottom > SCREEN_HEIGHT:
        	self.health = 0
        
        # verifier si atteint la fin de l'ecran
        if self.char_type == 'player':
            if self.rect.left + dx < 0 or self.rect.right + dx > SCREEN_WIDTH:
                dx = 0

		# Changer la position du joueur
        self.rect.x += dx
        self.rect.y += dy

		# Changer le scroll en se basant sur la position du joueur
        if self.char_type == 'player':
        	if (self.rect.right > SCREEN_WIDTH - scroll_thresh and bg_scroll < (world.level_length * tile_size) - SCREEN_WIDTH)\
        		or (self.rect.left < scroll_thresh and bg_scroll > abs(dx)):
        		self.rect.x -= dx
        		screen_scroll = -dx
                
        return screen_scroll, level_complete

    def ai(self, screen, player, bullet_group, gravity, tile_size, world, SCREEN_WIDTH, scroll_thresh, bg_scroll, screen_scroll, water_group, exit_group, SCREEN_HEIGHT, shot_fx):
        # Change la vitesse
        self.speed = 1
        # Verifier si le joueur et l'ennemie sont en vie
        if self.alive and player.alive:
            # Mettre en inactif aleatoirement
            if self.idling == False and random.randint(1, 200) == 1:
                self.update_action(0)
                self.idling = True
                self.idling_counter = 50
            
            # verifier
            if self.vision.colliderect(player.rect):
				# Arreter de courir et faire face au joueur
                self.update_action(0)
				# Tirer
                self.shoot(bullet_group, shot_fx)
            else:
                # Verifier si actif
                if self.idling == False:
                    # Changer le deplacement
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    
                    ai_moving_left = not ai_moving_right
        
                    # Deplacement et animation
                    self.move(ai_moving_right, ai_moving_left, gravity, world, SCREEN_WIDTH, scroll_thresh, bg_scroll, tile_size, screen_scroll, water_group, exit_group, SCREEN_HEIGHT)
                    self.update_action(1)
                    self.move_counter += 1
                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)
        
                    # Verifier le temps pour faire demie tour
                    if self.move_counter >= tile_size:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
    
                    # Si le temps est ecoule passer en actif
                    if self.idling_counter <= 0:
                        self.idling = False
        #scroll
        self.rect.x += screen_scroll
    
    def animation(self):
        # Mettre toute les images dans animation_list
        # Action sur place = 0 Action courir = 1 Action sauter = 2 Action mourir = 3
        animation_type = ['Idle', 'Run', 'Jump', 'Death']
        
        for animation in animation_type:   
            # Vider temporairement la liste d'image
            temp_list = []
            # compter le nombre d'image dans le dossier
            number_of_frame = len(os.listdir(f'img/{self.char_type}/{animation}'))

            for i in range(number_of_frame):
                image = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png').convert_alpha()
                image = pygame.transform.scale(image, (math.ceil(image.get_width() * self.scale), math.ceil(image.get_height() * self.scale)))
                temp_list.append(image)
            self.animation_list.append(temp_list)
        
        return self.animation_list[self.action][self.frame_index]
    
    def update_animation(self):
        # vitesse de l'animation
        ANIMATION_COOLDOWN = 100

        self.image = self.animation_list[self.action][self.frame_index]

        # Verifier si assez de temps est passe pour mettre a jour l'animation
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            # Passe a l'image suivante
            self.frame_index += 1
            # Reinitialise le temps
            self.update_time = pygame.time.get_ticks()

        # Verifier si l'animation est finie pour recommencer
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
    
    def update_action(self, new_action):
        # Verifier si l'action est differrent de la precedante
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
