import pygame
import math
import constants as cts
from game_objects.gameobject import GameObject




class VelocityObject(GameObject):

	def __init__(self, pos: list, size: list, color: pygame.Color, vel: list):
		super().__init__(pos, size, color)
		self.vel = vel

	# Increments the players velocity by the specified x and y amounts
	def accelerate(self, force: tuple):
		self.vel = cts.add(self.vel, force)

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
		for chunk in obstacles:
			player_rect = pygame.Rect(round(self.pos[0]), round(self.pos[1]), self.size[0], self.size[1])
			chunk_rect = pygame.Rect(chunk[0], chunk[1], cts.CHUNKPIXELSIZE[0], cts.CHUNKPIXELSIZE[1])
			if player_rect.colliderect(chunk_rect):
				for obstacle in obstacles[chunk]:
					if player_rect.colliderect(obstacle):
						# Get amount of overlap and move the object back by that amount
						if (player_rect.centerx - obstacle.centerx) > 0: # Player moving left
							self.movex(obstacle.right - self.pos[0])
						else: # Player moving right
							self.movex(obstacle.left - (self.pos[0] + self.size[0]))
						self.vel[0] = 0.0

	# Check collision between an object and a list of obstacles
	def check_collisiony(self, obstacles: list):
		for chunk in obstacles:
			player_rect = pygame.Rect(round(self.pos[0]), round(self.pos[1]), self.size[0], self.size[1])
			chunk_rect = pygame.Rect(chunk[0], chunk[1], cts.CHUNKPIXELSIZE[0], cts.CHUNKPIXELSIZE[1])
			if player_rect.colliderect(chunk_rect):
				for obstacle in obstacles[chunk]:
					if player_rect.colliderect(obstacle):
						# Get amount of overlap and move the object back by that amount
						if (player_rect.centery - obstacle.centery) > 0: # Player moving up
							self.movey(obstacle.bottom - self.pos[1])
						else: # Player moving down
							self.movey(obstacle.top - (self.pos[1] + self.size[1]))
						self.vel[1] = 0.0
