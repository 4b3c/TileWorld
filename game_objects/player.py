import pygame
import json
import os
import constants as cts
from game_objects.velocityobject import VelocityObject


class Player(VelocityObject):

	def __init__(self, name: str, savefile: str) -> None:
		super().__init__([0.0, 0.0], cts.PLAYERSIZE, cts.COLORS["player"], [0.0, 0.0])
		self.name = name
		self.savefile = savefile + "/player.json"
		self.load_from_file()
		pygame.draw.rect(self.surface, cts.COLORS["player_side"], (0, 5, 10, self.size[1] - 10))
		pygame.draw.rect(self.surface, cts.COLORS["player_side"], (self.size[0] - 10, 5, 10, self.size[1] - 10))

	def draw_to(self, screen: pygame.Surface, camera_offset: list):
		screen.blit(self.surface, (round(self.pos[0] - camera_offset[0]), round(self.pos[1] - camera_offset[1])))

	def load_from_file(self) -> list:
		with open(cts.SAVEFOLDER + self.savefile, 'r') as f:
			self.pos = json.load(f)["pos"]

	def save_to_file(self):
		with open(cts.SAVEFOLDER + self.savefile, 'w') as f:
			json.dump({"pos": self.pos}, f, indent = 1)