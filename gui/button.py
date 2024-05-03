import pygame
import constants as cts


class ToggleButton:

	def __init__(self, size: list) -> None:
		self.surface = pygame.Surface(size, pygame.SRCALPHA)

		pygame.draw.rect(self.surface, cts.COLORS["ui_brown"], (0, 0, size[0], size[1]), border_radius=8)
		pygame.draw.rect(self.surface, cts.COLORS["ui_grey"], (0, 0, size[0], size[1]), 4, 8)

		text_surface = cts.FONT.render("Pause", True, (240, 240, 240))
		text_rect = text_surface.get_rect()
		text_rect.center = cts.divide(size, (2, 2))
		self.surface.blit(text_surface, text_rect)