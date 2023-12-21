from villager import villagerClass

class populationClass:
	def __init__(self, popCount):
		self.villagers = [villagerClass() for _ in range(popCount)]

	def gen_image(self, scale):
		for villager in self.villagers:
			villager.gen_image(scale)

	def draw_to(self, window):
		for villager in self.villagers:
			villager.draw_to(window)