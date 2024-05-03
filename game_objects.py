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

	# Moves the object by the specified x increment
	def movex(self, x: float):
		self.pos[0] += x

	# Moves the object by the specified y increment
	def movey(self, y: float):
		self.pos[1] += y

	# Draws the object to the pygame window
	def draw_to(self, screen: pygame.Surface, camera_offset: list):
		screen.blit(self.surface, (round(self.pos[0] - camera_offset[0]), round(self.pos[1] - camera_offset[1])))


class VelocityObject(GameObject):

	def __init__(self, pos: list, size: list, color: pygame.Color, vel: list):
		super().__init__(pos, size, color)
		self.vel = vel

	# Increments the players velocity by the specified x and y amounts
	def accelerate(self, x: float, y: float):
		self.vel = cts.add(self.vel, [x, y])

		# Caps the velocity magnitude so that the max is the same even with diagonal movement
		velmag = math.sqrt(self.vel[0]**2 + self.vel[1]**2)
		if (velmag > cts.MAXSPEED):
			normal = cts.MAXSPEED / velmag
			self.vel = cts.multiply(self.vel, (normal, normal))

	# Moves the object by its velocity, and then applies friction
	def update_xpos(self, friction: float, deltatime: float):
		self.movex(self.vel[0] * deltatime)
		self.vel[0] *= (1 - friction)

	# Moves the object by its velocity, and then applies friction
	def update_ypos(self, friction: float, deltatime: float):
		self.movey(self.vel[1] * deltatime)
		self.vel[1] *= (1 - friction)

	# Check collision between an object and a list of obstacles
	def check_collisionx(self, obstacles: list):
		for obstacle in obstacles:
			rect = pygame.Rect(round(self.pos[0]), round(self.pos[1]), self.size[0], self.size[1])
			if rect.colliderect(obstacle):
				# Get amount of overlap and move the object back by that amount
				if (rect.centerx - obstacle.centerx) > 0: # Player moving left
					self.movex(obstacle.right - self.pos[0])
				else: # Player moving right
					self.movex(obstacle.left - (self.pos[0] + self.size[0]))
				self.vel[0] = 0.0

	# Check collision between an object and a list of obstacles
	def check_collisiony(self, obstacles: list):
		for obstacle in obstacles:
			rect = pygame.Rect(round(self.pos[0]), round(self.pos[1]), self.size[0], self.size[1])
			if rect.colliderect(obstacle):
				# Get amount of overlap and move the object back by that amount
				if (rect.centery - obstacle.centery) > 0: # Player moving up
					self.movey(obstacle.bottom - self.pos[1])
				else: # Player moving down
					self.movey(obstacle.top - (self.pos[1] + self.size[1]))
				self.vel[1] = 0.0


class Player(VelocityObject):

	def __init__(self, name: str) -> None:
		super().__init__([0.0, 0.0], cts.PLAYERSIZE, cts.COLORS["player"], [0.0, 0.0])
		self.name = name