import os
import pygame
from gui.button import Button
from gui.scene import Scene


class Selector(Scene):

	def __init__(self):
		super().__init__()

		self.buttons = [
			Button("New World", (280, 50), (700 - 140, 350)),
			Button("Back", (280, 50), (700 - 140, 350 + (70 * 5)))
		]
		self.selection_buttons = [Button("Open " + name, (280, 50), (700 - 140, 420 + 70 * i)) for i, name in zip(range(3), os.listdir("worlds"))]

		self.add_buttons(self.buttons + self.selection_buttons)

	def switching(self): # Everytime this scene loads it should update the selection buttons incase new worlds were created
		self.selection_buttons = [Button("Open " + name, (280, 50), (700 - 140, 420 + 70 * i)) for i, name in zip(range(3), os.listdir("worlds"))]
		self.add_buttons(self.buttons + self.selection_buttons)
		return super().switching()

	def core(self, window: pygame.Surface):
		for button in self.buttons:
			button.draw_to(window)
		for button in self.selection_buttons:
			button.draw_to(window)
		self.add_text("Select a World", (700, 250), window, 126)
