import pygame
import constants as cts


def scramble(x: int, y: int, z: int) -> int:
	return (x + 1) * (y + 2) * (z + 3) % cts.SEED


class Tile:

	def __init__(self, tile_id: int):
		self.tile_id = tile_id
		self.color = (tile_id % 255, 120, 160)
		self.obstacle = False


class Chunk:

	def __init__(self, pos: list, chunk_id: int):
		self.pos = pos
		self.chunk_id = chunk_id
		self.size = cts.CHUNKSIZE
		self.pxl_size = (self.size[0] * cts.TILESIZE, self.size[1] * cts.TILESIZE)
		self.tiles = {(x, y): Tile(scramble(x, y, chunk_id)) for x in range(self.size[0]) for y in range(self.size[1])}

		self.surface = pygame.Surface(self.pxl_size)
		self.generate_surface()

	def generate_surface(self):
		ts = cts.TILESIZE
		for tile in self.tiles:
			pygame.draw.rect(self.surface, self.tiles[tile].color, (tile[0] * ts, tile[1] * ts, ts, ts))

