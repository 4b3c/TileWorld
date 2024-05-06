from game_world.generation import layered_perlin2d
import constants as cts


class Tile:

	def __init__(self, pos: list):
		self.pos = pos
		self.val = layered_perlin2d(pos[0] / 50, pos[1] / 50)
		lightvdark = (pos[0] + pos[1]) % 2
		if (self.val > 0.7):
			self.color = cts.COLORS["stone_grey"][lightvdark]
		elif (self.val > 0.65):
			self.color = cts.COLORS["forrest_green"][lightvdark]
		elif (self.val > 0.45):
			self.color = cts.COLORS["field_green"][lightvdark]
		elif (self.val > 0.4):
			self.color = cts.COLORS["sand_tan"][lightvdark]
		else:
			self.color = cts.COLORS["water_blue"][lightvdark]

		self.changes = None
	
	# changes is a string containing all the modifications made to the tile in order 
	def modify(self, change: str):
		if (self.changes == None):
			self.changes = change
		else:
			self.changes += change

	def demodify(self):
		self.changes = None
