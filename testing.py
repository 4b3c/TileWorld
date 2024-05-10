# from game_world.chunk import Chunk
# import time
# lasttime = time.time()
# for i in range(200):
# 	Chunk((0, i))
# print(time.time() - lasttime)


import pygame
import constants as cts
from gui.main_menu import MainMenu
from gui.settings import Settings

# Initialize pygame and pygame window
pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode(cts.WINDOWSIZE)
pygame.display.set_caption("TileWorld")

scenes = {
	"MainMenu": MainMenu(),
	"Settings": Settings()
}

scene_traverse = [scenes["MainMenu"]]

while True:
	scene_traverse[-1].switching()
	next_scene = scene_traverse[-1].run(clock, window)
	
	if (next_scene in scenes):
		scene_traverse.append(scenes[next_scene])
	elif (next_scene == "Back"):
		scene_traverse.pop(-1)
	elif (next_scene == "Quit"):
		break

