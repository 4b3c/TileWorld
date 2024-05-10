import pygame
from gui.scene import Scene
from gui.button import Button



class Pause(Scene):
	
	def __init__(self):
		super().__init__()

		self.buttons = [
			Button("Resume", (280, 50), (700 - 140, 350)),
			Button("Settings", (280, 50), (700 - 140, 420)),
			Button("Save", (280, 50), (700 - 140, 490)),
			Button("Main Menu", (280, 50), (700 - 140, 560))
		]

		self.add_buttons(self.buttons)

	def core(self, window: pygame.Surface):
		for button in self.buttons:
			button.draw_to(window)
		self.add_text("Paused", (700, 250), window, 126)