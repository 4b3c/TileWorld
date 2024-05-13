import pygame
import random
import constants as cts
from game_objects.velocityobject import VelocityObject
from game_world.map import Map
from mytests.tree_generator import Tree
from mytests.tree_generator import pixellate


class Camera:

	def __init__(self, follow: VelocityObject, world: Map):
		self.follow = follow
		self.world = world
		self.size = cts.WINDOWSIZE

		self.update_pos()
		self.world.initialize_scene(self.pos)


		self.random_trees = [Tree() for _ in range(20)]
		for _ in range(200):
			for tree in self.random_trees:
				tree.grow()
				tree.draw()
		self.random_pos = [(random.randint(0, 1000), random.randint(-1600, -600)) for _ in range(20)]

	def update_pos(self):
		self.centerpos = cts.add((round(self.follow.pos[0]), round(self.follow.pos[1])), cts.divide(self.follow.size, (2, 2)))
		self.pos = cts.subtract(self.centerpos, cts.CENTER)

	def update_scene(self, deltatime: float):
		# update the player's position and then check for collisions
		self.follow.update_xpos(cts.FRICTION, deltatime)
		self.follow.check_collisionx(self.world.obstacles)
		self.follow.update_ypos(cts.FRICTION, deltatime)
		self.follow.check_collisiony(self.world.obstacles)

		self.update_pos()
		self.world.update_pos(self.pos)

	def draw_scene(self, screen: pygame.Surface):
		screen.fill(cts.COLORS["water_blue"][0])
		self.world.draw_to(screen, self.pos)
		self.follow.draw_to(screen, self.pos)

		for tree, pos in zip(self.random_trees, self.random_pos):
			screen.blit(pixellate(tree.surface), cts.subtract(pos, self.pos))