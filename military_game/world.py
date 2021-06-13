import pygame
from soldier import Soldier
from itembox import ItemBox
from healthbar import HealthBar

class World():
    def __init__(self, screen, tile_size):
        # Surafce
        self.screen = screen
        # Taille des tuiles
        self.tile_size = tile_size
        # Liste d'obstacle
        self.obstacle_list = []
        # Image
        health_box_img = pygame.image.load('img/icons/health_box.png').convert_alpha()
        ammo_box_img = pygame.image.load('img/icons/ammo_box.png').convert_alpha()
        grenade_box_img = pygame.image.load('img/icons/grenade_box.png').convert_alpha()
        self.item_boxes = {
        	'Health'	: health_box_img,
        	'Ammo'		: ammo_box_img,
        	'Grenade'	: grenade_box_img
        }

    def process_data(self, data, img_list, water_group, decoration_group, enemy_group, item_box_group, exit_group):
        self.level_length = len(data[0])
		#iterate through each value in level data file
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * self.tile_size
                    img_rect.y = y * self.tile_size
                    tile_data = (img, img_rect)
                if tile >= 0 and tile <= 8:
                    self.obstacle_list.append(tile_data)
                elif tile >= 9 and tile <= 10:
                    water = Water(img, x * self.tile_size, y * self.tile_size, self.tile_size)
                    water_group.add(water)
                elif tile >= 11 and tile <= 14:
                    decoration = Decoration(img, x * self.tile_size, y * self.tile_size, self.tile_size)
                    decoration_group.add(decoration)
                elif tile == 15:# Creer joueur
                    player = Soldier(self.screen, 'player', x * self.tile_size, y * self.tile_size, 15, 3)
                    health_bar = HealthBar(self.screen, player.health, player.max_health)
                elif tile == 16:# Creer enemies
                	enemy = Soldier(self.screen, 'enemy', x * self.tile_size, y * self.tile_size, 15)
                	enemy_group.add(enemy)
                elif tile == 17:#create ammo box
                	item_box = ItemBox('Ammo', self.item_boxes, x * self.tile_size, y * self.tile_size, self.tile_size)
                	item_box_group.add(item_box)
                elif tile == 18:#create grenade box
                	item_box = ItemBox('Grenade', self.item_boxes, x * self.tile_size, y * self.tile_size, self.tile_size)
                	item_box_group.add(item_box)
                elif tile == 19:#create health box
                	item_box = ItemBox('Health', self.item_boxes, x * self.tile_size, y * self.tile_size, self.tile_size)
                	item_box_group.add(item_box)
                elif tile == 20:#create exit
                	exit = Exit(img, x * self.tile_size, y * self.tile_size, self.tile_size)
                	exit_group.add(exit)
            
        return player, enemy, health_bar


    def draw(self, screen_scroll):
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll
            self.screen.blit(tile[0], tile[1])


class Decoration(pygame.sprite.Sprite):
	def __init__(self, img, x, y, tile_size):
		pygame.sprite.Sprite.__init__(self)
		self.image = img
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + tile_size // 2, y + (tile_size - self.image.get_height()))

	def update(self, screen_scroll):
		self.rect.x += screen_scroll


class Water(pygame.sprite.Sprite):
	def __init__(self, img, x, y, tile_size):
		pygame.sprite.Sprite.__init__(self)
		self.image = img
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + tile_size // 2, y + (tile_size - self.image.get_height()))

	def update(self, screen_scroll):
		self.rect.x += screen_scroll

class Exit(pygame.sprite.Sprite):
	def __init__(self, img, x, y, tile_size):
		pygame.sprite.Sprite.__init__(self)
		self.image = img
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + tile_size // 2, y + (tile_size - self.image.get_height()))

	def update(self, screen_scroll):
		self.rect.x += screen_scroll