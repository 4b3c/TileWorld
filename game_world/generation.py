import math
import random


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
	random.seed(z_order(x, y))
	return [random.uniform(-1, 1), random.uniform(-1, 1)]

def perlin2d(x: float, y: float):
	x0, y0 = math.floor(x), math.floor(y)
	x1, y1 = x0 + 1, y0 + 1
	corners = [[x0, y0], [x1, y0], [x0, y1], [x1, y1]]

	gradients = [gradient_vector(corner[0], corner[1]) for corner in corners]
	distances = [[corner[0] - x, corner[1] - y] for corner in corners]
	dot_products = [dot(g, d) for g, d in zip(gradients, distances)]

	u, v = smooth(x % 1), smooth(y % 1)
	return lerp(u, lerp(v, dot_products[0], dot_products[2]), lerp(v, dot_products[1], dot_products[3]))
