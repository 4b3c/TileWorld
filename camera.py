import pygame
import constants as cts
from game_objects import VelocityObject
from game_world import Map



class Camera:

	def __init__(self, follow: VelocityObject, world: Map):
		self.follow = follow
		self.world = world
		self.size = cts.WINDOWSIZE
		self.update_scene()
		
	def update_scene(self):
		self.follow.update_pos(cts.FRICTION)
		self.centerpos = [self.follow.pos[0] + self.follow.size[0], self.follow.pos[1] + self.follow.size[1]]
		self.pos = [self.centerpos[0] - cts.CENTER[0], self.centerpos[1] - cts.CENTER[1]]
		# self.pos = [0, 0] # For debugging purposes
		self.world.update_pos(self.pos)

	def draw_scene(self, screen: pygame.Surface):
		screen.fill(cts.COLORS["light_blue"])
		self.world.draw_to(screen, self.pos)
		self.follow.draw_to(screen, self.pos)