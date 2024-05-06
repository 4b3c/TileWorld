import pygame
import constants as cts
from game_objects.velocityobject import VelocityObject


class Player(VelocityObject):

	def __init__(self, name: str) -> None:
		super().__init__([0.0, 0.0], cts.PLAYERSIZE, cts.COLORS["player"], [0.0, 0.0])
		self.name = name
		pygame.draw.rect(self.surface, cts.COLORS["player_side"], (0, 5, 10, self.size[1] - 10))
		pygame.draw.rect(self.surface, cts.COLORS["player_side"], (self.size[0] - 10, 5, 10, self.size[1] - 10))

	def draw_to(self, screen: pygame.Surface, camera_offset: list):
		screen.blit(self.surface, (round(self.pos[0] - camera_offset[0]), round(self.pos[1] - camera_offset[1])))