import pygame
import constants as cts
from game_object import player

pygame.init()

window = pygame.display.set_mode(cts.WINDOWSIZE)
pygame.display.set_caption("TileWorld")
running = True

character = player("Reza")


mousePos = pygame.mouse.get_pos()

print("Starting...")
while running:
	lastPos = mousePos
	mousePos = pygame.mouse.get_pos()
	mousePressed = pygame.mouse.get_pressed()
	keypresses = pygame.key.get_pressed()

	if (keypresses[pygame.K_w] or keypresses[pygame.K_UP]): character.accelerate(0.0, -cts.SPEED);
	if (keypresses[pygame.K_s] or keypresses[pygame.K_DOWN]): character.accelerate(0.0, cts.SPEED)
	if (keypresses[pygame.K_a] or keypresses[pygame.K_LEFT]): character.accelerate(-cts.SPEED, 0.0)
	if (keypresses[pygame.K_d] or keypresses[pygame.K_RIGHT]): character.accelerate(cts.SPEED, 0.0)
			
	window.fill(cts.COLORS["light_blue"])
	character.update(cts.FRICTION, window, cts.CENTER)
	pygame.display.update()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()
