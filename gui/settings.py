import pygame
from gui.scene import Scene
from gui.button import Button

class Settings(Scene):

	def __init__(self):
		super().__init__()

		self.buttons = [
			Button("Back", (280, 50), (700 - 140, 350))
		]

		self.add_buttons(self.buttons)

	def core(self, window: pygame.Surface):
		for button in self.buttons:
			button.draw_to(window)
		self.add_text("Settings", (700, 250), window, 126)