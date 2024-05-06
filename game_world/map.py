import pygame
import os
import json
import constants as cts
from game_world.chunk import Chunk


class Map:

	def __init__(self, savefile: str):
		self.savefile = savefile + ".json"
		self.viewport_size = cts.WINDOWSIZE
		width, height = cts.pxl_to_chunk(self.viewport_size)
		width += 2
		height += 2
		self.chunk_viewport_count = (width, height)
		
		# chunks is a dictionary of chunks where each key corresponds to the chunk at that location
		# rendered_chunks is a dictionary of viewable (or nearly in frame) chunks
		# each rendered_chunks key corresponds to a chunk's position within the viewport, not its actual position
		self.chunks = {(x, y): Chunk((x, y)) for x in range(-4, 4) for y in range(-4, 4)}
		self.rendered_chunks = {(x, y): self.chunks[(x, y)] for x in range(0, width) for y in range(0, height)}
		self.obstacles = []
		self.update_obstacles()

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
			# Iterate over every chunk that has been modified
			for chunk in chunkedits:
				tuple_chunk = cts.str_to_tuple(chunk)
				# Create it, if it isnt in the defaultly loaded ones
				if (tuple_chunk not in self.chunks):
					self.chunks[tuple_chunk] = Chunk(tuple_chunk)
				# Generate all it's tiles so we can modify them correctly
				self.chunks[tuple_chunk].load_all_tiles()
				for edit in chunkedits[chunk]:
					self.chunks[tuple_chunk].modify(cts.str_to_tuple(edit), chunkedits[chunk][edit])

		
	# Based upon the position of the camera, decides if we need to shift the dict of rendered chunks
	def update_pos(self, camera_offset: list):
		first_chunk_x, first_chunk_y = self.rendered_chunks[(0, 0)].pxl_pos
		final_index = tuple(cts.subtract(self.chunk_viewport_count, (1, 1)))
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
					self.update_obstacles()
					continue

				# Lastly, if the chunk isn't in the dict of arrays, create a new chunk
				self.rendered_chunks[col, row] = Chunk([pos[0] + x, pos[1] + y])

	# Draws each chunk in the rendered dictionary to the screen
	def draw_to(self, screen: pygame.Surface, camera_offset: list):
		for chunk in self.rendered_chunks:
			self.rendered_chunks[chunk].draw_to(screen, camera_offset)

	# Allows for the modification of tiles
	def modify(self, coordinates: list, change: str):
		chunk = cts.pxl_to_chunk(coordinates)
		tile = tuple(cts.subtract(cts.pxl_to_tile(coordinates), cts.multiply(chunk, cts.CHUNKSIZE)))
		self.chunks[chunk].modify(tile, change)
		self.update_obstacles()

	def demodify(self, coordinates: list):
		chunk = cts.pxl_to_chunk(coordinates)
		tile = tuple(cts.subtract(cts.pxl_to_tile(coordinates), cts.multiply(chunk, cts.CHUNKSIZE)))
		self.chunks[chunk].demodify(tile)
		self.update_obstacles()

	def save_to_file(self) -> dict:
		save_list = {}
		for chunk in self.chunks:
			if (self.chunks[chunk].get_save_dict() != None):
				save_list[str(chunk)] = self.chunks[chunk].get_save_dict()
		with open(cts.SAVEFOLDER + self.savefile, 'w') as f:
			json.dump(save_list, f, indent = 1)

	def update_obstacles(self):
		self.obstacles = [obstacle for chunk in self.rendered_chunks for obstacle in self.rendered_chunks[chunk].obstacles()]