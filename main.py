import pygame
import time
import constants as cts
from game_objects.player import Player
from game_world.map import Map
from camera import Camera


pygame.init()
clock = pygame.time.Clock()
last_time = time.time()

window = pygame.display.set_mode(cts.WINDOWSIZE)
pygame.display.set_caption("TileWorld")
running = True

character = Player("Reza", "Weaven")
world = Map("Weaven")
main_camera = Camera(character, world)

mousePos = pygame.mouse.get_pos()
mouseDown = False

print("Starting...")
print("Rendered chunks:", world.rendered_chunks.keys())
game_loops = 0

while (running):
	dt = clock.tick(120) / 1000

	lastPos = mousePos
	mousePos = pygame.mouse.get_pos()
	mousePressed = pygame.mouse.get_pressed()
	keypresses = pygame.key.get_pressed()

	if (mousePressed[0] and not mouseDown):
		world.modify(cts.add(mousePos, main_camera.pos), "w")
		mouseDown = True
	elif (mousePressed[2] and not mouseDown):
		world.demodify(cts.add(mousePos, main_camera.pos))
		mouseDown = True
	elif (mouseDown and not mousePressed[0] and not mousePressed[2]):
		mouseDown = False

	if (keypresses[pygame.K_w] or keypresses[pygame.K_UP]): character.accelerate(0.0, -cts.ACCELERATION)
	if (keypresses[pygame.K_s] or keypresses[pygame.K_DOWN]): character.accelerate(0.0, cts.ACCELERATION)
	if (keypresses[pygame.K_a] or keypresses[pygame.K_LEFT]): character.accelerate(-cts.ACCELERATION, 0.0)
	if (keypresses[pygame.K_d] or keypresses[pygame.K_RIGHT]): character.accelerate(cts.ACCELERATION, 0.0)
		
	main_camera.update_scene(dt)
	main_camera.draw_scene(window)
	pygame.display.flip()

	game_loops += 1
	if (time.time() - last_time >= 1):
		print("fps:", game_loops)
		game_loops = 0
		last_time = time.time()

	for event in pygame.event.get():
		if (event.type == pygame.QUIT):
			world.save_to_file()
			character.save_to_file()
			running = False

pygame.quit()
quit()