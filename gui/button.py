import pygame
import constants as cts
from gui.scene import Scene



class Button:

	def __init__(self, text: str, size: list, pos: list):
		self.text = text
		self.size = size
		self.pos = pos
		self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
		self.center = cts.divide(self.size, (2, 2))
		self.surface = pygame.Surface(size, pygame.SRCALPHA)
		self.set_normal()

	def set_text(self):
		text_surface = cts.FONT.render(self.text, True, (240, 240, 240))
		text_rect = text_surface.get_rect()
		text_rect.center = self.center
		self.surface.blit(text_surface, text_rect)

	def set_normal(self):
		# Decorate buttons with ui style adn add text
		pygame.draw.rect(self.surface, cts.COLORS["ui_brown"], (0, 0, self.size[0], self.size[1]), border_radius=8)
		pygame.draw.rect(self.surface, cts.COLORS["ui_grey"], (0, 0, self.size[0], self.size[1]), 4, 8)
		self.set_text()

	def set_hover(self):
		# Decorate buttons with hovered ui style and text
		pygame.draw.rect(self.surface, cts.COLORS["blue"], (0, 0, self.size[0], self.size[1]), border_radius=8)
		pygame.draw.rect(self.surface, cts.COLORS["ui_grey"], (0, 0, self.size[0], self.size[1]), 4, 8)
		self.set_text()

	def draw_to(self, window: pygame.Surface):
		window.blit(self.surface, self.pos)

	def clicked(self) -> str:
		return self.text