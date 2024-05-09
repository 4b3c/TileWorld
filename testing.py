# from game_world.chunk import Chunk
# import time
# lasttime = time.time()
# for i in range(200):
# 	Chunk((0, i))
# print(time.time() - lasttime)


import pygame
import constants as cts
from gui import scenes

# Initialize pygame and pygame window
pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode(cts.WINDOWSIZE)
pygame.display.set_caption("TileWorld")

scenes.main_menu(window, clock)