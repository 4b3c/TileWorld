import pygame
from game_objects import VelocityObject
import constants as cts



class Camera:

	def __init__(self, follow: VelocityObject):
		self.follow = follow
		self.size = cts.WINDOWSIZE
		self.update_pos()
		
	def update_pos(self):
		self.follow.update_pos(cts.FRICTION)
		self.centerpos = [self.follow.pos[0] + self.follow.size[0], self.follow.pos[1] + self.follow.size[1]]
		self.pos = [self.centerpos[0] - cts.CENTER[0], self.centerpos[1] - cts.CENTER[1]]

	def draw_scene(self, screen: pygame.Surface):
		screen.fill(cts.COLORS["light_blue"])
		self.follow.draw_to(screen, self.pos)