import pygame
import constants as cts
from tilemap import tilemap
from player import player

pygame.init()

window = pygame.display.set_mode(cts.WINDOWSIZE)
pygame.display.set_caption("TileWorld")
running = True

gameMap = tilemap((0, 0))
playerMe = player((100, 100), 40, (153, 126, 234))

mousePos = pygame.mouse.get_pos()

while running:
	lastPos = mousePos
	mousePos = pygame.mouse.get_pos()
	mousePressed = pygame.mouse.get_pressed()

	keypresses = pygame.key.get_pressed()

	if (keypresses[pygame.K_w]):
		playerMe.vel[1] += -1;
	if (keypresses[pygame.K_s]):
		playerMe.vel[1] += 1;
	if (keypresses[pygame.K_a]):
		playerMe.vel[0] += -1;
	if (keypresses[pygame.K_d]):
		playerMe.vel[0] += 1;
		
	window.fill(cts.COLORS["light_blue"])
	playerMe.draw(window, gameMap)
	gameMap.draw(window)
	pygame.display.update()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()