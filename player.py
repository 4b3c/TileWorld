import pygame
import math
import constants as cts

class player:
	def __init__(self, pos, radius, color):
		self.pos = list(pos)
		self.vel = [0, 0]
		self.radius = radius
		self.color = color

		self.surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
		pygame.draw.circle(self.surface, self.color, (self.radius, self.radius), self.radius)

	def move(self, dist):
		self.pos = cts.add(self.pos, dist)

	def draw(self, screen, world):
		velmag = math.sqrt(self.vel[0]**2 + self.vel[1]**2)
		if (velmag > cts.MAXSPEED):
			self.vel = [self.vel[0] * cts.MAXSPEED / velmag, self.vel[1] * cts.MAXSPEED / velmag]
		if (self.pos[0] + self.vel[0] > cts.BOUNDSX[0] and self.pos[0] + self.vel[0] < cts.BOUNDSX[1] \
	  		and self.pos[1] + self.vel[1] > cts.BOUNDSY[0] and self.pos[1] + self.vel[1] < cts.BOUNDSY[1]):
			self.move(self.vel)
		else:
			world.move(self.vel)
		self.vel = [self.vel[0] * (1 - cts.FRICTION), self.vel[1] * (1 - cts.FRICTION)]
		screen.blit(self.surface, self.pos)
