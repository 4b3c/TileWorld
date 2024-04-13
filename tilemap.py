import math
import pygame
import json
import os
import constants as cts
from mapchunk import mapchunk as chunk

class tilemap():
	def __init__(self, pos, name):
		# Set windowpos which is a relative position and is how rendered chunk placement is calculated
		self.windowpos = pos
		self.vel = [0, 0]
		self.chunkatzero = (0, 0)
		self.name = name
		self.filename = self.name + ".json"

		# Load the modified chunks, or else create an empty dictionary for modified chunks
		# Creates a dictionary of rendered chunks where the key is their relative position (x, y)
		self.renderedchunks = {(x, y): chunk((x, y)) for x in range(-1, 3) for y in range(-1, 3)}

		# Rendered chunks are a 4x4 grid, where each chunk is half the width and height of the game window
		if (self.filename in os.listdir(cts.SAVEFOLDER)):
			self.loadchunks()
			self.addchunkstorender()
		else:
			self.chunks = {}
			self.savechunks()
	
	def setcolidable(self):
		self.colidable = []
		for chunk in self.renderedchunks:
			self.colidable += self.renderedchunks[chunk].getobstacles(chunk, self.windowpos)

	def loadchunks(self):
		with open(cts.SAVEFOLDER + self.filename, 'r') as f:
			chunksaves = json.load(f)
			self.chunks = {cts.strtup(pos): chunk(cts.strtup(pos), chunksaves[pos]) for pos in chunksaves}
		
	def savechunks(self):
		for renderedchunk in self.renderedchunks:
			self.chunks[self.renderedchunks[renderedchunk].pos] = self.renderedchunks[renderedchunk]
		chunksaves = {str(pos): self.chunks[pos].savestate() for pos in self.chunks}
		with open(cts.SAVEFOLDER + self.filename, 'w') as f:
			json.dump(chunksaves, f, indent = 0)

	def addchunkstorender(self):
		for x in range(-1, 3):
			for y in range(-1, 3):
				try:
					self.renderedchunks[(x, y)] = self.chunks[(x, y)]
				except:
					pass

	def draw(self, screen, character, mousepos, mousepressed):
		# Apply "friction" so movement slows to a stop smoothly
		self.vel = [self.vel[0] * (1 - cts.FRICTION), self.vel[1] * (1 - cts.FRICTION)]

		# Cap tha magnitude of the velocity to prevent diagonal movement from being faster than cardinal movement
		velmag = math.sqrt(self.vel[0]**2 + self.vel[1]**2)
		if (velmag > cts.MAXSPEED):
			self.vel = [self.vel[0] * cts.MAXSPEED / velmag, self.vel[1] * cts.MAXSPEED / velmag]

		self.move(self.vel)
		self.setcolidable()
		collided, moveback = self.checkcollisions(character)
		if (collided):
			self.move(moveback)

		# Draws each chunk based on its key (x, y) and multiplying that by it's size, then adding the window position
		for mapchunk in self.renderedchunks:
			xpos, ypos = cts.add(self.windowpos, cts.muliply(mapchunk, cts.CHUNKSIZE))
			screen.blit(self.renderedchunks[mapchunk], (xpos, ypos))
			if (mousepressed[0]):
				if (pygame.Rect(xpos, ypos, cts.CHUNKSIZE[0], cts.CHUNKSIZE[1]).collidepoint(mousepos)):
					tile = self.renderedchunks[mapchunk].tilepos((mousepos[0] - xpos, mousepos[1] - ypos))
					self.renderedchunks[mapchunk].changetile(tile)

		playerpos = cts.subtract(cts.CENTER, self.vel, cts.PLAYERSIZE)
		character.draw(screen, playerpos, velmag)


	def move(self, distance):
		# Updates the window position, but if we are near an edge of the rendered chunks, unloads and loads the necessary ones
		self.windowpos = cts.subtract(self.windowpos, distance)
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
					try:
						mapchunk = self.chunks[(col + self.chunkatzero[0] + x, row + self.chunkatzero[1] + y)]
					except:
						# TODO: instead of just creating a new chunk object, we need to load the correct one
						mapchunk = chunk((col + self.chunkatzero[0] + x, row + self.chunkatzero[1] + y))
				if (self.renderedchunks[(col, row)].ismodified()):
					self.chunks[(col + self.chunkatzero[0], row + self.chunkatzero[1])] = self.renderedchunks[(col, row)]
				self.renderedchunks[(col, row)] = mapchunk
		self.chunkatzero = cts.add(self.chunkatzero, (x, y))
		self.setcolidable()

	def checkcollisions(self, character):
		playerrect = pygame.Rect(character.pos[0], character.pos[1], 80, 80)
		moveback = [0, 0]
		maxmove = 10
		for wall in self.colidable:
			if playerrect.colliderect(wall):
				overlapleft = playerrect.right - wall.left
				overlapright = wall.right - playerrect.left
				overlaptop = playerrect.bottom - wall.top
				overlapbottom = wall.bottom - playerrect.top

				print(overlapleft, overlapright, overlaptop, overlapbottom)

				if (overlapleft < overlapright and overlapleft < maxmove):
					moveback[0] = -overlapleft
				elif (overlapright < maxmove):
					moveback[0] = overlapright
				
				if (overlaptop < overlapbottom and overlaptop < maxmove):
					moveback[1] = overlaptop
				elif (overlapbottom < maxmove):
					moveback[1] = -overlapbottom

				return True, moveback

		return False, moveback


