import pygame
from random import randint as rint

# Initialize Pygame and set up screen
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Colors
WHITE = (255, 255, 255)
TAN = (230, 200, 200)
BLUE = (60, 100, 205)
GREEN = (40, 225, 0)

# Player properties
player_size = 50
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT // 2 - player_size // 2
player_speed = 1

# Square properties
square_size = 50
squares = []


debugprint = False


# Generate random squares
def generate_squares():
	for _ in range(10):
		square = pygame.Rect(rint(0, WIDTH - square_size), rint(0, HEIGHT - square_size), square_size, square_size)
		squares.append(square)

# Check collision between player and squares
def check_collision(player_rect):
	player_x = player_rect.x
	player_y = player_rect.y
	
	for square in squares:
		if player_rect.colliderect(square):
			# Calculate the direction of the collision
			dx = player_rect.centerx - square.centerx
			dy = player_rect.centery - square.centery

			if debugprint:
				print(dx, dy)

			# Adjust player position based on collision direction
			if abs(dx) > abs(dy):
				if dx > 0:
					player_x = square.right
				else:
					player_x = square.left - player_size
			else:
				if dy > 0:
					player_y = square.bottom
				else:
					player_y = square.top - player_size
	return player_x, player_y

# Main game loop
running = True
generate_squares()
while running:
	# Event handling
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	debugprint = False
	if pygame.mouse.get_pressed()[0]:
		debugprint = True

	# Get key presses
	keys = pygame.key.get_pressed()
	
	# Move the player
	if keys[pygame.K_w]: player_y -= player_speed
	if keys[pygame.K_a]: player_x -= player_speed
	if keys[pygame.K_s]: player_y += player_speed
	if keys[pygame.K_d]: player_x += player_speed

	# Create potential player rectangle, then undo movements if collided
	player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
	player_x, player_y = check_collision(player_rect)
	player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
	
	# Draw everything
	screen.fill(WHITE)
	pygame.draw.rect(screen, TAN, player_rect)
	for square in squares:
		pygame.draw.rect(screen, BLUE, square)
	pygame.display.flip()

	pygame.time.Clock().tick(300)

# Quit Pygame
pygame.quit()
