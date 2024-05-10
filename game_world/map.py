import pygame
import json
import os
import constants as cts
from game_world.chunk import Chunk


class Map:

	def __init__(self, savefile: str):
		if (savefile in os.listdir(cts.SAVEFOLDER)):
			self.savefile = savefile + "/world.json"
		else: # If the world doesn't already exist, we create a folder for it in the worlds directory
			os.mkdir(cts.SAVEFOLDER + savefile)
			self.savefile = savefile + "/world.json"
			with open(cts.SAVEFOLDER + self.savefile, 'w') as f: # Then we create a file for the world data
				json.dump({}, f, indent = 1)
			with open(cts.SAVEFOLDER + savefile + "/player.json", 'w') as f: # And a file for the player data
				json.dump({"pos": (0.0, 0.0)}, f, indent = 1)

		# Chunks is a dictionary of chunks where each key corresponds to the chunk at that location
		self.chunks = self.load_from_file()

	def initialize_scene(self, camera_offset: list):
		# Rendered_chunks is a list of viewable (or nearly in frame) chunks (index = [x][y])
		# It's initially set to only one chunk, because it will automatically adjust its size to what is needed
		center_chunk_pos = tuple(cts.pxl_to_chunk(camera_offset))
		self.rendered_chunks = {center_chunk_pos: self.get_chunk(center_chunk_pos)}
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
		
	def get_chunk(self, pos: tuple) -> Chunk:
		return self.chunks[pos] if pos in self.chunks else Chunk(pos)

	# Based upon the position of the camera, decides if we need to shift the dict of rendered chunks
	def update_pos(self, camera_offset: list):
		keys = sorted(self.rendered_chunks.keys())
		first_chunk_x, first_chunk_y = self.rendered_chunks[keys[0]].pos
		last_chunk_x, last_chunk_y = self.rendered_chunks[keys[-1]].pos

		if (camera_offset[0] + cts.WINDOWSIZE[0] > last_chunk_x - cts.CHUNKPIXELSIZE[0]): # Add chunks to the right
			self.add_to_render(cts.CHUNKPIXELSIZE[0], 0, keys)
		elif (camera_offset[0] + cts.WINDOWSIZE[0] < last_chunk_x - (2 * cts.CHUNKPIXELSIZE[0])): # Remove chunks from the right
			self.remove_from_render(-cts.CHUNKPIXELSIZE[0], 0, keys)

		elif (camera_offset[0] < first_chunk_x + cts.CHUNKPIXELSIZE[0]): # Add chunks to the left
			self.add_to_render(-cts.CHUNKPIXELSIZE[0], 0, keys)
		elif (camera_offset[0] > first_chunk_x + (2 * cts.CHUNKPIXELSIZE[0])): # Remove chunks from the left
			self.remove_from_render(cts.CHUNKPIXELSIZE[0], 0, keys)

		elif (camera_offset[1] + cts.WINDOWSIZE[1] > last_chunk_y - cts.CHUNKPIXELSIZE[1]): # Add chunks to the bottom
			self.add_to_render(0, cts.CHUNKPIXELSIZE[1], keys)
		elif (camera_offset[1] + cts.WINDOWSIZE[1] < last_chunk_y - (2 * cts.CHUNKPIXELSIZE[1])): # Remove chunks from the bottom
			self.remove_from_render(0, -cts.CHUNKPIXELSIZE[1], keys)

		elif (camera_offset[1] < first_chunk_y + cts.CHUNKPIXELSIZE[1]): # Add chunks to the top
			self.add_to_render(0, -cts.CHUNKPIXELSIZE[1], keys)
		elif (camera_offset[1] > first_chunk_y + (2 * cts.CHUNKPIXELSIZE[1])): # Remove chunks from the top
			self.remove_from_render(0, cts.CHUNKPIXELSIZE[1], keys)

	# Given the dict (grid) of rendered chunks, we move each row or column one step
	def add_to_render(self, x: int, y: int, keys: list):
		keys_plus = [(key[0] + x, key[1] + y) for key in keys]
		for key in [key for key in keys_plus if key not in keys]: # Gets keys one forward in direction of movement
			self.rendered_chunks[key] = self.get_chunk(key)

		self.obstacles = self.get_obstacles()

	def remove_from_render(self, x: int, y: int, keys: list):
		keys_minus = [(key[0] - x, key[1] - y) for key in keys]
		for key in [(key[0] + x, key[1] + y) for key in keys_minus if key not in keys]: # Gets keys oppsite movement
			self.rendered_chunks.pop(key)
		
		self.obstacles = self.get_obstacles()

	# Draws each chunk in the rendered dictionary to the screen
	def draw_to(self, screen: pygame.Surface, camera_offset: list):
		for chunk in self.rendered_chunks:
			self.rendered_chunks[chunk].draw_to(screen, camera_offset)

	# Allows for the modification of tiles
	def modify(self, coordinates: list, change: str):
		chunk = tuple(cts.pxl_to_chunk(coordinates))
		tile = tuple(cts.pxl_to_tile(coordinates))
		self.chunks[chunk] = self.rendered_chunks[chunk]
		self.chunks[chunk].modify(tile, change)
		self.obstacles = self.get_obstacles()

	def demodify(self, coordinates: list):
		chunk = tuple(cts.pxl_to_chunk(coordinates))
		tile = tuple(cts.pxl_to_tile(coordinates))
		self.chunks[chunk].demodify(tile)
		self.obstacles = self.get_obstacles()

	def get_obstacles(self) -> list:
		# This is a nested loop because otherwise it would be a list of lists of obstacles, so we unpack the obstacle list too
		return [obstacle for chunk in self.rendered_chunks for obstacle in self.rendered_chunks[chunk].obstacles()]