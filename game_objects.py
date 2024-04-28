import pygame
import math
import constants as cts


class GameObject:

	def __init__(self, pos: list, size: list, color: pygame.Color):
		self.pos = pos
		self.size = size
		self.color = color
		self.surface = pygame.Surface(size)
		self.surface.fill(color)

	def move(self, x: float, y: float):
		self.pos[0] += x
		self.pos[1] += y

	def draw_to(self, screen: pygame.Surface, camera_offset: list):
		screen.blit(self.surface, (round(self.pos[0] - camera_offset[0]), round(self.pos[1] - camera_offset[1])))


class VelocityObject(GameObject):

	def __init__(self, pos: list, size: list, color: pygame.Color, vel: list):
		super().__init__(pos, size, color)
		self.vel = vel

	def accelerate(self, x: float, y: float):
		self.vel[0] = self.vel[0] + x
		self.vel[1] = self.vel[1] + y

		velmag = math.sqrt(self.vel[0]**2 + self.vel[1]**2)
		if (velmag > cts.MAXSPEED):
			self.vel[0] = self.vel[0] * cts.MAXSPEED / velmag
			self.vel[1] = self.vel[1] * cts.MAXSPEED / velmag

	def update_pos(self, friction: float):
		self.move(self.vel[0], self.vel[1])

		self.vel[0] *= (1 - friction)
		self.vel[1] *= (1 - friction)


class Player(VelocityObject):

	def __init__(self, name: str) -> None:
		super().__init__([0.0, 0.0], cts.PLAYERSIZE, cts.COLORS["player"], [0.0, 0.0])
		self.name = name