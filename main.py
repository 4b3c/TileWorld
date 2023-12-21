import constants as cnst
import pygame
from map import mapClass
from population import populationClass
import time

# Define game specific variables
running = True
delta_time = 0.01
game_zoom = 200
map_x = 40
map_y = 50
new_map = mapClass(cnst.map_size)
new_map.gen_image((map_x, map_y), game_zoom)
new_pop = populationClass(1)
new_pop.gen_image(game_zoom)

# Initialize game essentials
pygame.init()
clock = pygame.time.Clock()
prev_time = time.time()
window = pygame.display.set_mode(cnst.window_size)
mouse_pos = pygame.mouse.get_pos()


while running:

	# Calculate the mouse movement and clicking
	last_mouse_pos = mouse_pos
	mouse_pos = pygame.mouse.get_pos()
	mouse_pressed = pygame.mouse.get_pressed()

	# Handle dragging the map around
	if mouse_pressed[0]:
		movement = (last_mouse_pos[0] - mouse_pos[0], last_mouse_pos[1] - mouse_pos[1])
		map_x -= movement[0]
		map_y -= movement[1]
		# uncomment when optimizing 'loading tiles'
		# new_map.gen_image((map_x, map_y), game_zoom)
		# new_pop.gen_image(game_zoom)
		new_pop.move_villager(0, (mouse_pos[0] - map_x, mouse_pos[1] - map_y))


	for event in pygame.event.get():
		# Handle clicking the X button
		if event.type == pygame.QUIT:
			running = False
		# Handle zooming in and out of the map
		elif event.type == pygame.MOUSEWHEEL:
			last_scale = game_zoom
			game_zoom += round(event.y * cnst.zoom_step * game_zoom)
			game_zoom = min(cnst.zoom_max, max(cnst.zoom_min, game_zoom))

			if last_scale != game_zoom:
				map_x = mouse_pos[0] - ((game_zoom * (mouse_pos[0] - map_x)) / last_scale)
				map_y = mouse_pos[1] - ((game_zoom * (mouse_pos[1] - map_y)) / last_scale)
				
				new_map.gen_image((map_x, map_y), game_zoom)
				new_pop.gen_image(game_zoom)

	# Draw everything to the screen
	window.fill((120, 150, 210))
	window.blit(new_map.surface, (map_x, map_y))
	new_pop.draw_to(window, (map_x, map_y), delta_time)

	# Calculate FPS and Delta Time
	clock.tick()
	FPS = int(clock.get_fps())
	current_time = time.time()
	delta_time = (current_time - prev_time) * 1000
	prev_time = current_time
	print("FPS:", FPS, "Delta Time:", delta_time)

	# Update the screen
	pygame.display.update()