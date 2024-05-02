import pygame, time
from random import randint as rint

# Initialize Pygame and set up screen
pygame.init()
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
last_time = time.time()

# Colors
WHITE = (255, 255, 255)
TAN = (230, 200, 200)
BLUE = (60, 100, 205)
GREEN = (40, 225, 0)

# Player properties
player_size = 50
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT // 2 - player_size // 2
player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
player_speed = 3

# Square properties
square_size = 50
squares = []

# World properties
camera_x = 0
camera_y = 0

debugprint = False


# Generate random squares
def generate_squares():
	return [pygame.Rect(rint(0, WIDTH), rint(0, HEIGHT), square_size, square_size) for _ in range(10)]

# Generate non random squares
def generate_cool_squares(pos):
	return [pygame.Rect(10 + i * square_size, pos, square_size, square_size) for i in range(10)]

def move_squares(x_dist, y_dist):
	return [pygame.Rect(sq.x + x_dist, sq.y + y_dist, sq.width, sq.height) for sq in squares]

# Check collision between player and obstacles
def check_collision(squares, camera_x, camera_y):
	for square in squares:
		if player_rect.colliderect(square):
			# Calculate the direction of the collision
			dx = player_rect.centerx - square.centerx
			dy = player_rect.centery - square.centery

			if debugprint:
				print(dx, dy)

			# Adjust camera position based on collision direction
			if abs(dx) > abs(dy):
				if dx > 0: # Player moving left
					camera_x -= square.right - player_rect.left
				else: # Player moving right
					camera_x -= square.left - player_rect.right
			else:
				if dy > 0: # Player moving up
					camera_y -= square.bottom - player_rect.top
				else: # Player moving down
					camera_y -= square.top - player_rect.bottom
	return camera_x, camera_y

# Main game loop
running = True
squares = generate_cool_squares(100) + generate_cool_squares(600)
while running:
	# Event handling
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	debugprint = False
	if pygame.mouse.get_pressed()[0]:
		print(camera_x, camera_y)
		debugprint = True

	# Get key presses
	keys = pygame.key.get_pressed()
	
	# Move the camera
	if keys[pygame.K_w]: camera_y += player_speed
	if keys[pygame.K_a]: camera_x += player_speed
	if keys[pygame.K_s]: camera_y -= player_speed
	if keys[pygame.K_d]: camera_x -= player_speed

	# Create potential object rects, then undo movements if collided
	potential_obstacles = move_squares(camera_x, camera_y)
	camera_x, camera_y = check_collision(potential_obstacles, camera_x, camera_y)
	
	# Draw everything
	screen.fill(WHITE)
	for square in move_squares(camera_x, camera_y):
		pygame.draw.rect(screen, BLUE, square)
	pygame.draw.rect(screen, TAN, player_rect)
	pygame.display.flip()

	pygame.time.Clock().tick(300)

	print(time.time() - last_time)
	last_time = time.time()

# Quit Pygame
pygame.quit()
