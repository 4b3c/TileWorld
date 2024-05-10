import pygame
from gui.input import Input


class Scene:

	def __init__(self):
		pass

	def add_buttons(self, buttons: list):
		self.input_handler = Input(buttons)

	def add_text(self, text: str, pos: tuple, window: pygame.Surface, text_size: int):
		font = pygame.font.Font(None, text_size)
		text_surface = font.render(text, True, (230, 230, 230))
		text_rect = text_surface.get_rect()
		text_rect.center = pos
		window.blit(text_surface, text_rect)

	def add_text_top_left(self, text: str, pos: tuple, window: pygame.Surface, text_size: int):
		font = pygame.font.Font(None, text_size)
		text_surface = font.render(text, True, (230, 230, 230))
		text_rect = text_surface.get_rect()
		text_rect.topleft = pos
		window.blit(text_surface, text_rect)

	def switching(self):
		self.input_handler.check_hover(pygame.mouse.get_pos())
	
	def core(self, window: pygame.Surface):
		pass

	def event_core(self):
		for event in pygame.event.get():
			if (event.type == pygame.MOUSEMOTION):
				self.input_handler.check_hover(event.dict["pos"])

			elif (event.type == pygame.MOUSEBUTTONDOWN):
				next_scene = self.input_handler.check_click(event.dict["pos"])
				if (next_scene != None):
					return next_scene
				
			elif (event.type == pygame.KEYDOWN):
				if (event.key == pygame.K_ESCAPE):
					return "Back"
				
			elif (event.type == pygame.QUIT):
				return "Quit"
		
		return None

	def run(self, clock: pygame.Clock, window: pygame.Surface):
		while True:
			clock.tick(120) / 1000

			window.fill((61, 101, 93))
			self.core(window)
			pygame.display.flip()

			event = self.event_core()
			if (event != None):
				return event