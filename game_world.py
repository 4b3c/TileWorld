import pygame
import os
import constants as cts

pygame.init()
font = pygame.font.Font(None, 36)

def scramble(x: int, y: int, z: int) -> int:
	return (x + 100) * (y + 200) * (z + 300) % cts.SEED

def pxl_to_chunk(coordinates: list):
		return (coordinates[0] // cts.CHUNKPIXELSIZE[0], coordinates[1] // cts.CHUNKPIXELSIZE[1])

def chunk_to_pxl(coordinates: list):
		return (coordinates[0] * cts.CHUNKPIXELSIZE[0], coordinates[1] * cts.CHUNKPIXELSIZE[1])


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
		self.pxl_pos =  (cts.CHUNKPIXELSIZE[0] * self.pos[0], cts.CHUNKPIXELSIZE[1] * self.pos[1])
		self.tiles = {(x, y): Tile(scramble(x, y, chunk_id)) for x in range(self.size[0]) for y in range(self.size[1])}

		self.surface = pygame.Surface(cts.CHUNKPIXELSIZE)
		self.generate_surface()

	def generate_surface(self):
		ts = cts.TILESIZE
		for tile in self.tiles:
			pygame.draw.rect(self.surface, self.tiles[tile].color, (tile[0] * ts, tile[1] * ts, ts, ts))

		# Add border and coordinate text
		pygame.draw.rect(self.surface, (40, 40, 40), (0, 0, cts.CHUNKPIXELSIZE[0], cts.CHUNKPIXELSIZE[0]), 2)
		text_surface = font.render(str(self.pos), True, (40, 40, 40))
		text_rect = text_surface.get_rect()
		text_rect.topleft = (15, 15)
		self.surface.blit(text_surface, text_rect)

	def draw_to(self, screen: pygame.Surface, camera_offset: list):
		screen.blit(self.surface, (self.pxl_pos[0] - camera_offset[0], self.pxl_pos[1] - camera_offset[1]))


class Map:

	def __init__(self, savefile: str):
		self.savefile = savefile
		self.viewport_size = cts.WINDOWSIZE
		width, height = pxl_to_chunk(self.viewport_size)
		self.chunk_viewport_count = (width + 2, height + 2)

		self.chunkshift_x = {
			-1: range(self.chunk_viewport_count[0] - 1, -1, -1),
			0: range(0, self.chunk_viewport_count[0], 1),
			1: range(0, self.chunk_viewport_count[0], 1)
		}

		self.chunkshift_y = {
			-1: range(self.chunk_viewport_count[1] - 1, -1, -1),
			0: range(0, self.chunk_viewport_count[1], 1),
			1: range(0, self.chunk_viewport_count[1], 1)
		}

		# # World has already been created, so load from a file
		# if (self.filename in os.listdir(cts.SAVEFOLDER)):
		# 	self.chunks = self.load_chunks()
		# # Create chunks for the first time
		# else:
			
		self.chunks = {(x, y): Chunk((x, y), scramble(x, y, cts.SEED)) for x in range(-8, 8) for y in range(-8, 8)}
		self.rendered_chunks = {}
		self.get_rendered([0, 0])

	# Gets all chunks in view based upon the camera offset and viewing size
	def get_rendered(self, camera_offset: list):
		offset = pxl_to_chunk(camera_offset)
		for x in range(0, self.chunk_viewport_count[0]):
			for y in range(0, self.chunk_viewport_count[1]):
				if (x + offset[0], y + offset[1]) in self.chunks:
					self.rendered_chunks[(x, y)] = self.chunks[(x + offset[0], y + offset[1])]
				else:
					self.rendered_chunks[(x, y)] = Chunk((x, y), scramble(x, y, cts.SEED))

	def update_pos(self, camera_offset: list):
		first_chunk_x, first_chunk_y = self.rendered_chunks[(0, 0)].pxl_pos
		final_index = (self.chunk_viewport_count[0] - 1, self.chunk_viewport_count[1] - 1)
		last_chunk_x, last_chunk_y = self.rendered_chunks[final_index].pxl_pos
		if (camera_offset[0] < first_chunk_x): # Left unrendered
			self.shiftchunks(-1, 0)
		elif (camera_offset[0] + self.viewport_size[0] > last_chunk_x + cts.CHUNKPIXELSIZE[0]): # Right unrendered
			self.shiftchunks(1, 0)
		elif (camera_offset[1] < first_chunk_y): # Top unrendered
			self.shiftchunks(0, -1)
		elif (camera_offset[1] + self.viewport_size[1] > last_chunk_y + cts.CHUNKPIXELSIZE[1]): # Bottom unrendered
			self.shiftchunks(0, 1)

	def shiftchunks(self, x: int, y: int):
		# Given the grid of rendered chunks, we move each row and/or column to the one behind it
		for col in self.chunkshift_x[x]:
			for row in self.chunkshift_y[y]:

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

	def draw_to(self, screen: pygame.Surface, camera_offset: list):
		for chunk in self.rendered_chunks:
			self.rendered_chunks[chunk].draw_to(screen, camera_offset)
