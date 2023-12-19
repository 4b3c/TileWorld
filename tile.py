import constants


class tileClass:
	def __init__(self, terrain):
		self.terrain = terrain
		self.color = constants.terrain_color[terrain]


