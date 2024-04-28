import pygame
import constants as cts


def scramble(x: int, y: int, z: int) -> int:
	return (x + 100) * (y + 200) * (z + 300) % cts.SEED


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
		self.pxl_pos =  (self.pxl_size[0] * self.pos[0], self.pxl_size[1] * self.pos[1])
		self.tiles = {(x, y): Tile(scramble(x, y, chunk_id)) for x in range(self.size[0]) for y in range(self.size[1])}

		self.surface = pygame.Surface(self.pxl_size)
		self.generate_surface()

	def generate_surface(self):
		ts = cts.TILESIZE
		for tile in self.tiles:
			pygame.draw.rect(self.surface, self.tiles[tile].color, (tile[0] * ts, tile[1] * ts, ts, ts))

	def draw_to(self, screen: pygame.Surface, camera_offset: list):
		screen.blit(self.surface, (self.pxl_pos[0] - camera_offset[0], self.pxl_pos[1] - camera_offset[1]))


class Map:

	def __init__(self, savefile: str):
		self.savefile = savefile
		self.pos = [0, 0]
		self.rendered_chunks = {(x, y): Chunk((x, y), scramble(x, y, cts.SEED)) for x in range(-1, 3) for y in range(-1, 3)}

	def draw_to(self, screen: pygame.Surface, camera_offset: list):
		for chunk in self.rendered_chunks:
			self.rendered_chunks[chunk].draw_to(screen, camera_offset)