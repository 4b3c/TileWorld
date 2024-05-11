import pygame
import random
import constants as cts
from game_world.generation import layered_perlin2d


class Tile:

	def __init__(self, pos: list):
		self.pos = pos
		self.val = layered_perlin2d(pos[0] / 3000, pos[1] / 3000)
		lightvdark = (pos[0] // cts.TILESIZE[0] + pos[1] // cts.TILESIZE[1]) % 2
		self.surface = pygame.Surface(cts.TILESIZE)

		random.seed(hash(self.pos))

		if (self.val > 0.65):
			self.surface.fill(cts.COLORS["stone_grey"][lightvdark])
		elif (self.val > 0.55):
			# self.surface.fill(cts.COLORS["forrest_green"][lightvdark])
			self.surface = cts.forrests[random.randint(0, len(cts.grasses) - 1)].copy()
		elif (self.val > 0.45):
			# self.surface.fill(cts.COLORS["field_green"][lightvdark])
			self.surface = cts.grasses[random.randint(0, len(cts.grasses) - 1)].copy()
		elif (self.val > 0.35):
			self.surface.fill(cts.COLORS["sand_tan"][lightvdark])
		else:
			self.surface.fill(cts.COLORS["water_blue"][lightvdark])

		self.changes = None
	
	# changes is a string containing all the modifications made to the tile in order 
	def modify(self, change: str):
		self.changes = change
		self.surface.fill(cts.COLORS[change])

	def demodify(self):
		self.changes = None
