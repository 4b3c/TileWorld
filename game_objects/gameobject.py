import pygame


class GameObject:

	def __init__(self, pos: list, size: list, color: pygame.Color):
		self.pos = pos
		self.size = size
		self.color = color
		self.surface = pygame.Surface(size)
		self.surface.fill(color)

	# Moves the object by the specified x increment
	def movex(self, x: float):
		self.pos[0] += x

	# Moves the object by the specified y increment
	def movey(self, y: float):
		self.pos[1] += y

	# Draws the object to the pygame window
	def draw_to(self, screen: pygame.Surface, camera_offset: list):
		screen.blit(self.surface, (round(self.pos[0] - camera_offset[0]), round(self.pos[1] - camera_offset[1])))