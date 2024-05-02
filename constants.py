import pygame
pygame.init()

# Window
WINDOWSIZE = (1400, 800)
CENTER = (WINDOWSIZE[0] / 2, WINDOWSIZE[1] / 2)

# World
CHUNKSIZE = (8, 8)
TILESIZE = 80
CHUNKPIXELSIZE = (CHUNKSIZE[0] * TILESIZE, CHUNKSIZE[1] * TILESIZE)
SEED = 2763492
SAVEFOLDER = "worlds/"

# Player
PLAYERSIZE = (60, 60)
ACCELERATION = 1.8
FRICTION = 0.2
MAXSPEED = ACCELERATION / FRICTION

# General
COLORS = {
	# General colors
	"light_green": pygame.Color(100, 230, 140),
	"dark_green": pygame.Color(70, 180, 110),
	"light_blue": pygame.Color(100, 170, 230),
	"light_grey": pygame.Color(40, 40, 40),
	# Player
	"player": pygame.Color(120, 30, 10),
	# Tile modificiations
	"w": pygame.Color(40, 40, 40),
	"t": pygame.Color(50, 190, 90)
}

FONT = pygame.font.Font(None, 36)

def add(list1, list2):
	return [x + y for x, y in zip(list1, list2)]

def subtract(list1, list2):
	return [x - y for x, y in zip(list1, list2)]

def multiply(list1, list2):
	return [x * y for x, y in zip(list1, list2)]

def divide(list1, list2):
	return [x / y for x, y in zip(list1, list2)]

def str_to_tuple(string: str):
    try:
        return int(string[1:string.index(",")]), int(string[string.index(" "):-1])
    except:
        print(string)
        quit()
