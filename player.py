import pygame
import math
import constants as cts

class player:
	def __init__(self, pos, radius, color):
		# Set initial variables
		self.pos = list(pos)
		self.radius = radius
		self.color = color

		# Create a transparent surface with a circle on to represent the player
		self.surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
		pygame.draw.circle(self.surface, self.color, (self.radius, self.radius), self.radius)

	def draw(self, screen, pos, speed):
		# Reset the surface and draw a circle proportinal in size to the speed of the player
		self.surface.fill(pygame.SRCALPHA)
		pygame.draw.circle(self.surface, self.color, (self.radius, self.radius), self.radius - speed * 1.5)
		screen.blit(self.surface, (pos[0], pos[1]))
