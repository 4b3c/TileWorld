import pygame
from game_objects import GameObject
import constants as cts



class Camera:
    def __init__(self, follow: GameObject) -> None:
        self.follow = follow
        self.size = list(cts.WINDOWSIZE)
        self.update()
        
    def update(self):
        self.follow.update(cts.FRICTION)
        self.centerpos = [self.follow.pos[0] + self.follow.size[0], self.follow.pos[1] + self.follow.size[1]]
        self.pos = [self.centerpos[0] - cts.CENTER[0], self.centerpos[1] - cts.CENTER[1]]

    def draw_scene(self, screen: pygame.Surface):
        screen.fill(cts.COLORS["light_blue"])
        self.follow.draw(screen, self.pos)