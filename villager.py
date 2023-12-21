import name
import numpy as np
import pygame

class villagerClass:
	def __init__(self):
		self.firstname = name.random_name()
		self.lastname = name.random_name()
		self.name = self.firstname + " " + self.lastname

		self.x = 400
		self.y = 200
		self.target_x = 900
		self.target_y = 100

		self.health = 100
		self.happiness = 100
		self.hunger = 0
		self.speed = 0.34
		self.education = 0
		self.traits = []
		self.inventory = []

		self.job = None
		self.home = None

	def gen_image(self, scale):
		self.scale = scale
		self.img_size = (int(1/8 * self.scale), int(1/5 * self.scale), 3)
		self.img = np.zeros(self.img_size, dtype=np.uint8)
		self.surface = pygame.surfarray.make_surface(self.img)

	def draw_to(self, surface, top_left_pos, delta_time):
		diff_x = self.target_x - self.x
		diff_y = self.target_y - self.y
		if abs(diff_x) > 0.499:
			self.x += (abs(diff_x) / diff_x) * self.speed * delta_time
		elif abs(diff_y) > 0.499:
			self.y += (abs(diff_y) / diff_y) * self.speed * delta_time

		surface.blit(self.surface, (self.x + top_left_pos[0], self.y + top_left_pos[1]))

	def move_to(self, coords):
		self.target_x = coords[0]
		self.target_y = coords[1]
