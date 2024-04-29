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
		self.pos = cts.add(self.pos, [x, y])

	def draw_to(self, screen: pygame.Surface, camera_offset: list):
		screen.blit(self.surface, (round(self.pos[0] - camera_offset[0]), round(self.pos[1] - camera_offset[1])))


class VelocityObject(GameObject):

	def __init__(self, pos: list, size: list, color: pygame.Color, vel: list):
		super().__init__(pos, size, color)
		self.vel = vel

	def accelerate(self, x: float, y: float):
		self.vel = cts.add(self.vel, [x, y])

		velmag = math.sqrt(self.vel[0]**2 + self.vel[1]**2)
		if (velmag > cts.MAXSPEED):
			normal = cts.MAXSPEED / velmag
			self.vel = cts.multiply(self.vel, (normal, normal))

	def update_pos(self, friction: float):
		self.move(self.vel[0], self.vel[1])
		self.vel = cts.multiply(self.vel, (1 - friction, 1 - friction))


class Player(VelocityObject):

	def __init__(self, name: str) -> None:
		super().__init__([0.0, 0.0], cts.PLAYERSIZE, cts.COLORS["player"], [0.0, 0.0])
		self.name = name

	# Check collision between player and obstacles (TODO fix this)
	def check_collision(self, squares, camera_x, camera_y):
		for square in squares:
			if player_rect.colliderect(square):
				# Calculate the direction of the collision
				dx = player_rect.centerx - square.centerx
				dy = player_rect.centery - square.centery

				if debugprint:
					print(dx, dy)

				# Adjust camera position based on collision direction
				if abs(dx) > abs(dy):
					if dx > 0: # Player moving left
						camera_x += player_rect.x - square.right
					else: # Player moving right
						camera_x -= square.left - player_rect.right
				else:
					if dy > 0: # Player moving up
						camera_y += player_rect.y - square.bottom
					else: # Player moving down
						camera_y -= square.top - player_rect.bottom
		return camera_x, camera_y