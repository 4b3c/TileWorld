import pygame
import constants as cts

class mapchunk(pygame.Surface):
	def __init__(self, pos, modifications = None):
		super().__init__(cts.CHUNKSIZE)
		self.pos = pos
		if modifications == None:
			self.modifications = {}
		else:
			self.modifications = modifications
		self.checkerboard()
		self.applymodifications()

	def tilepos(self, pixelpos):
		return (int(pixelpos[0] / cts.TILESIZE), int(pixelpos[1] / cts.TILESIZE))
	
	def changetile(self, tilepos):
		ts = cts.TILESIZE
		pygame.draw.rect(self, (30, 30, 30), (tilepos[0] * ts, tilepos[1] * ts, ts, ts))
		self.modifications[tilepos] = (30, 30, 30)

	def checkerboard(self):
		ts = cts.TILESIZE
		for i in range(int(self.get_width() / ts) + 1):
			for j in range(int(self.get_height() / ts) + 1):
				if ((i + j) % 2 == 0):
					pygame.draw.rect(self, ((cts.SEED * self.pos[0] * self.pos[1] * i * j) % 255, 140, 180), (i * ts, j * ts, ts, ts))
				else:
					pygame.draw.rect(self, ((cts.SEED * i * j) % 255, 120, 160), (i * ts, j * ts, ts, ts))

	def applymodifications(self):
		ts = cts.TILESIZE
		for modification in self.modifications:
			posx, posy = cts.strtup(modification)
			pygame.draw.rect(self, self.modifications[modification], (posx * ts, posy * ts, ts, ts))

	def ismodified(self):
		return self.modifications == {}
	
	def savestate(self):
		return {str(mod): self.modifications[mod] for mod in self.modifications}