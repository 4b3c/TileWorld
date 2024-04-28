import pygame
import time
import constants as cts
from game_objects import Player
from game_world import Map
from camera import Camera

pygame.init()
last_time = time.time()
game_loops = 0

window = pygame.display.set_mode(cts.WINDOWSIZE)
pygame.display.set_caption("TileWorld")
running = True

character = Player("Reza")
chunk_id_current = 82234
world = Map("Weaven")
main_camera = Camera(character, world)


mousePos = pygame.mouse.get_pos()

print("Starting...")
while running:
	lastPos = mousePos
	mousePos = pygame.mouse.get_pos()
	mousePressed = pygame.mouse.get_pressed()
	keypresses = pygame.key.get_pressed()

	if (keypresses[pygame.K_w] or keypresses[pygame.K_UP]): character.accelerate(0.0, -cts.ACCELERATION);
	if (keypresses[pygame.K_s] or keypresses[pygame.K_DOWN]): character.accelerate(0.0, cts.ACCELERATION)
	if (keypresses[pygame.K_a] or keypresses[pygame.K_LEFT]): character.accelerate(-cts.ACCELERATION, 0.0)
	if (keypresses[pygame.K_d] or keypresses[pygame.K_RIGHT]): character.accelerate(cts.ACCELERATION, 0.0)
		
	main_camera.update_pos()
	main_camera.draw_scene(window)
	pygame.display.update()

	game_loops += 1
	if (time.time() - last_time >= 1):
		print("fps:", game_loops)
		game_loops = 0
		last_time = time.time()

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()
