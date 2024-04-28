import pygame
import constants as cts
from game_objects import Player
from game_world import Chunk
from camera import Camera

pygame.init()

window = pygame.display.set_mode(cts.WINDOWSIZE)
pygame.display.set_caption("TileWorld")
running = True

character = Player("Reza")
chunk_id_current = 1215432
world = Chunk([0, 0], chunk_id_current)
main_camera = Camera(character)


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
			
	main_camera.update_pos()
	main_camera.draw_scene(window)
	window.blit(world.surface, (10, 10))
	pygame.display.update()
	pygame.Clock().tick(60)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()
