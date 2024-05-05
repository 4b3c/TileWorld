from game_world.generation import perlin2d

class Tile:

	def __init__(self, pos: list):
		self.pos = pos
		self.val = (perlin2d(pos[0] / 5, pos[1] / 5) + 1) * 127.5
		self.color = (self.val, 170, 70)

		self.changes = None
	
	# changes is a string containing all the modifications made to the tile in order 
	def modify(self, change: str):
		if (self.changes == None):
			self.changes = change
		else:
			self.changes += change

	def demodify(self):
		self.changes = None
