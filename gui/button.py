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
		
		self.hovered = False
		self.focused = False
		self.regenerate()
		

	def set_text(self):
		text_surface = cts.FONT.render(self.text, True, (240, 240, 240))
		text_rect = text_surface.get_rect()
		text_rect.center = self.center
		self.surface.blit(text_surface, text_rect)

	def regenerate(self):
		if (self.hovered):
			pygame.draw.rect(self.surface, cts.COLORS["blue"], (0, 0, self.size[0], self.size[1]), border_radius=8)
		else:
			pygame.draw.rect(self.surface, cts.COLORS["ui_brown"], (0, 0, self.size[0], self.size[1]), border_radius=8)
		pygame.draw.rect(self.surface, cts.COLORS["ui_grey"], (0, 0, self.size[0], self.size[1]), 4, 8)
		self.set_text()

	def draw_to(self, window: pygame.Surface):
		window.blit(self.surface, self.pos)

	def clicked(self) -> str:
		return self.text
	

class TextBox(Button):

	def __init__(self, size: list, pos: list):
		self.cursor_ticks = 0
		super().__init__("", size, pos)
		self.numbers_only = False

	def set_text(self):
		if (self.focused and self.cursor_ticks > 60):
			text_surface = cts.FONT.render(self.text + "|", True, (240, 240, 240))
		else:
			text_surface = cts.FONT.render(self.text, True, (240, 240, 240))
		text_rect = text_surface.get_rect()
		text_rect.midleft = (20, self.center[1])
		self.surface.blit(text_surface, text_rect)
		self.cursor_ticks += 1
		if (self.cursor_ticks > 120): self.cursor_ticks = 0
	
	def draw_to(self, window: pygame.Surface):
		self.regenerate()
		return super().draw_to(window)