import pygame
from game_world.tiles import Tile
import constants as cts

class Chunk:

	def __init__(self, pos: list):
		self.pos = pos
		width, height = cts.CHUNKSIZE
		self.tiles_to_load = [tuple(cts.add(self.pos, cts.multiply((x, y), cts.TILESIZE))) for x in range(width) for y in range(height)]
		self.tiles = {}

		self.surface = pygame.Surface(cts.CHUNKPIXELSIZE)
		self.update_surface()

	# Generates the pygame surface used for displaying to the screen
	def update_surface(self):
		ts = cts.TILESIZE[0]
		for tile in self.tiles:
			pygame.draw.rect(self.surface, self.tiles[tile].color, (tile[0] - self.pos[0], tile[1] - self.pos[1], ts, ts))

		# Add border and coordinate text for debugging purposes
		# pygame.draw.rect(self.surface, (40, 40, 40), (0, 0, cts.CHUNKPIXELSIZE[0], cts.CHUNKPIXELSIZE[0]), 2)
		# text_surface = cts.FONT.render(str(self.pos), True, (40, 40, 40))
		# text_rect = text_surface.get_rect()
		# text_rect.topleft = (15, 15)
		# self.surface.blit(text_surface, text_rect)
  
	def load_next_tile(self):
		first_tile = self.tiles_to_load.pop(0)
		self.tiles[first_tile] = Tile(first_tile)
		self.update_surface()

	def load_all_tiles(self):
		while (self.tiles_to_load != []):
			self.load_next_tile()

	# Draws the chunk to a given screen
	def draw_to(self, screen: pygame.Surface, camera_offset: list):
		screen.blit(self.surface, cts.subtract(self.pos, camera_offset))
		if (self.tiles_to_load != []):
			self.load_next_tile()
	
	# Allows for the modification of tiles
	def modify(self, tile: Tile, change: str):
		ts = cts.TILESIZE
		self.tiles[tile].modify(change)
		pygame.draw.rect(self.surface, cts.COLORS[change], (tile[0] - self.pos[0], tile[1] - self.pos[1], ts[0], ts[1]))

	def demodify(self, tile: Tile):
		ts = cts.TILESIZE
		self.tiles[tile].demodify()
		pygame.draw.rect(self.surface, self.tiles[tile].color, (tile[0] - self.pos[0], tile[1] - self.pos[1], ts[0], ts[1]))

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
				obstacle_list.append(pygame.Rect(tile[0], tile[1], cts.TILESIZE[0], cts.TILESIZE[1]))
		return obstacle_list