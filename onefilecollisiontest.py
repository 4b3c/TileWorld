import pygame
import sys
from random import randint as ri

# Initialize Pygame and set up display
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Define colors
WHITE = (255, 255, 255)
TAN = (230, 200, 200)
BLUE = (60, 100, 205)
GREEN = (40, 225, 0)

# Define player and world parameters
player_size = 50
max_speed = 1
world_movement = [0, 0]
friction = 0.8

# Create player and world rects
player = pygame.Rect(WIDTH // 2 - player_size // 2, HEIGHT // 2 - player_size // 2, player_size, player_size)
world_objs = [pygame.Rect(ri(0, WIDTH), ri(0, HEIGHT), player_size, player_size) for x in range(10)]

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    world_movement = [0, 0]
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        world_movement[1] = max_speed;
    if keys[pygame.K_s]:
        world_movement[1] = -max_speed;
    if keys[pygame.K_a]:
        world_movement[0] = max_speed;
    if keys[pygame.K_d]:
        world_movement[0] = -max_speed;
    
    # Update visuals:
    screen.fill(WHITE)

    # Draw the world
    for rect in world_objs:
        rect.x += world_movement[0]
        rect.y += world_movement[1]
        pygame.draw.rect(screen, BLUE, rect)
    
    # Draw player
    pygame.draw.rect(screen, TAN, player)
    
    # Update display
    pygame.display.flip()

pygame.quit()
sys.exit()
