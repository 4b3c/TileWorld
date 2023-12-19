import constants
from tile import tileClass
import random
import numpy as np
import cv2
import pygame

class mapClass:
	def __init__(self, size, scale):
		self.size = size
		self.wid = size[0]
		self.hgt = size[1]
		self.scale = scale

		self.tiles = {(x, y): tileClass(random.choice(constants.terrains)) for x in range(size[0]) for y in range(size[1])}

	def gen_image(self, top_left_pos):
		self.img_size = (self.size[0] * self.scale, self.size[1] * self.scale, 3)
		self.img = np.zeros(self.img_size, dtype=np.uint8)
		scl = self.scale
		for tile_coord, tile_obj in self.tiles.items():
			x, y = tile_coord
			self.img[x * scl:(x + 1) * scl, y * scl:(y + 1) * scl] = tile_obj.color

		self.surface = pygame.surfarray.make_surface(self.img)
