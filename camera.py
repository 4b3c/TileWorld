import pygame
import constants as cts
from game_objects.velocityobject import VelocityObject
from game_world.map import Map


class Camera:

	def __init__(self, follow: VelocityObject, world: Map):
		self.follow = follow
		self.world = world
		self.size = cts.WINDOWSIZE

		self.update_pos()
		self.world.initialize_scene(self.pos)

	def update_pos(self):
		self.centerpos = cts.add((round(self.follow.pos[0]), round(self.follow.pos[1])), cts.divide(self.follow.size, (2, 2)))
		self.pos = cts.subtract(self.centerpos, cts.CENTER)

	def update_scene(self, deltatime: float):
		# update the player's position and then check for collisions
		self.follow.update_xpos(cts.FRICTION, deltatime)
		self.follow.check_collisionx(self.world.obstacles)
		self.follow.update_ypos(cts.FRICTION, deltatime)
		self.follow.check_collisiony(self.world.obstacles)

		self.update_pos()
		self.world.update_pos(self.pos)

	def draw_scene(self, screen: pygame.Surface):
		screen.fill(cts.COLORS["water_blue"][0])
		self.world.draw_to(screen, self.pos)
		self.follow.draw_to(screen, self.pos)