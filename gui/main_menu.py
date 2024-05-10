import pygame
from gui.button import Button
from gui.scene import Scene




class MainMenu(Scene):

	def __init__(self) -> None:
		super().__init__()

		self.buttons = [
			Button("Play", (280, 50), (700 - 140, 350)),
			Button("Settings", (280, 50), (700 - 140, 420)),
			Button("Quit", (280, 50), (700 - 140, 490))
		]

		self.add_buttons(self.buttons)

	def core(self, window: pygame.Surface):
		for button in self.buttons:
			button.draw_to(window)
		self.add_text("TileWorld", (700, 250), window, 236)

				
