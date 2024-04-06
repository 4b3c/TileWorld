import pygame
import math
import constants as cts

class player:
	def __init__(self, pos, radius, color):
		# Set initial variables
		self.pos = list(pos)
		self.vel = [0, 0]
		self.radius = radius
		self.color = color

		# Create a transparent surface with a circle on to represent the player
		self.surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
		pygame.draw.circle(self.surface, self.color, (self.radius, self.radius), self.radius)

	def draw(self, screen, world):
		# Apply "friction" so the player slows to a stop smoothly
		self.vel = [self.vel[0] * (1 - cts.FRICTION), self.vel[1] * (1 - cts.FRICTION)]

		# Cap tha magnitude of the velocity to prevent diagonal movement from being faster than cardinal movement
		velmag = math.sqrt(self.vel[0]**2 + self.vel[1]**2)
		if (velmag > cts.MAXSPEED):
			self.vel = [self.vel[0] * cts.MAXSPEED / velmag, self.vel[1] * cts.MAXSPEED / velmag]

		world.move(self.vel)
		self.surface.fill(pygame.SRCALPHA)
		pygame.draw.circle(self.surface, self.color, (self.radius, self.radius), self.radius - velmag)
		screen.blit(self.surface, cts.add(self.pos, (self.vel[0] * 15, self.vel[1] * 15)))
