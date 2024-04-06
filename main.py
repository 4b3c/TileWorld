import pygame
from tilemap import tilemap

pygame.init()

window = pygame.display.set_mode((1000, 600))
running = True

gameMap = tilemap((100, 100))
gameMap.fill((100, 230, 140))
gameMap.checkerboard()

while running:
    window.fill((100, 170, 230))
    window.blit(gameMap, (10, 10))
    pygame.display.update()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()