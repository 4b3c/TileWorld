import pygame
import random
import math

# Initialize pygame and pygame window
pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((1400, 800))
pygame.display.set_caption("TileWorld")

tileset = pygame.image.load("tests/tiles.png")


grasses = [tileset.subsurface(i * 64, 0, 64, 64) for i in range(7) for _ in range(int(i // 2) + 1)]
forrests = [tileset.subsurface(i * 64, 64, 64, 64) for i in range(7) for _ in range(int(i // 2) + 1)]
seed = random.randint(0, 10000)

def distance(x: int, y: int) -> int:
	return int(math.sqrt(x**2 + y**2))

def z_order(x: int, y: int) -> int:
	result = 0
	for i in range(32): # Assuming 32-bit integers
		result |= ((x & (1 << i)) << i) | ((y & (1 << i)) << (i + 1))
	return result

def random_tile(x: int, y: int):
	random.seed(z_order(x, y) + seed)

	if (distance(x, 0) > 10 + random.randint(0, 3)):
		return forrests[random.randint(0, (len(forrests) - 1))]
	else:
		return grasses[random.randint(0, (len(grasses) - 1))]

for col in range(int(1400 // 64) + 1):
	for row in range(int(800 // 64) + 1):
		window.blit(random_tile(col, row), (col * 64, row * 64))
		
		pygame.display.flip()


while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit()