import pygame
import constants as cts


class game_object:

    def __init__(self, pos: list, size: list, color: pygame.Color) -> None:
        self.pos = pos
        self.size = size
        self.color = color
        self.surface = pygame.Surface(size)
        self.surface.fill(color)

    def move(self, x: float, y: float):
        self.pos[0] += x
        self.pos[1] += y

    def draw(self, screen: pygame.Surface, camera_offset: list):
        screen.blit(self.surface, (self.pos[0] + camera_offset[0], self.pos[1] + camera_offset[1]))


class velocity_object(game_object):

    def __init__(self, pos: list, size: list, color: pygame.Color, vel: list) -> None:
        super().__init__(pos, size, color)
        self.vel = vel

    def accelerate(self, x: float, y: float):
        self.vel[0] = self.vel[0] + x
        self.vel[1] = self.vel[1] + y

    def update(self, friction: float, screen: pygame.Surface, camera_offset: list):
        self.move(self.vel[0], self.vel[1])
        self.draw(screen, camera_offset)

        self.vel[0] *= (1 - friction)
        self.vel[1] *= (1 - friction)


class player(velocity_object):

    def __init__(self, name: str) -> None:
        super().__init__([0, 0], cts.PLAYERSIZE, cts.COLORS["player"], [0, 0])
        self.name = name