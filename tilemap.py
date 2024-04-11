import pygame
import json
import os
import constants as cts
from mapchunk import mapchunk as chunk

class tilemap():
	def __init__(self, pos, name):
		# Set windowpos which is a relative position and is how rendered chunk placement is calculated
		self.windowpos = pos
		self.chunkatzero = (0, 0)
		self.name = name
		self.filename = self.name + ".json"

		# Load the modified chunks, or else create an empty dictionary for modified chunks
		# Creates a dictionary of rendered chunks where the key is their relative position (x, y)
		self.renderedchunks = {(x, y): chunk((x, y)) for x in range(-1, 3) for y in range(-1, 3)}
		self.setcolidable()

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
		self.setcolidable()

	def draw(self, screen, mousepos, mousepressed):

		# Draws each chunk based on its key (x, y) and multiplying that by it's size, then adding the window position
		for mapchunk in self.renderedchunks:
			xpos, ypos = cts.add(self.windowpos, cts.muliply(mapchunk, cts.CHUNKSIZE))
			screen.blit(self.renderedchunks[mapchunk], (xpos, ypos))
			if (mousepressed[0]):
				if (mousepressed[0] and pygame.Rect(xpos, ypos, cts.CHUNKSIZE[0], cts.CHUNKSIZE[1]).collidepoint(mousepos)):
					tile = self.renderedchunks[mapchunk].tilepos((mousepos[0] - xpos, mousepos[1] - ypos))
					self.renderedchunks[mapchunk].changetile(tile)
					self.setcolidable()


	def move(self, playervel, playerpos, window):
		self.setcolidable()
		dist = self.check_collision(self.colidable, pygame.Rect(playerpos[0] + playervel[0], playerpos[1] + playervel[1], 80, 80), playervel[0], playervel[1])

		# self.windowpos = cts.add(self.windowpos, (dist[2], dist[3]))
	
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

		return dist

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

	def check_collision(self, walls, player: pygame.Rect, player_vel_x, player_vel_y):
		new_vel_x = player_vel_x
		new_vel_y = player_vel_y
		offset_x = 0
		offset_y = 0

		# Check for collisions with each wall
		for wall in walls:
			if (player.top < wall.bottom and player.bottom > wall.top):
				if (player.right > wall.left and player.left < wall.left):
					print("Colided left of wall")
					if (player_vel_x > 0):
						new_vel_x = 0
						offset_x = player.right - wall.left
				elif (player.right > wall.right and player.left < wall.right):
					print("Colided right of wall")
					if (player_vel_x < 0):
						new_vel_x = 0
						offset_x = player.left - wall.right

			if (player.right > wall.left and player.left < wall.right):
				if (player.top < wall.top and player.bottom > wall.top):
					print("Colided top of wall")
					if (player_vel_y > 0):
						new_vel_y = 0
						offset_y = player.bottom - wall.top
				elif (player.top < wall.bottom and player.bottom > wall.bottom):
					print("Colided bottom of wall")
					if (player_vel_y < 0):
						new_vel_y = 0
						offset_y = player.top - wall.bottom

		if offset_x > offset_y and offset_y != 0:
			offset_x = 0
		if offset_y > offset_x and offset_x != 0:
			offset_y = 0

		return [new_vel_x, new_vel_y, offset_x, offset_y]


