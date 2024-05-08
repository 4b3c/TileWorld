import pygame
import constants as cts
from game_objects.gameobject import GameObject

class ToggleButton(GameObject):

	def __init__(self, size: list, pos: list) -> None:
		super().__init__(pos, size, pygame.Color(0, 0, 0))

		# Overwrite the surface variable
		self.surface = pygame.Surface(size, pygame.SRCALPHA)

		pygame.draw.rect(self.surface, cts.COLORS["ui_brown"], (0, 0, size[0], size[1]), border_radius=8)
		pygame.draw.rect(self.surface, cts.COLORS["ui_grey"], (0, 0, size[0], size[1]), 4, 8)

		text_surface = cts.FONT.render("Build", True, (240, 240, 240))
		text_rect = text_surface.get_rect()
		text_rect.center = cts.divide(size, (2, 2))
		self.surface.blit(text_surface, text_rect)