import pygame

# Window
WINDOWSIZE = (1600, 900)
CENTER = (WINDOWSIZE[0] / 2, WINDOWSIZE[1] / 2)

# World
CHUNKSIZE = (8, 8)
TILESIZE = 50
SEED = 2763492
SAVEFOLDER = "worlds/"

# Player
PLAYERSIZE = (60, 60)
ACCELERATION = 0.08
FRICTION = 0.02
MAXSPEED = ACCELERATION / FRICTION

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