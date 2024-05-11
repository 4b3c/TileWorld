import pygame
import random
import math
import time


brown0 = (73, 34, 1)
brown1 = (62, 28, 0)

class Node:
    
    def __init__(self, age: int, length: int, angle: int) -> None:
        print(age)
        self.age = age
        self.length = length
        self.angle = angle
        self.left = None
        self.right = None

    def add_left(self, age) -> None:
        self.left = Node(age * 2, max(random.randint(15, 40) - age, 12), random.randint(95, 110))

    def add_right(self, age) -> None:
        self.right = Node(age * 2, max(random.randint(15, 40) - age, 12), random.randint(70, 85))

    def grow(self, age) -> None:
        number = random.randint(1, 3)
        if (number == 1 and self.left == None): self.add_left(age)
        elif (number == 2 and self.right == None): self.add_right(age)
        else:
            self.length += 1
            self.age += 20

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


def draw_parrallel_lines(start, stop, width, window):
    for i in range(round(-width / 2) - 1, round(width / 2) + 1, 1):
        if i < -1:
            brown = brown1
        else:
            brown = brown0
        pygame.draw.line(window, brown, (start[0] + i, start[1]), (stop[0] + i, stop[1]))


def draw(node: Node, start: tuple[float, float], window: pygame.Surface) -> None: # Draws every node in a tree, along with connections
    if (node == None):
        return
    pos = get_position(start, node.length, math.radians(node.angle))
    draw_parrallel_lines(start, pos, math.sqrt(count(node)), window) # Thick line
    # pygame.draw.circle(window, (255, 255, 255), pos, 4)
    # pygame.draw.line(window, (255, 255, 255), start, pos) # Skeleton line
    draw(node.left, pos, window)
    draw(node.right, pos, window)


def random_child(node: Node) -> Node: # Picks a random node from the children of a root
    if (node == None or node.left == None or node.right == None):
        return None
    
    choices = [node, random_child(node.left), random_child(node.left), random_child(node.right), random_child(node.right)]
    return random.choice([valid for valid in choices if valid != None]) # Only returns valid choices (Not None and having 2 children)

    
class Tree:

    def __init__(self) -> None:
        self.age = 0
        self.rect = pygame.Rect(0, 0, 400, 600)
        self.surface = pygame.Surface(self.rect.size)
        self.root = Node(self.age, 30, 90)

    def grow(self):
        if (count(self.root) < 80):
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
        self.surface.fill((61, 101, 93))
        draw(self.root, self.rect.midbottom, self.surface)






pygame.init()

window = pygame.display.set_mode((900, 700))

tree = Tree()



while True:
    tree.grow()
    window.fill((61, 101, 93))
    window.blit(tree.surface, (250, 50))
    tree.draw()
    pygame.display.flip()
    time.sleep(0.01)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        elif (event.type == pygame.MOUSEBUTTONDOWN):
            pygame.image.save(tree.surface, "images/tree.png")
            tree = Tree()



