import pygame
import constants as cts


class tilemap():
	def __init__(self, pos):
		self.zero_pos = pos
		self.chunks = {(x, y): chunk(cts.CHUNKSIZE) for x in range(-1, 3) for y in range(-1, 3)}

		for mapchunk in self.chunks:
			self.chunks[mapchunk].checkerboard()

	def draw(self, screen):
		for mapchunk in self.chunks:
			screen.blit(self.chunks[mapchunk], cts.add(self.zero_pos, cts.muliply(mapchunk, cts.CHUNKSIZE)))
    
	def move(self, dist):
		self.zero_pos = cts.subtract(self.zero_pos, dist)
		if (self.zero_pos[0] < 0):
			self.zero_pos[0] += cts.CHUNKSIZE[0]
			self.shiftchunks(-1, 0)
		elif (self.zero_pos[0] > cts.CHUNKSIZE[0]):
			self.zero_pos[0] -= cts.CHUNKSIZE[0]
			self.shiftchunks(1, 0)

		if (self.zero_pos[1] < 0):
			self.zero_pos[1] += cts.CHUNKSIZE[1]
			self.shiftchunks(0, -1)
		elif (self.zero_pos[1] > cts.CHUNKSIZE[1]):
			self.zero_pos[1] -= cts.CHUNKSIZE[1]
			self.shiftchunks(0, 1)


	def shiftchunks(self, x, y):
		for col in cts.CHUNKSHIFT[x]:
			for row in cts.CHUNKSHIFT[y]:
				try:
					mapchunk = self.chunks[(row + x, col + y)]
					print("worked:", end="")
				except:
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
