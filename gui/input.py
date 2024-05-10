

class Input:

	def __init__(self, buttons: list):
		self.buttons = buttons

	def check_hover(self, mouse_pos: tuple):
		for button in self.buttons:
			if (button.rect.collidepoint(mouse_pos)):
				button.set_hover()
			else:
				button.set_normal()

	def check_click(self, mouse_pos: tuple):
		for button in self.buttons:
			if (button.rect.collidepoint(mouse_pos)):
				return button.clicked()
