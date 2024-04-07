from typing import Any
import pygame
import constants as cts

ts = cts.TILESIZE
cs = cts.CHUNKSIZE

class mapchunk(pygame.Surface):
	def __init__(self, pos, modifications = None):
		super().__init__(cs)
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
		pygame.draw.rect(self, cts.COLORS["light_grey"], (tilepos[0] * ts, tilepos[1] * ts, ts, ts))
		self.modifications[tilepos] = "light_grey"

	def checkerboard(self):
		for i in range(int(self.get_width() / ts) + 1):
			for j in range(int(self.get_height() / ts) + 1):
				if ((i + j) % 2 == 0):
					pygame.draw.rect(self, ((cts.SEED * self.pos[0] * self.pos[1] * i * j) % 255, 140, 180), (i * ts, j * ts, ts, ts))
				else:
					pygame.draw.rect(self, ((cts.SEED * i * j) % 255, 120, 160), (i * ts, j * ts, ts, ts))

	def applymodifications(self):
		for modification in self.modifications:
			posx, posy = cts.strtup(modification)
			pygame.draw.rect(self, cts.COLORS[self.modifications[modification]], (posx * ts, posy * ts, ts, ts))
			pygame.draw.rect(self, (130, 130, 130), (posx * ts + 4, posy * ts + 4, ts - 8, ts - 8))

	def ismodified(self):
		return self.modifications != {}
	
	def savestate(self):
		return {str(mod): self.modifications[mod] for mod in self.modifications}
	
	def getrect(self, windowpos):
		return pygame.Rect(self.pos[0] * cs[0] + windowpos[0], self.pos[1] * cs[1] + windowpos[1], ts, ts)
	
	def getobstacles(self, renderpos, windowpos):
		modifiedtiles = [cts.strtup(mod) for mod in self.modifications]
		xpos = (renderpos[0] * cs[0]) + windowpos[0]
		ypos = (renderpos[1] * cs[1]) + windowpos[1]
		return [pygame.Rect(xpos + (tile[0] * ts) , ypos + (tile[1] * ts) , ts, ts) for tile in modifiedtiles]