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

		self.health = 100
		self.happiness = 100
		self.hunger = 0
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

	def draw_to(self, window):
		window.blit(self.surface, (self.x, self.y))
