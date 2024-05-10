import pygame
from pygame import Surface
from gui.scene import Scene
from gui.button import Button, TextBox
from gui.input import Input

class NewWorld(Scene):

	def __init__(self):
		super().__init__()

		self.buttons = [
			Button("Create World", (280, 50), (700 - 140, 350)),
			Button("Cancel", (280, 50), (700 - 140, 560))
		]

		self.textboxes = [
			TextBox((200, 50), (700 - 60, 420)),
		]

		self.add_buttons(self.buttons)
		self.typing_handler = Input(self.textboxes)

	def core(self, window: Surface):
		for button in self.buttons + self.textboxes:
			button.draw_to(window)
		self.add_text("Create a New World", (700, 250), window, 126)
		self.add_text_top_left("Name:", (700 - 140, 430), window, 36)

	def switching(self): # Clear text every time this scene is loaded
		for textbox in self.textboxes:
			textbox.text = ""
		return super().switching()

	def event_core(self):
		for event in pygame.event.get():
			if (event.type == pygame.MOUSEMOTION):
				self.typing_handler.check_hover(event.dict["pos"])
				self.input_handler.check_hover(event.dict["pos"])

			elif (event.type == pygame.MOUSEBUTTONDOWN):
				self.typing_handler.check_click(event.dict["pos"])
				next_scene = self.input_handler.check_click(event.dict["pos"])
				if (next_scene != None):
					if (next_scene == "Cancel"):
						return "Back"
					elif (self.textboxes[0].text != ""):
						return "Open " + self.textboxes[0].text
				
			elif (event.type == pygame.KEYDOWN):
				for textbox in self.textboxes:
					if (textbox.focused):
						if event.key == pygame.K_BACKSPACE: # Backspace will remove the last character
							textbox.text = textbox.text[:-1]
						elif event.key == pygame.K_ESCAPE: # Escape does the same thing as pressing "Cancel"
							return "Back"
						elif (event.key == pygame.K_RETURN): # Enter/return does the same thing as pressing "Create World"
							return "Open " + self.textboxes[0].text
						else: # Otherwise append the character to the string of text
							textbox.text += event.unicode
				
			elif (event.type == pygame.QUIT):
				return "Quit"
		
		return None