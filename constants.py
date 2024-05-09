import pygame
pygame.init()


def add(list1, list2):
	return [x + y for x, y in zip(list1, list2)]

def subtract(list1, list2):
	return [x - y for x, y in zip(list1, list2)]

def multiply(list1, list2):
	return [x * y for x, y in zip(list1, list2)]

def divide(list1, list2):
	return [x / y for x, y in zip(list1, list2)]

# Window
WINDOWSIZE = (1400, 800)
CENTER = (WINDOWSIZE[0] / 2, WINDOWSIZE[1] / 2)

# World
CHUNKSIZE = (8, 8)
TILESIZE = (64, 64)
CHUNKPIXELSIZE = multiply(CHUNKSIZE, TILESIZE)
SEED = 2763492
SAVEFOLDER = "worlds/"

# Player
PLAYERSIZE = (50, 50)
ACCELERATION = 60
FRICTION = 0.08
MAXSPEED = ACCELERATION / FRICTION

# General
COLORS = {
	# General colors
	"field_green": (pygame.Color(130, 170, 70), pygame.Color(110, 150, 50)),
	"forrest_green": (pygame.Color(70, 120, 60), pygame.Color(50, 100, 40)),
	"water_blue": (pygame.Color(100, 170, 230), pygame.Color(80, 150, 210)),
	"stone_grey": (pygame.Color(120, 120, 120), pygame.Color(100, 100, 100)),
	"sand_tan": (pygame.Color(240, 210, 130), pygame.Color(220, 190, 110)),
	# User interface
	"ui_brown": pygame.Color(170, 110, 50),
	"ui_grey": pygame.Color(50, 50, 50),
	# Player
	"player": pygame.Color(120, 30, 10),
	"player_side": pygame.Color(80, 50, 50),
	# Tile modificiations
	"w": pygame.Color(80, 80, 80),
	"t": pygame.Color(50, 190, 90),
	# Random Palette
	"blue": pygame.Color(51, 72, 77),
	"teal": pygame.Color(61, 101, 93),
	"green": pygame.Color(118, 147, 83),
	"yelllow": pygame.Color(235, 191, 88)
}

FONT = pygame.font.Font(None, 36)
FONTLARGE = pygame.font.Font(None, 52)


def str_to_tuple(string: str):
    try:
        return int(string[1:string.index(",")]), int(string[string.index(" "):-1])
    except:
        print(string)
        quit()


def pxl_to_chunk(coordinates: list) -> tuple:
	return multiply(CHUNKPIXELSIZE, (int((coordinates[0] // CHUNKPIXELSIZE[0])), int((coordinates[1] // CHUNKPIXELSIZE[1]))))

def chunk_to_pxl(coordinates: list) -> tuple:
	return (int(coordinates[0] * CHUNKSIZE[0]), int(coordinates[1] * CHUNKSIZE[1]))

def pxl_to_tile(coordinates: list) -> tuple:
	return multiply(TILESIZE, (int(coordinates[0] // TILESIZE[0]), int(coordinates[1] // TILESIZE[1])))

def tile_to_pxl(coordinates: list) -> tuple:
	return (int(coordinates[0] * TILESIZE[0]), int(coordinates[1] * TILESIZE[1]))
