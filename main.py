import constants as cnst
import pygame
from map import mapClass
from population import populationClass

pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode(cnst.window_size)


running = True
game_zoom = 200
map_x = 40
map_y = 50
new_map = mapClass(cnst.map_size)
new_map.gen_image((map_x, map_y), game_zoom)
new_pop = populationClass(1)
new_pop.gen_image(game_zoom)


mouse_pos = pygame.mouse.get_pos()


while running:

	last_mouse_pos = mouse_pos
	mouse_pos = pygame.mouse.get_pos()
	mouse_pressed = pygame.mouse.get_pressed()

	if mouse_pressed[0]:
		movement = (last_mouse_pos[0] - mouse_pos[0], last_mouse_pos[1] - mouse_pos[1])
		map_x -= movement[0]
		map_y -= movement[1]
		# uncomment when optimizing 'loading tiles'
		# new_map.gen_image((map_x, map_y), game_zoom)
		# new_pop.gen_image(game_zoom)


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.MOUSEWHEEL:
			last_scale = game_zoom
			game_zoom += round(event.y * cnst.zoom_step * game_zoom)
			game_zoom = min(cnst.zoom_max, max(cnst.zoom_min, game_zoom))

			if last_scale != game_zoom:
				map_x = mouse_pos[0] - ((game_zoom * (mouse_pos[0] - map_x)) / last_scale)
				map_y = mouse_pos[1] - ((game_zoom * (mouse_pos[1] - map_y)) / last_scale)
				
				new_map.gen_image((map_x, map_y), game_zoom)
				new_pop.gen_image(game_zoom)
				
			
	window.fill((120, 150, 210))
	window.blit(new_map.surface, (map_x, map_y))
	new_pop.draw_to(window)

	clock.tick()
	print("FPS:", int(clock.get_fps()))

	pygame.display.update()