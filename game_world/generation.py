import math
import random
import constants as cts

def smooth(x: float) -> float:
	return (6 * (x**5)) - (15 * (x**4)) + (10 * (x**3))

def z_order(x: int, y: int) -> int:
	result = 0
	for i in range(32): # Assuming 32-bit integers
		result |= ((x & (1 << i)) << i) | ((y & (1 << i)) << (i + 1))
	return result

def dot(list1: list, list2: list) -> float:
	total = 0
	for x0, x1 in zip(list1, list2):
		total += (x0 * x1)
	return total

def lerp(t: float, x0: float, x1: float) -> float:
	return x0 + (t * (x1 - x0))

def gradient_vector(x: int, y: int) -> list:
	random.seed(z_order(x, y) + cts.SEED)
	return [random.uniform(-1, 1), random.uniform(-1, 1)]

def perlin2d(x: float, y: float) -> float:
	x0, y0 = math.floor(x), math.floor(y)
	x1, y1 = x0 + 1, y0 + 1
	corners = [[x0, y0], [x1, y0], [x0, y1], [x1, y1]]

	gradients = [gradient_vector(corner[0], corner[1]) for corner in corners]
	distances = [[corner[0] - x, corner[1] - y] for corner in corners]
	dot_products = [dot(g, d) for g, d in zip(gradients, distances)]

	u, v = smooth(x % 1), smooth(y % 1)
	return lerp(u, lerp(v, dot_products[0], dot_products[2]), lerp(v, dot_products[1], dot_products[3]))

def layered_perlin2d(x: float, y: float) -> float:
	layer1 = perlin2d(x * 1, y * 1) * 27
	layer2 = perlin2d(x * 3, y * 3) * 9
	layer3 = perlin2d(x * 9, y * 9) * 3
	layer4 = perlin2d(x * 27, y * 27) * 1

	average = (layer1 + layer2 + layer3 + layer4) / (27 + 9 + 3 + 1)

	return (average + 1) / 2


# x, y = random.random() * 100, random.random() * 100

# print(x, y)
# print(layered_perlin2d(x, y))
# print((perlin2d(x, y) + 1) / 2)


# import pygame

# pygame.init()
# window = pygame.display.set_mode((600, 600))

# for i in range(300):
# 	for j in range(300):
# 		range01 = layered_perlin2d(i / 50, j / 50)
# 		colorval = min(255, max(0, range01 * 255))
# 		window.set_at((i, j), (colorval, colorval, colorval))

# 		pygame.display.flip()

# while True:
# 	for event in pygame.event.get():
# 		if event.type == pygame.QUIT:
# 			pygame.quit()
# 			quit()