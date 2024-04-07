import pygame
import constants as cts

class tilemap():
	def __init__(self, pos):
		# Set windowpos which is a relative position and is how rendered chunk placement is calculated
		self.windowpos = pos
		self.chunkatzero = (0, 0)
		
		# Creates a dictionary of rendered chunks where the key is their relative position (x, y)
		# Rendered chunks are a 4x4 grid, where each chunk is half the width and height of the game window
		self.renderedchunks = {(x, y): chunk(cts.CHUNKSIZE, (x, y)) for x in range(-1, 3) for y in range(-1, 3)}
		for mapchunk in self.renderedchunks:
			self.renderedchunks[mapchunk].checkerboard()
			print(mapchunk)

	def draw(self, screen, mousepos, mousepressed):
		# Draws each chunk based on its key (x, y) and multiplying that by it's size, then adding the window position
		for mapchunk in self.renderedchunks:
			xpos, ypos = cts.add(self.windowpos, cts.muliply(mapchunk, cts.CHUNKSIZE))
			screen.blit(self.renderedchunks[mapchunk], (xpos, ypos))
			if (mousepressed[0] and pygame.Rect(xpos, ypos, cts.CHUNKSIZE[0], cts.CHUNKSIZE[1]).collidepoint(mousepos)):
				tile = self.renderedchunks[mapchunk].tile((mousepos[0] - xpos, mousepos[1] - ypos))
				self.renderedchunks[mapchunk].changetile(tile)
				print("Mouse clicked in chunk:", self.renderedchunks[mapchunk].pos, "in tile:", tile)

	def move(self, dist):
		# Updates the window position, but if we are near an edge of the rendered chunks, unloads and loads the necessary ones
		self.windowpos = cts.subtract(self.windowpos, dist)
		if (self.windowpos[0] < 0):
			self.windowpos[0] += cts.CHUNKSIZE[0]
			self.shiftchunks(1, 0)
		elif (self.windowpos[0] > cts.CHUNKSIZE[0]):
			self.windowpos[0] -= cts.CHUNKSIZE[0]
			self.shiftchunks(-1, 0)

		if (self.windowpos[1] < 0):
			self.windowpos[1] += cts.CHUNKSIZE[1]
			self.shiftchunks(0, 1)
		elif (self.windowpos[1] > cts.CHUNKSIZE[1]):
			self.windowpos[1] -= cts.CHUNKSIZE[1]
			self.shiftchunks(0, -1)

	def shiftchunks(self, x, y):
		# Given the 4x4 grid of rendered chunks, we move each row and/or column to the one behind it
		for col in cts.CHUNKSHIFT[x]:
			for row in cts.CHUNKSHIFT[y]:
				mapchunk = None
				# This fails if we try to move a row/column behind the first one or after the last one 
				try:
					mapchunk = self.renderedchunks[(col + x, row + y)]
				except:
					# TODO: instead of just creating a new chunk object, we need to load the correct one
					mapchunk = chunk(cts.CHUNKSIZE, (col + self.chunkatzero[0] + x, row + self.chunkatzero[1] + y))
					mapchunk.checkerboard()
				self.renderedchunks[(col, row)] = mapchunk
		self.chunkatzero = cts.add(self.chunkatzero, (x, y))

class chunk(pygame.Surface):
	def __init__(self, size, pos):
		super().__init__(size)
		self.pos = pos

	def tile(self, pixelpos):
		return (int(pixelpos[0] / cts.TILESIZE), int(pixelpos[1] / cts.TILESIZE))
	
	def changetile(self, tilepos):
		ts = cts.TILESIZE
		pygame.draw.rect(self, (30, 30, 30), (tilepos[0] * ts, tilepos[1] * ts, ts, ts))

	def checkerboard(self):
		ts = cts.TILESIZE
		for i in range(int(self.get_width() / ts) + 1):
			for j in range(int(self.get_height() / ts) + 1):
				if ((i + j) % 2 == 0):
					pygame.draw.rect(self, ((cts.SEED * i * j) % 255, 140, 180), (i * ts, j * ts, ts, ts))
				else:
					pygame.draw.rect(self, ((cts.SEED * i * j) % 255, 120, 160), (i * ts, j * ts, ts, ts))
