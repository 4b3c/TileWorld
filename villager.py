import name


class villagerClass:
	def __init__(self):
		self.firstname = name.random_name()
		self.lastname = name.random_name()
		self.name = self.firstname + " " + self.lastname

		self.health = 100
		self.happiness = 100
		self.hunger = 0
		self.education = 0
		self.traits = []
		self.inventory = []

		self.job = None
		self.home = None
