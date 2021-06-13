import pygame

# Classe representant le projectile
class Projectile(pygame.sprite.Sprite):
    
    def __init__(self, player):
        super().__init__()
        # Joueur
        self.player = player
        # Projectile image
        self.image = pygame.image.load('assets/projectile.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        # Position projectile
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x + 120
        self.rect.y = player.rect.y + 80
        # Vitesse
        self.velocity = 5
        # rotation
        self.origin_image = self.image
        self.angle = 0

    def rotate(self):
        self.angle += 8
        self.image = pygame.transform.rotozoom(self.origin_image, self.angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)

    def remove(self):
        self.player.all_fire_right.remove(self)
        self.player.all_fire_left.remove(self)
    
    def move_right(self):
        self.rect.x += self.velocity
        self.rotate()

        # Condition de collision et de dommage avec monstre
        for monster in self.player.game.check_collision(self, self.player.game.all_monsters):
            self.remove()
            monster.damage(self.player.attack)

        # Detruire le projectile quand il sort de map
        if self.rect.x > 1080:
            self.remove()
            

    def move_left(self):
        self.rect.x -= self.velocity
        self.rotate()

        # Condition de collision et de dommage avec monstre
        for monster in self.player.game.check_collision(self, self.player.game.all_monsters):
            self.remove()
            monster.damage(self.player.attack)

        # Detruire le projectile quand il sort de map
        if self.rect.x < 0:
            self.remove()