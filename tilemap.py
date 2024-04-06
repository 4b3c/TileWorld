import pygame
import constants as cts


class tilemap():
	def __init__(self, pos):
		# Set windowpos which is a relative position and is how rendered chunk placement is calculated
		self.windowpos = pos
		
		# Creates a dictionary of rendered chunks where the key is their relative position (x, y)
		# Rendered chunks are a 4x4 grid, where each chunk is half the width and height of the game window
		self.chunks = {(x, y): chunk(cts.CHUNKSIZE) for x in range(-1, 3) for y in range(-1, 3)}
		for mapchunk in self.chunks:
			self.chunks[mapchunk].checkerboard()

	def draw(self, screen):
		# Draws each chunk based on its key (x, y) and multiplying that by it's size, then adding the window position
		for mapchunk in self.chunks:
			screen.blit(self.chunks[mapchunk], cts.add(self.windowpos, cts.muliply(mapchunk, cts.CHUNKSIZE)))
    
	def move(self, dist):
		# Updates the window position, but if we are near an edge of the rendered chunks, unloads and loads the necessary ones
		self.windowpos = cts.subtract(self.windowpos, dist)
		if (self.windowpos[0] < 0):
			self.windowpos[0] += cts.CHUNKSIZE[0]
			self.shiftchunks(-1, 0)
		elif (self.windowpos[0] > cts.CHUNKSIZE[0]):
			self.windowpos[0] -= cts.CHUNKSIZE[0]
			self.shiftchunks(1, 0)

		if (self.windowpos[1] < 0):
			self.windowpos[1] += cts.CHUNKSIZE[1]
			self.shiftchunks(0, -1)
		elif (self.windowpos[1] > cts.CHUNKSIZE[1]):
			self.windowpos[1] -= cts.CHUNKSIZE[1]
			self.shiftchunks(0, 1)


	def shiftchunks(self, x, y):
		# Given the 4x4 grid of rendered chunks, we move each row and/or column to the one behind it
		for col in cts.CHUNKSHIFT[x]:
			for row in cts.CHUNKSHIFT[y]:
				# This fails if we try to move a row/column behind the first one or after the last one 
				try:
					mapchunk = self.chunks[(row + x, col + y)]
					print("worked:", end="")
				except:
					# TODO: instead of just creating a new chunk object, we need to load the correct one
					mapchunk = chunk(cts.CHUNKSIZE)
					mapchunk.checkerboard()
					print("failed:", end="")
				self.chunks[(row, col)] = mapchunk
				print((row, col), (row + x, col + y))


class chunk(pygame.Surface):
	def checkerboard(self):
		ts = cts.TILESIZE
		for i in range(int(self.get_width() / ts) + 1):
			for j in range(int(self.get_height() / ts) + 1):
				if ((i + j) % 2 == 0):
					pygame.draw.rect(self, ((cts.SEED * i * j) % 255, 140, 180), (i * ts, j * ts, ts, ts))
				else:
					pygame.draw.rect(self, ((cts.SEED * i * j) % 255, 120, 160), (i * ts, j * ts, ts, ts))
