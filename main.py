import pygame
import constants as cts
from game_objects.player import Player
from game_world.map import Map
from camera import Camera
from gui.button import ToggleButton


# Initialize pygame and pygame window
pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode(cts.WINDOWSIZE)
pygame.display.set_caption("TileWorld")


# Initialize main game variables
running = True
mouseDown = False
mousePos = pygame.mouse.get_pos()


# Initialize player and world
print("Starting...")
character = Player("Reza", "Weaven")
print("Player created")
world = Map("Weaven")
print("World created")
main_camera = Camera(character, world)
print("Camera created")


# Testing
button = ToggleButton((140, 60), (cts.WINDOWSIZE[0] - 30 - 140, 30))

def add_text(text: str, pos: tuple, screen: pygame.Surface):
	text_surface = cts.FONT.render(text, True, (230, 230, 230))
	text_rect = text_surface.get_rect()
	text_rect.topleft = pos
	screen.blit(text_surface, text_rect)

# Main game loop
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
	button.draw_to(window)
	add_text("fps: " + str(round(clock.get_fps())), (30, 30), window)
	add_text("pos: " + str(round(character.pos[0])) + ", " + str(round(character.pos[1])), (30, 60), window)
	pygame.display.flip()

	for event in pygame.event.get():
		if (event.type == pygame.QUIT):
			world.save_to_file()
			character.save_to_file()
			running = False

pygame.quit()
quit()