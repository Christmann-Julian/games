import pygame
import button
import csv
from pygame import mixer
from grenade import Grenade
from world import World

mixer.init()
pygame.init()

# Variable commune
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
scroll_thresh = 200
screen_scroll = 0
bg_scroll = 0
gravity = 0.75
rows = 16
cols = 150
tile_size = SCREEN_HEIGHT // rows
tile_type = 21
level = 1
max_level = 3
start_game = False

# Nombre de FPS
clock = pygame.time.Clock()

# Creation de la fenetre et de son nom
pygame.display.set_caption('Military game')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Charger musique
pygame.mixer.music.load('audio/music2.mp3')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1, 0.0, 5000)
jump_fx = pygame.mixer.Sound('audio/jump.wav')
jump_fx.set_volume(0.3)
shot_fx = pygame.mixer.Sound('audio/shot.wav')
shot_fx.set_volume(0.3)
grenade_fx = pygame.mixer.Sound('audio/grenade.wav')
grenade_fx.set_volume(0.5)

# Charger image de la map
# Mettre les tuiles dans une liste
img_list = []
for x in range(tile_type):
	img = pygame.image.load(f'img/tile/{x}.png')
	img = pygame.transform.scale(img, (tile_size, tile_size))
	img_list.append(img)

# Police d'ecriture
font = pygame.font.SysFont('Futura', 30)

# Images boutons
start_img = pygame.image.load('img/start_btn.png').convert_alpha()
exit_img = pygame.image.load('img/exit_btn.png').convert_alpha()
restart_img = pygame.image.load('img/restart_btn.png').convert_alpha()
# Images fond d'ecran
pine1_img = pygame.image.load('img/Background/pine1.png').convert_alpha()
pine2_img = pygame.image.load('img/Background/pine2.png').convert_alpha()
mountain_img = pygame.image.load('img/Background/mountain.png').convert_alpha()
sky_img = pygame.image.load('img/Background/sky_cloud.png').convert_alpha()

def draw_bg():
    screen.fill((135, 206, 235))
    width = sky_img.get_width()
    for x in range(5):
    	screen.blit(sky_img, ((x * width) - bg_scroll * 0.5, 0))
    	screen.blit(mountain_img, ((x * width) - bg_scroll * 0.6, SCREEN_HEIGHT - mountain_img.get_height() - 300))
    	screen.blit(pine1_img, ((x * width) - bg_scroll * 0.7, SCREEN_HEIGHT - pine1_img.get_height() - 150))
    	screen.blit(pine2_img, ((x * width) - bg_scroll * 0.8, SCREEN_HEIGHT - pine2_img.get_height()))

def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

# Fonction pour remettre a 0 le niveau
def reset_level():
	enemy_group.empty()
	bullet_group.empty()
	grenade_group.empty()
	explosion_group.empty()
	item_box_group.empty()
	decoration_group.empty()
	water_group.empty()
	exit_group.empty()

	# Creer une liste de tuile vide
	data = []
	for row in range(rows):
		r = [-1] * cols
		data.append(r)

	return data

# Joueur
move_right = False
move_left = False
shoot = False
grenade = False
grenade_thrown = False

# Creer buttons
start_button = button.Button(SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 - 150, start_img, 1)
exit_button = button.Button(SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 50, exit_img, 1)
restart_button = button.Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, restart_img, 2)

# Creation des groupes
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

# Creer une liste vide de tuiles
world_data = []
for row in range(rows):
	r = [-1] * cols
	world_data.append(r)

# Charger les infos du level et creer la map
with open(f'level/level{level}_data.csv', newline='') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	for x, row in enumerate(reader):
		for y, tile in enumerate(row):
			world_data[x][y] = int(tile)
world = World(screen, tile_size)
player, enemy, health_bar = world.process_data(world_data, img_list, water_group, decoration_group, enemy_group, item_box_group, exit_group)

running = True

while running:

    if start_game == False:
        # Fond d'ecran
        draw_bg()
        # Ajouter buttons
        if start_button.draw(screen):
        	start_game = True
        if exit_button.draw(screen):
        	running = False
    else:
        # Fond d'ecran
        draw_bg()
    
        # Dessine la MAP
        world.draw(screen_scroll)
        
        # Dessine le joueur
        player.update()
        player.draw()
    
        # Dessiner la bar de sante
        health_bar.draw(player.health)
    
        # Modifier et dessiner les groupes
        bullet_group.update(player, enemy, bullet_group, enemy_group, world, screen_scroll)
        grenade_group.update(gravity, explosion_group, player, enemy_group, tile_size, world, screen_scroll, grenade_fx)
        explosion_group.update(screen_scroll)
        item_box_group.update(player, screen_scroll)
        decoration_group.update(screen_scroll)
        water_group.update(screen_scroll)
        exit_group.update(screen_scroll)
        bullet_group.draw(screen)
        grenade_group.draw(screen)
        explosion_group.draw(screen)
        item_box_group.draw(screen)
        decoration_group.draw(screen)
        water_group.draw(screen)
        exit_group.draw(screen)
    
        # Munition texte
        draw_text('AMMO: ', font, (255, 255, 255), 10, 35)
        for x in range(player.ammo):
            screen.blit(pygame.image.load('img/icons/bullet.png').convert_alpha(), (90 + (x * 10), 40))
	    # Grenades texte
        draw_text('GRENADES: ', font, (255, 255, 255), 10, 60)
        for x in range(player.grenade):
            screen.blit(pygame.image.load('img/icons/grenade.png').convert_alpha(), (135 + (x * 15), 60))
    
        # Mise en place du groupe d'ennemies
        for enemy in enemy_group:
            enemy.ai(screen, player, bullet_group, gravity, tile_size, world, SCREEN_WIDTH, scroll_thresh, bg_scroll, screen_scroll, water_group, exit_group, SCREEN_HEIGHT, shot_fx)
            enemy.update()
            enemy.draw()
        
        # Changement d'animation
        if player.alive:
            # Animation tir
            if shoot:
                player.shoot(bullet_group, shot_fx)
            # Animation grenade
            elif grenade and grenade_thrown == False and player.grenade > 0:
                grenade = Grenade(player.rect.centerx + (0.5 * player.rect.size[0] * player.direction), player.rect.top, player.direction)
                grenade_group.add(grenade)
                grenade_thrown = True
                player.grenade -= 1
            # Animation joueur
            if player.in_air:
                player.update_action(2) # animation saut
            elif move_right or move_left:
                player.update_action(1) # animation deplacement
            else:
                player.update_action(0) # animation sur place
        else:
        	screen_scroll = 0
        	if restart_button.draw(screen):
        		bg_scroll = 0
        		world_data = reset_level()
        		# Charge les donnes du niveau et cree la map
        		with open(f'level/level{level}_data.csv', newline='') as csvfile:
        			reader = csv.reader(csvfile, delimiter=',')
        			for x, row in enumerate(reader):
        				for y, tile in enumerate(row):
        					world_data[x][y] = int(tile)
        		world = World(screen, tile_size)
        		player, enemy, health_bar = world.process_data(world_data, img_list, water_group, decoration_group, enemy_group, item_box_group, exit_group)
    
        # Deplacement du joueur
        screen_scroll, level_complete = player.move(move_right, move_left, gravity, world, SCREEN_WIDTH, scroll_thresh, bg_scroll, tile_size, screen_scroll, water_group, exit_group, SCREEN_HEIGHT)
        bg_scroll -= screen_scroll

        # Condition pour niveau suivant
        if level_complete:
            level += 1
            bg_scroll = 0
            world_data = reset_level()

            if level <= max_level:
                # Charge les donnes du niveau et cree la map
                with open(f'level/level{level}_data.csv', newline='') as csvfile:
                	reader = csv.reader(csvfile, delimiter=',')
                	for x, row in enumerate(reader):
                		for y, tile in enumerate(row):
                			world_data[x][y] = int(tile)
                world = World(screen, tile_size)
                player, enemy, health_bar = world.process_data(world_data, img_list, water_group, decoration_group, enemy_group, item_box_group, exit_group)
            else:
                start_game = False

    # Mettre à jour le jeu
    pygame.display.flip()
    
    for event in pygame.event.get():
        
        # Condition de fermeture du jeu
        if event.type == pygame.QUIT:
            running = False
            print('Fermeture du jeu')
            pygame.quit()
        
        # Condition touche enfoncer
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                move_right = True
            if event.key == pygame.K_LEFT:
                move_left = True
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_UP and player.alive:
                jump_fx.play()
                player.jump = True
            if event.key == pygame.K_DOWN and player.alive:
                grenade = True
        
        # Condition touche relache
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                move_right = False
            if event.key == pygame.K_LEFT:
                move_left = False
            if event.key == pygame.K_SPACE:
                shoot = False
            if event.key == pygame.K_DOWN:
                grenade = False
                grenade_thrown = False
    
    clock.tick(60)