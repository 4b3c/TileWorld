import pygame
import constants as cts

tile_size = 50

class tilemap():
	def __init__(self, pos):
		self.zero_pos = pos
		chunks = {(x, y): chunk(cts.CHUNKSIZE) for x in range(-1, 3) for y in range(-1, 3)}

		for chunk1 in chunks:
			print(chunk1, chunks[chunk1])


	def draw(self, screen):
		screen.blit(self.surface, self.pos)
      


class chunk(pygame.Surface):

	def checkerboard(self, color):
		for i in range(int(self.get_width() / tile_size) + 1):
			for j in range(int(self.get_height() / tile_size) + 1):
				if ((i + j) % 2 == 0):
					pygame.draw.rect(self, ((cts.SEED * i * j) % 255, (cts.SEED * i) % 255, (cts.SEED - i * j) % 255), (i * tile_size, j * tile_size, tile_size, tile_size))
				else:
					pygame.draw.rect(self, ((cts.SEED * i * j) % 255, 120, (cts.SEED + i * j) % 255), (i * tile_size, j * tile_size, tile_size, tile_size))



tilemap()