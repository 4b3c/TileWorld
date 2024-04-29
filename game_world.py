import pygame
import os
import json
import constants as cts


def scramble(x: int, y: int, z: int) -> int:
	return (x + 100) * (y + 200) * (z + 300) % cts.SEED

def pxl_to_chunk(coordinates: list) -> tuple:
	return (int(coordinates[0] // cts.CHUNKPIXELSIZE[0]), int(coordinates[1] // cts.CHUNKPIXELSIZE[1]))

def pxl_to_tile(coordinates: list) -> tuple:
	return (int(coordinates[0] // cts.TILESIZE), int(coordinates[1] // cts.TILESIZE))


class Tile:

	def __init__(self, tile_id: int):
		self.tile_id = tile_id
		self.color = (tile_id % 255, 120, 160)
		self.changes = None
	
	# changes is a string containing all the modifications made to the tile in order 
	def modify(self, change: str):
		if (self.changes == None):
			self.changes = change
		else:
			self.changes += change


class Chunk:

	def __init__(self, pos: list, chunk_id: int):
		self.pos = pos
		self.chunk_id = chunk_id
		self.size = cts.CHUNKSIZE
		self.pxl_pos =  (cts.CHUNKPIXELSIZE[0] * self.pos[0], cts.CHUNKPIXELSIZE[1] * self.pos[1])
		self.tiles = {(x, y): Tile(scramble(x, y, chunk_id)) for x in range(self.size[0]) for y in range(self.size[1])}

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
		screen.blit(self.surface, (self.pxl_pos[0] - camera_offset[0], self.pxl_pos[1] - camera_offset[1]))
	
	# Allows for the modification of tiles
	def modify(self, tile: Tile, change: str):
		ts = cts.TILESIZE
		self.tiles[tile].modify(change)
		pygame.draw.rect(self.surface, cts.COLORS[change], (tile[0] * ts, tile[1] * ts, ts, ts))

	def get_save_dict(self) -> dict:
		save_list = {}
		for tile in self.tiles:
			if (self.tiles[tile].changes != None):
				save_list[str(tile)] = self.tiles[tile].changes
		if save_list == {}:
			return None
		return save_list




class Map:

	def __init__(self, savefile: str):
		self.savefile = savefile
		self.viewport_size = cts.WINDOWSIZE
		width, height = pxl_to_chunk(self.viewport_size)
		width += 2
		height += 2
		self.chunk_viewport_count = (width, height)
		
		# chunks is a dictionary of chunks where each key corresponds to the chunk at that location
		# rendered_chunks is a dictionary of viewable (or nearly in frame) chunks
		# each rendered_chunks key corresponds to a chunk's position within the viewport, not its actual position
		self.chunks = {(x, y): Chunk((x, y), scramble(x, y, cts.SEED)) for x in range(-8, 8) for y in range(-8, 8)}
		self.rendered_chunks = {(x, y): self.chunks[(x, y)] for x in range(0, width) for y in range(0, height)}

		# A dictionary for the order of iteration when shifting viewable chunks
		self.chunkshift = {
			(-1, "x"): range(self.chunk_viewport_count[0] - 1, -1, -1),
			(0, "x"): range(0, self.chunk_viewport_count[0], 1),
			(1, "x"): range(0, self.chunk_viewport_count[0], 1),
			(-1, "y"): range(self.chunk_viewport_count[1] - 1, -1, -1),
			(0, "y"): range(0, self.chunk_viewport_count[1], 1),
			(1, "y"): range(0, self.chunk_viewport_count[1], 1)
		}

		if (self.savefile in os.listdir(cts.SAVEFOLDER)):
			with open(cts.SAVEFOLDER + self.savefile, 'r') as f:
				chunkedits = json.load(f)
			for chunk in chunkedits:
				tuple_chunk = cts.str_to_tuple(chunk)
				if (tuple_chunk not in self.chunks):
					self.chunks[tuple_chunk] = Chunk(tuple_chunk, cts.SEED)
				for edit in chunkedits[chunk]:
					self.chunks[tuple_chunk].modify(cts.str_to_tuple(edit), chunkedits[chunk][edit])

		
	# Based upon the position of the camera, decides if we need to shift the dict of rendered chunks
	def update_pos(self, camera_offset: list):
		first_chunk_x, first_chunk_y = self.rendered_chunks[(0, 0)].pxl_pos
		final_index = (self.chunk_viewport_count[0] - 1, self.chunk_viewport_count[1] - 1)
		last_chunk_x, last_chunk_y = self.rendered_chunks[final_index].pxl_pos

		if (camera_offset[0] + self.viewport_size[0] > last_chunk_x + cts.CHUNKPIXELSIZE[0]): # Right unrendered
			self.shiftchunks(1, 0)
		elif (camera_offset[0] < first_chunk_x): # Left unrendered
			self.shiftchunks(-1, 0)
		elif (camera_offset[1] + self.viewport_size[1] > last_chunk_y + cts.CHUNKPIXELSIZE[1]): # Bottom unrendered
			self.shiftchunks(0, 1)
		elif (camera_offset[1] < first_chunk_y): # Top unrendered
			self.shiftchunks(0, -1)

	# Given the dict (grid) of rendered chunks, we move each row or column one step
	def shiftchunks(self, x: int, y: int):
		for col in self.chunkshift[(x, "x")]:
			for row in self.chunkshift[(y, "y")]:

				# Simply shift all the chunks in the rendering dictionary
				if (col + x, row + y) in self.rendered_chunks:
					self.rendered_chunks[col, row] = self.rendered_chunks[col + x, row + y]
					continue

				# For chunks on the edge of the dictionary, first check if they exist in the dict of all the chunks
				pos = self.rendered_chunks[col, row].pos
				if (pos[0] + x, pos[1] + y) in self.chunks:
					self.rendered_chunks[col, row] = self.chunks[pos[0] + x, pos[1] + y]
					continue

				# Lastly, if the chunk isn't in the dict of arrays, create a new chunk
				self.rendered_chunks[col, row] = Chunk([pos[0] + x, pos[1] + y], scramble(pos[0] + x, pos[1] + y, cts.SEED))

	# Draws each chunk in the rendered dictionary to the screen
	def draw_to(self, screen: pygame.Surface, camera_offset: list):
		for chunk in self.rendered_chunks:
			self.rendered_chunks[chunk].draw_to(screen, camera_offset)

	# Allows for the modification of tiles
	def modify(self, coordinates: list, change: str):
		chunk = pxl_to_chunk(coordinates)
		tile_x, tile_y = pxl_to_tile(coordinates)
		tile = (tile_x - (chunk[0] * cts.CHUNKSIZE[0]), tile_y - (chunk[1] * cts.CHUNKSIZE[1]))
		self.chunks[chunk].modify(tile, change)

	def save_to_file(self) -> dict:
		save_list = {}
		for chunk in self.chunks:
			if (self.chunks[chunk].get_save_dict() != None):
				save_list[str(chunk)] = self.chunks[chunk].get_save_dict()
		with open(cts.SAVEFOLDER + self.savefile, 'w') as f:
			json.dump(save_list, f, indent = 1)