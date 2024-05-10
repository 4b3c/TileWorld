import pygame
import constants as cts
from gui.scene import Scene
from gui.button import Button
from game_objects.player import Player
from game_world.map import Map
from camera import Camera


class Game(Scene):

	def __init__(self, filename: str):
		super().__init__()

		self.filename = filename
		self.buttons = [
			Button("Pause", (160, 50), (1400 - 190, 30))
		]
		self.add_buttons(self.buttons)		

		# Initialize player and world
		self.world = Map(self.filename) # Creating the world before the player is important incase it doesn't have a save folder
		self.character = Player("Reza", self.filename)
		self.main_camera = Camera(self.character, self.world)

	def run(self, clock: pygame.Clock, window: pygame.Surface):
		while True:
			dt = clock.tick(120) / 1000
			keypresses = pygame.key.get_pressed()

			if (keypresses[pygame.K_w] or keypresses[pygame.K_UP]): self.character.accelerate((0.0, -cts.ACCELERATION))
			if (keypresses[pygame.K_s] or keypresses[pygame.K_DOWN]): self.character.accelerate((0.0, cts.ACCELERATION))
			if (keypresses[pygame.K_a] or keypresses[pygame.K_LEFT]): self.character.accelerate((-cts.ACCELERATION, 0.0))
			if (keypresses[pygame.K_d] or keypresses[pygame.K_RIGHT]): self.character.accelerate((cts.ACCELERATION, 0.0))
			if (keypresses[pygame.K_ESCAPE]): return "Pause"

			self.main_camera.update_scene(dt)
			self.main_camera.draw_scene(window)
			for button in self.buttons:
				button.draw_to(window)
			self.add_text_top_left("fps: " + str(round(clock.get_fps())), (30, 30), window, 36)
			self.add_text_top_left("pos: " + str(round(self.character.pos[0])) + ", " + str(round(self.character.pos[1])), (30, 60), window, 36)
			pygame.display.flip()

			for event in pygame.event.get():
				if (event.type == pygame.MOUSEMOTION):
					self.input_handler.check_hover(event.dict["pos"])

				elif (event.type == pygame.MOUSEBUTTONDOWN):
					next_scene = self.input_handler.check_click(event.dict["pos"])
					if (next_scene != None):
						self.world.save_to_file()
						self.character.save_to_file()
						return next_scene
					
				elif (event.type == pygame.QUIT):
					self.world.save_to_file()
					self.character.save_to_file()
					return "Quit"