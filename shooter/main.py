import pygame
from game import Game
from banner import Banner
pygame.init()

# Creation de la fenetre et de son nom
pygame.display.set_caption('Shooter game')
screen = pygame.display.set_mode((1080, 720))

# Chargement de l'image de fond
background = pygame.image.load('assets/bg.jpg')

# Nombre de FPS
clock = pygame.time.Clock()

# Chargement du jeu
game = Game(screen)
banner = Banner(screen)
running = True

while running:

    # Mise en place de l'image de fond et sauvegarde
    screen.blit(background, (0, -200))
    
    # Est ce que la partie a commence ?
    if game.is_playing:
        game.update(screen)
    # Chargement de la banniere et du bouton play
    else:
        banner.get_play_button()
        banner.get_banner()

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
            game.pressed[event.key] = True
            
            # Condition touche espace enfoncer faire boule de feu
            if event.key == pygame.K_e:
                game.player.fire_right()
            if event.key == pygame.K_a:
                game.player.fire_left()
            if event.key == pygame.K_SPACE and game.is_playing == False:
                game.start()
                # jouer le son
                game.sound_manager.play('click')
                
        # Condition touche relache
        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False
        
        # Condition clique souris
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Condition clique sur bouton play
            if banner.play_button_rect.collidepoint(event.pos) and game.is_playing == False:
                game.start()
                # jouer le son
                game.sound_manager.play('click')
    
    clock.tick(60)