import constants as cts
from game_objects.velocityobject import VelocityObject


class Player(VelocityObject):

	def __init__(self, name: str) -> None:
		super().__init__([0.0, 0.0], cts.PLAYERSIZE, cts.COLORS["player"], [0.0, 0.0])
		self.name = name