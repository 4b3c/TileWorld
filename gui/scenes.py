import pygame
from gui.button import ToggleButton
from gui.input import Input

play = ToggleButton("Play", (280, 50), (700 - 140, 350))
settings = ToggleButton("Settings", (280, 50), (700 - 140, 420))
escape = ToggleButton("Quit", (280, 50), (700 - 140, 490))


input_handler = Input([play, settings, escape])

def add_text(text: str, pos: tuple, screen: pygame.Surface):
	font = pygame.font.Font(None, 236)
	text_surface = font.render(text, True, (230, 230, 230))
	text_rect = text_surface.get_rect()
	text_rect.center = pos
	screen.blit(text_surface, text_rect)

def main_menu(window: pygame.Surface, clock: pygame.Clock):
	while True:
		clock.tick(120) / 1000

		window.fill((61, 101, 93))
		play.draw_to(window)
		settings.draw_to(window)
		escape.draw_to(window)
		add_text("TileWorld", (700, 250), window)

		pygame.display.flip()

		for event in pygame.event.get():
			if (event.type == pygame.QUIT):
				return
			elif (event.type == pygame.MOUSEMOTION):
				input_handler.check_hover(event.dict["pos"])
			elif (event.type == pygame.MOUSEBUTTONDOWN):
				input_handler.check_click(event.dict["pos"])

				
