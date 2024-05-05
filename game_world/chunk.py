import pygame
from game_world.tiles import Tile
import constants as cts

class Chunk:

	def __init__(self, pos: list):
		self.pos = pos
		self.size = cts.CHUNKSIZE
		self.pxl_pos = cts.multiply(cts.CHUNKPIXELSIZE, self.pos)
		self.first_tile = cts.multiply(self.pos, self.size)
		self.tiles = {(x, y): Tile(cts.add(self.first_tile, (x, y))) for x in range(self.size[0]) for y in range(self.size[1])}

		self.surface = pygame.Surface(cts.CHUNKPIXELSIZE)
		self.generate_surface()

	# Generates the pygame surface used for displaying to the screen
	def generate_surface(self):
		ts = cts.TILESIZE
		for tile in self.tiles:
			pygame.draw.rect(self.surface, self.tiles[tile].color, (tile[0] * ts, tile[1] * ts, ts, ts))

		# Add border and coordinate text for debugging purposes
		# pygame.draw.rect(self.surface, (40, 40, 40), (0, 0, cts.CHUNKPIXELSIZE[0], cts.CHUNKPIXELSIZE[0]), 2)
		# text_surface = cts.FONT.render(str(self.pos), True, (40, 40, 40))
		# text_rect = text_surface.get_rect()
		# text_rect.topleft = (15, 15)
		# self.surface.blit(text_surface, text_rect)

	# Draws the chunk to a given screen
	def draw_to(self, screen: pygame.Surface, camera_offset: list):
		screen.blit(self.surface, cts.subtract(self.pxl_pos, camera_offset))
	
	# Allows for the modification of tiles
	def modify(self, tile: Tile, change: str):
		ts = cts.TILESIZE
		self.tiles[tile].modify(change)
		pygame.draw.rect(self.surface, cts.COLORS[change], (tile[0] * ts, tile[1] * ts, ts, ts))

	def demodify(self, tile: Tile):
		ts = cts.TILESIZE
		self.tiles[tile].demodify()
		pygame.draw.rect(self.surface, self.tiles[tile].color, (tile[0] * ts, tile[1] * ts, ts, ts))

	def get_save_dict(self) -> dict:
		save_list = {}
		for tile in self.tiles:
			if (self.tiles[tile].changes != None):
				save_list[str(tile)] = self.tiles[tile].changes
		if save_list == {}:
			return None
		return save_list
	
	def obstacles(self) -> list:
		obstacle_list = []
		for tile in self.tiles:
			if (self.tiles[tile].changes != None):
				tile_x, tile_y = cts.add(cts.tile_to_pxl(tile), self.pxl_pos)
				obstacle_list.append(pygame.Rect(tile_x, tile_y, cts.TILESIZE, cts.TILESIZE))
		return obstacle_list