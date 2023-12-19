import constants as cnst
import pygame
from map import mapClass


pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode(cnst.window_size)


running = True
new_map = mapClass(cnst.map_size, 25)
map_x = 100
map_y = 100
new_map.gen_image((map_x, map_y))
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
		# new_map.gen_image((map_x, map_y))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.MOUSEWHEEL:
			last_scale = new_map.scale
			new_map.scale += round(event.y * cnst.zoom_step * new_map.scale)
			new_map.scale = min(cnst.zoom_max, max(cnst.zoom_min, new_map.scale))

			if last_scale != new_map.scale:
				map_x = mouse_pos[0] - ((new_map.scale * (mouse_pos[0] - map_x)) / last_scale)
				map_y = mouse_pos[1] - ((new_map.scale * (mouse_pos[1] - map_y)) / last_scale)
				
				new_map.gen_image((map_x, map_y))
			
	window.fill((120, 150, 210))
	window.blit(new_map.surface, (map_x, map_y))

	clock.tick()
	print("FPS:", int(clock.get_fps()))

	pygame.display.update()