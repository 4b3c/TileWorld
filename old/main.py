import pygame
import constants as cts
from tilemap import tilemap
from player import player

pygame.init()

window = pygame.display.set_mode(cts.WINDOWSIZE)
pygame.display.set_caption("TileWorld")
running = True

gameMap = tilemap((0, 0), "Wowland")
playerMe = player(cts.subtract(cts.CENTER, (40, 40)), 40, (124, 176, 112))

mousePos = pygame.mouse.get_pos()

print("Starting...")
while running:
	lastPos = mousePos
	mousePos = pygame.mouse.get_pos()
	mousePressed = pygame.mouse.get_pressed()
	keypresses = pygame.key.get_pressed()

	if (keypresses[pygame.K_w] or keypresses[pygame.K_UP]):
		gameMap.vel[1] += -0.08;
	if (keypresses[pygame.K_s] or keypresses[pygame.K_DOWN]):
		gameMap.vel[1] += 0.08;
	if (keypresses[pygame.K_a] or keypresses[pygame.K_LEFT]):
		gameMap.vel[0] += -0.08;
	if (keypresses[pygame.K_d] or keypresses[pygame.K_RIGHT]):
		gameMap.vel[0] += 0.08;
		
	window.fill(cts.COLORS["light_blue"])
	gameMap.draw(window, playerMe, mousePos, mousePressed)
	pygame.display.update()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			gameMap.savechunks()
			pygame.quit()
			quit()
