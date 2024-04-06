import pygame
import math
import constants

class player:
	def __init__(self, pos, radius, color):
		self.pos = list(pos)
		self.vel = [0, 0]
		self.radius = radius
		self.color = color

		self.surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
		pygame.draw.circle(self.surface, self.color, (self.radius, self.radius), self.radius)

	def draw(self, screen):
		velmag = math.sqrt(self.vel[0]**2 + self.vel[1]**2)
		if (velmag > constants.MAXSPEED):
			self.vel = [self.vel[0] * constants.MAXSPEED / velmag, self.vel[1] * constants.MAXSPEED / velmag]
		self.pos[0] += self.vel[0];
		self.pos[1] += self.vel[1];
		self.vel = [self.vel[0] * (1 - constants.FRICTION), self.vel[1] * (1 - constants.FRICTION)]
		screen.blit(self.surface, self.pos)
