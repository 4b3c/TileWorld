import pygame
pygame.init()

# Window
WINDOWSIZE = (1600, 900)
CENTER = (WINDOWSIZE[0] / 2, WINDOWSIZE[1] / 2)

# World
CHUNKSIZE = (8, 8)
TILESIZE = 50
CHUNKPIXELSIZE = (CHUNKSIZE[0] * TILESIZE, CHUNKSIZE[1] * TILESIZE)
SEED = 2763492
SAVEFOLDER = "worlds/"

# Player
PLAYERSIZE = (60, 60)
ACCELERATION = 0.08
FRICTION = 0.02
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
    "w": pygame.Color(70, 70, 80),
    "t": pygame.Color(50, 190, 90)
}
FONT = pygame.font.Font(None, 36)
