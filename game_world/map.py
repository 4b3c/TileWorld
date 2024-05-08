import pygame
import json
import constants as cts
from game_world.chunk import Chunk


class Map:

	def __init__(self, savefile: str):
		self.savefile = savefile + "/world.json"
		# Add 1 chunk because pxl_to_chunk floors value, and add 3 more buffer chunks
		self.viewport_size = cts.add(cts.pxl_to_chunk(cts.WINDOWSIZE), (4, 4))
		print("Viewport size:", self.viewport_size)
		# Chunks is a dictionary of chunks where each key corresponds to the chunk at that location
		self.chunks = self.load_from_file()

	def initialize_scene(self, camera_offset: list):
		# Rendered_chunks is a list of viewable (or nearly in frame) chunks (index = [x][y])
		self.rendered_chunks = self.get_rendered_chunks(camera_offset)
		self.obstacles = self.get_obstacles()

	def load_from_file(self) -> dict:
		with open(cts.SAVEFOLDER + self.savefile, 'r') as f:
			chunkedits = json.load(f)
		# Create all chunks that were saved
		chunks = {cts.str_to_tuple(chunk): Chunk(cts.str_to_tuple(chunk)) for chunk in chunkedits}
		for chunk in chunks:
			# Generate all it's tiles so we can modify them correctly
			chunks[chunk].load_all_tiles()
			for edit in chunkedits[str(chunk)]:
				chunks[chunk].modify(cts.str_to_tuple(edit), chunkedits[str(chunk)][edit])
		return chunks
	
	def save_to_file(self) -> dict:
		save_list = {}
		for chunk in self.chunks:
			if (self.chunks[chunk].get_save_dict() != None):
				save_list[str(chunk)] = self.chunks[chunk].get_save_dict()
		with open(cts.SAVEFOLDER + self.savefile, 'w') as f:
			json.dump(save_list, f, indent = 1)

	def get_rendered_chunks(self, camera_offset: list) -> dict:
		fx, fy = cts.pxl_to_chunk(camera_offset)
		width, height = self.viewport_size
		return {(fx + x, fy + y): self.get_chunk((fx + x, fy + y)) for y in range(height) for x in range(width)}
		
	def get_chunk(self, pos: tuple) -> Chunk:
		return self.chunks[pos] if pos in self.chunks else Chunk(pos)

	# Based upon the position of the camera, decides if we need to shift the dict of rendered chunks
	def update_pos(self, camera_offset: list):
		keys = sorted(self.rendered_chunks.keys())
		first_chunk_x, first_chunk_y = self.rendered_chunks[keys[0]].pxl_pos
		last_chunk_x, last_chunk_y = self.rendered_chunks[keys[-1]].pxl_pos

		if (camera_offset[0] + self.viewport_size[0] > last_chunk_x - (2 * cts.CHUNKPIXELSIZE[0])): # Right unrendered
			self.shiftchunks(1, 0)
		elif (camera_offset[0] < first_chunk_x + cts.CHUNKPIXELSIZE[0]): # Left unrendered
			self.shiftchunks(-1, 0)
		elif (camera_offset[1] + self.viewport_size[1] > last_chunk_y - (2 * cts.CHUNKPIXELSIZE[1])): # Bottom unrendered
			self.shiftchunks(0, 1)
		elif (camera_offset[1] < first_chunk_y + cts.CHUNKPIXELSIZE[1]): # Top unrendered
			self.shiftchunks(0, -1)

	# Given the dict (grid) of rendered chunks, we move each row or column one step
	def shiftchunks(self, x: int, y: int):
		print("Shifting:", str((x, y)))
		keys = self.rendered_chunks.keys()
		keys_plus = [(key[0] + x, key[1] + y) for key in keys]
		keys_minus = [(key[0] - x, key[1] - y) for key in keys]

		for key in [key for key in keys_plus if key not in keys]: # Gets keys one forward in direction of movement
			self.rendered_chunks[key] = self.get_chunk(key)
		for key in [(key[0] + x, key[1] + y) for key in keys_minus if key not in keys]: # Gets keys oppsite movement
			self.rendered_chunks.pop(key)
		
		self.obstacles = self.get_obstacles()

	# Draws each chunk in the rendered dictionary to the screen
	def draw_to(self, screen: pygame.Surface, camera_offset: list):
		for chunk in self.rendered_chunks:
			self.rendered_chunks[chunk].draw_to(screen, camera_offset)

	# Allows for the modification of tiles
	def modify(self, coordinates: list, change: str):
		chunk = cts.pxl_to_chunk(coordinates)
		tile = tuple(cts.subtract(cts.pxl_to_tile(coordinates), cts.multiply(chunk, cts.CHUNKSIZE)))
		self.chunks[chunk].modify(tile, change)
		self.obstacles = self.get_obstacles()

	def demodify(self, coordinates: list):
		chunk = cts.pxl_to_chunk(coordinates)
		tile = tuple(cts.subtract(cts.pxl_to_tile(coordinates), cts.multiply(chunk, cts.CHUNKSIZE)))
		self.chunks[chunk].demodify(tile)
		self.obstacles = self.get_obstacles()

	def get_obstacles(self) -> list:
		# This is a nested loop because otherwise it would be a list of lists of obstacles, so we unpack the obstacle list too
		return [obstacle for chunk in self.rendered_chunks for obstacle in self.rendered_chunks[chunk].obstacles()]