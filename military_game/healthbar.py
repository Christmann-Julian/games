import pygame

class HealthBar():
	def __init__(self, screen, health, max_health):
		self.screen = screen
		self.x = 10
		self.y = 10
		self.health = health
		self.max_health = max_health

	def draw(self, health):
		# Mettre la nouvelle sante
		self.health = health
		# Calculer le ratio de la bar
		ratio = self.health / self.max_health
		pygame.draw.rect(self.screen, (0, 0, 0), (self.x - 2, self.y - 2, 154, 24))
		pygame.draw.rect(self.screen, (255, 0, 0), (self.x, self.y, 150, 20))
		pygame.draw.rect(self.screen, (0, 255, 0), (self.x, self.y, 150 * ratio, 20))