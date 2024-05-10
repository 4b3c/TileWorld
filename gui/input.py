

class Input:

	def __init__(self, buttons: list):
		self.buttons = buttons

	def check_hover(self, mouse_pos: tuple) -> None:
		for button in self.buttons:
			if (button.rect.collidepoint(mouse_pos)):
				button.hovered = True
			else:
				button.hovered = False
			button.regenerate()

	def check_click(self, mouse_pos: tuple) -> str:
		for button in self.buttons:
			if (button.rect.collidepoint(mouse_pos)):
				button.focused = True
				return button.clicked()
			else:
				button.focused = False
