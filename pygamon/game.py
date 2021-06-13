from player import Player
import pygame
import pytmx
import pyscroll

class Game:

    def __init__(self):
        # Creer la fenetre et le nom du jeux
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Pygamon - Aventure")

        # Charger le fichier tmx
        tmx_data = pytmx.util_pygame.load_pygame('carte.tmx')
        # Charge l'image de la map
        map_data = pyscroll.data.TiledMapData(tmx_data)
        # Charge et superpose les calques sur la surface d'affichage (self.screen.get_size)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        self.map = ''

        # Generer joueur
        player_position = tmx_data.get_object_by_name("player")
        self.player = Player(player_position.x, player_position.y)

        # liste des rectangles de collision
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # Dessiner le groupe de calque
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        # Dessiner le groupe de joueur
        self.group.add(self.player)

        # Rectangle de collision pour entrer dans la maison
        enter_house = tmx_data.get_object_by_name('enter_house')
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)

        # Rectangle de collision pour entrer dans la maison
        enter_house_2 = tmx_data.get_object_by_name('enter_house_2')
        self.enter_house_2_rect = pygame.Rect(enter_house_2.x, enter_house_2.y, enter_house_2.width, enter_house_2.height)

        # collision panneau
        pannel = tmx_data.get_object_by_name('pannel')
        self.pannel_rect = pygame.Rect(pannel.x, pannel.y, pannel.width, pannel.height)
    
    def handle_input(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]:
            self.player.move_up()
            self.player.change_animation('up')
        elif pressed[pygame.K_DOWN]:
            self.player.move_down()
            self.player.change_animation('down')
        elif pressed[pygame.K_LEFT]:
            self.player.move_left()
            self.player.change_animation('left')
        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()
            self.player.change_animation('right')

    def switch_house(self):
        # Charger la carte
        tmx_data = pytmx.util_pygame.load_pygame('house.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        # liste des rectangles de collision
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # Dessiner le groupe de calque
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        self.group.add(self.player)

        # Rectangle de collision pour entrer dans la maison
        enter_house = tmx_data.get_object_by_name('exit_house')
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)

        # Recuperer le point de spawn
        spawn_house = tmx_data.get_object_by_name('spawn_house')
        self.spawn_house_rect = pygame.Rect(spawn_house.x, spawn_house.y, spawn_house.width, spawn_house.height)
        self.player.position[0] = spawn_house.x
        self.player.position[1] = spawn_house.y - 20

    def switch_house_2(self):
        # Charger la carte
        tmx_data = pytmx.util_pygame.load_pygame('house2.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        # liste des rectangles de collision
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # Dessiner le groupe de calque
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        self.group.add(self.player)

        # Rectangle de collision pour entrer dans la maison
        enter_house = tmx_data.get_object_by_name('exit_house')
        self.enter_house_2_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)

        # Recuperer le point de spawn
        spawn_house = tmx_data.get_object_by_name('spawn_house')
        self.spawn_house_rect = pygame.Rect(spawn_house.x, spawn_house.y, spawn_house.width, spawn_house.height)
        self.player.position[0] = spawn_house.x
        self.player.position[1] = spawn_house.y - 20
    
    def switch_world(self):
        # Charger la carte
        tmx_data = pytmx.util_pygame.load_pygame('carte.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        # liste des rectangles de collision
        self.walls = []

        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # Dessiner le groupe de calque
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)
        self.group.add(self.player)

        # Rectangle de collision pour entrer dans la maison
        enter_house = tmx_data.get_object_by_name('enter_house')
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)
        # Rectangle de collision pour entrer dans la maison
        enter_house_2 = tmx_data.get_object_by_name('enter_house_2')
        self.enter_house_2_rect = pygame.Rect(enter_house_2.x, enter_house_2.y, enter_house_2.width, enter_house_2.height)

        enter_house_exit = ''

        if self.map == 'house':
            enter_house_exit = 'enter_house_exit'
        
        if self.map == 'house2':
            enter_house_exit = 'enter_house_exit_2'

        # Recuperer le point de spawn
        spawn_house = tmx_data.get_object_by_name(enter_house_exit)
        self.spawn_house_rect = pygame.Rect(spawn_house.x, spawn_house.y, spawn_house.width, spawn_house.height)
        self.player.position[0] = spawn_house.x
        self.player.position[1] = spawn_house.y + 20
        

    def update(self):
        self.group.update()

        # Verification entrer de la maison
        if self.player.feet.colliderect(self.enter_house_rect):
            self.switch_house()
            self.map = 'house'

        # Verification entrer de la maison
        if self.player.feet.colliderect(self.enter_house_2_rect):
            self.switch_house_2()
            self.map = 'house2'

        # Verification entrer de la maison
        if self.player.feet.colliderect(self.enter_house_rect):
            self.switch_world()

        # Verification entrer de la maison
        if self.player.feet.colliderect(self.enter_house_2_rect):
            self.switch_world()

        # Verification de collision
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()

    def run(self):
        # Nombre de FPS
        clock = pygame.time.Clock()

        # Boucle du jeu
        running = True
        
        while running:
            self.player.save_location()
            self.handle_input()
            self.update()
            self.group.center(self.player.rect.center)
            self.group.draw(self.screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            clock.tick(60)
        
        pygame.quit()
