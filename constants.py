import random
import pygame

WINDOWSIZE = (1600, 900)
CENTER = (WINDOWSIZE[0] / 2, WINDOWSIZE[1] / 2)
CHUNKSIZE = (WINDOWSIZE[0] / 2, WINDOWSIZE[1] / 2)
TILESIZE = 50
PLAYERSIZE = (40, 40)
SPEED = 0.03
FRICTION = 0.02

SEED = 2763492
SAVEFOLDER = "worlds/"

COLORS = {
    "light_green": pygame.Color(100, 230, 140),
    "dark_green": pygame.Color(70, 180, 110),
    "light_blue": pygame.Color(100, 170, 230),
    "light_grey": pygame.Color(40, 40, 40),
    "player": pygame.Color(123, 13, 12)
}

CHUNKSHIFT = {
	-1: range(2, -2, -1),
    0: range(-1, 3, 1),
	1: range(-1, 3, 1)
}