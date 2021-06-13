import pygame

class ItemBox(pygame.sprite.Sprite):
	def __init__(self, item_type, item_boxes, x, y, tile_size):
		pygame.sprite.Sprite.__init__(self)
		self.item_type = item_type
		self.image = item_boxes[self.item_type]
		self.rect = self.image.get_rect()
		self.rect.midtop = (x + tile_size // 2, y + (tile_size - self.image.get_height()))


	def update(self, player, screen_scroll):
		# Scroll
		self.rect.x += screen_scroll
		# Verifier si le joueur touche la boite 
		if pygame.sprite.collide_rect(self, player):
			# Condition pour savoir de quel boite il s'agit
			if self.item_type == 'Health':
				player.health += 30
				if player.health > player.max_health:
					player.health = player.max_health
			elif self.item_type == 'Ammo':
				player.ammo += 10
			elif self.item_type == 'Grenade':
				player.grenade += 3
			# Supprimer la boite
			self.kill()