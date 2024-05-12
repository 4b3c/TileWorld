import pygame
import random
import math
import time
from clump_generator import clump


brown0 = (73, 34, 1)
brown1 = (62, 28, 0)



class Node:
	
	def __init__(self, age: int, length: int, angle: int) -> None:
		self.age = age
		self.length = length
		self.angle = angle
		self.left = None
		self.right = None
		self.leaves = clump()

	def add_left(self, age) -> None:
		self.left = Node(age * 2, max(random.randint(15, 40) - age, 12), random.randint(95, 110))

	def add_right(self, age) -> None:
		self.right = Node(age * 2, max(random.randint(15, 40) - age, 12), random.randint(70, 85))

	def grow(self, age) -> None:
		number = random.randint(1, 3)
		if (number == 1 and self.left == None): self.add_left(age)
		elif (number == 2 and self.right == None): self.add_right(age)
		else:
			self.length += 1.2
			self.age += 13

	def bend(self, angle_incremeent: float):
		if self.angle > 140 or self.angle < 40:
			return
		self.angle += angle_incremeent
		self.age -= 3
		if self.left != None: self.left.age -= 3
		if self.right != None: self.right.age -= 3


def copy(node):
	if node is None:
		return None
	new_node = Node(node.age, node.length, node.angle)
	new_node.left = copy(node.left)
	new_node.right = copy(node.right)
	return new_node



def count(node: Node) -> int: # Returns the number of child nodes (incudes itself)
	if (node == None):
		return 0
	
	return 1 + count(node.left) + count(node.right)


def youngest(node: Node) -> tuple[int, Node]: # Returns the age and node
	if (node == None):
		return [10000, None]
		
	left = youngest(node.left)
	right = youngest(node.right)

	if (node.age < left[0] and node.age < right[0]):
		return (node.age, node)
	else:
		return left if left[0] < right[0] else right


def get_position(start: tuple[float ,float], radius: float, angle: float): # Takes rectangular and polar coords and adds them
	return ((start[0] + (radius * math.cos(angle))), (start[1] - (radius * math.sin(angle))))


def draw_parallel_lines(start, stop, perp_angle, width, window): # Perp angle needs to be in radians https://www.desmos.com/calculator/hh236r60m7
	for i in range(round(-width / 2), round(width / 2) + 1, 1):
		new_start = (start[0] + (i * math.cos(perp_angle)), start[1] + (-i * math.sin(perp_angle)))
		new_stop = (stop[0] + (i * math.cos(perp_angle)), stop[1] + (-i * math.sin(perp_angle)))
		
		if i < -1:
			brown = brown1
		else:
			brown = brown0
		pygame.draw.line(window, brown, new_start, new_stop, 2)


def draw(node: Node, start: tuple[float, float], window: pygame.Surface) -> None: # Draws every node in a tree, along with connections
	if (node == None):
		return
	pos = get_position(start, node.length, math.radians(node.angle))
	width = count(node)**(3/4)

	if (count(node) < 12): window.blit(node.leaves, (pos[0] - 40, pos[1] - 40)) # If the node has < 10 children draw leaves
	pygame.draw.circle(window, brown0, pos, width * 0.6) # This brown circle colors in gaps between braches that are very bent
	draw_parallel_lines(start, pos, math.radians(node.angle + 90), width, window) # Draws the branch for each node
	# pygame.draw.line(window, (255, 255, 255), start, pos, 2) # Skeleton of the tree for testing purposes
	draw(node.left, pos, window) # Recursively draws node's left and right children
	draw(node.right, pos, window)
	if (count(node) < 3): window.blit(node.leaves, (pos[0] - 40, pos[1] - 40)) # If the node is extremely close to the edge, it also draws leaves on top


def random_child(node: Node) -> Node: # Picks a random node from the children of a root
	if (node == None or node.left == None or node.right == None):
		return None
	
	choices = [node, random_child(node.left), random_child(node.left), random_child(node.right), random_child(node.right)]
	return random.choice([valid for valid in choices if valid != None]) # Only returns valid choices (Not None and having 2 children)


def pixellate(surface: pygame.Surface):
	width, height = surface.get_size()
	small = pygame.transform.scale(surface, (width // 4, height // 4))
	return pygame.transform.scale(small, (width, height))


	
class Tree:

	def __init__(self) -> None:
		self.age = 0
		self.rect = pygame.Rect(0, 0, 300, 300)
		self.surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
		self.root = Node(self.age, 30, 90)

	def grow(self):
		if (count(self.root) < 50):
			self.age += 1
			grow_node = youngest(self.root)[1]
			grow_node.grow(self.age)
			bend_node = random_child(self.root)
			if (bend_node != None):
				if count(bend_node.left) < count(bend_node.right):
					bend_node.left.bend(1)
				else:
					bend_node.right.bend(-1)


	def draw(self):
		self.surface.fill((0, 0, 0, 0))
		draw(self.root, self.rect.midbottom, self.surface)






pygame.init()

window = pygame.display.set_mode((900, 700))

tree = Tree()



while True:
	tree.grow()
	window.fill((61, 101, 93))
	window.blit(pixellate(tree.surface), (300, 200))
	# window.blit(tree.surface, (300, 200))
	tree.draw()
	pygame.display.flip()
	time.sleep(0.01)


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit()
		elif (event.type == pygame.MOUSEBUTTONDOWN):
			pygame.image.save(pixellate(tree.surface), "images/tree.png")
			tree = Tree()



