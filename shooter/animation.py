import pygame
import random

class AnimateSprite(pygame.sprite.Sprite):

    def __init__(self, sprite_name, size=(200, 200)):
        super().__init__()
        # Taille image
        self.size = size
        # Image
        self.image = pygame.image.load(f'assets/{sprite_name}.png')
        self.image = pygame.transform.scale(self.image, self.size)
        self.images = animations.get(sprite_name)
        # Image actuelle
        self.current_image = 0
        # Animation en cour ?
        self.animation = False
    
    def start_animation(self):
        self.animation = True

    def animate(self, loop=False):

        if self.animation:
            # Passe a l'image suivante
            self.current_image += random.randint(0, 1)
    
            # Verifie si on atteint la fin de l'animation
            if self.current_image >= len(self.images):
                # Recommence a la premiere image
                self.current_image = 0

                # Verifie si l'animation n'est pas en mode boucle
                if loop is False:
                    # Desactive l'animation
                    self.animation = False
            
            # Modifier l'image
            self.image = self.images[self.current_image]
            self.image = pygame.transform.scale(self.image, self.size)

def load_animation_images(sprite_name):
        # Chargement des 24 images de l'animation
        images = []
        # Recuperer chemin du dossier pou ce sprite
        path = f"assets/{sprite_name}/{sprite_name}"

        for num in range(1, 24):
            image_path = path + str(num) + ".png"
            images.append(pygame.image.load(image_path))
        
        return images

animations = {
    'mummy': load_animation_images('mummy'),
    'player': load_animation_images('player'),
    'alien': load_animation_images('alien'),
}