import pygame
import random

green0 = (96, 173, 87)
green1 = (57, 139, 70)
green2 = (0, 98, 56)

def draw_circles(surface, size, x, y):
    pygame.draw.circle(surface, (green0), (x, y - 2), size) # Top (bright)
    pygame.draw.circle(surface, (green2), (x, y + 2), size) # Bottom (dark)
    pygame.draw.circle(surface, (green1), (x, y), size - 2) # Center (medium)



def clump() -> pygame.Surface:
    surface = pygame.Surface((80, 80), pygame.SRCALPHA)

    for i in range(random.randint(3, 10), 1, -1):
        draw_circles(surface, random.randint(i * 3, i * 4), random.randint(25 + i, 55 - i), random.randint(25 + i, 55 - i))
    for i in range(random.randint(3, 20), 1, -1):
        x, y = random.randint(25, 55), random.randint(25, 55)
        pygame.draw.line(surface, green2, (x, y), (x, y + random.randint(10, 30)), 4)



    return surface
