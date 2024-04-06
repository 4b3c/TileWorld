import pygame

class tilemap(pygame.Surface):
    
    def checkerboard(self):
        for i in range(int(self.get_width() / 20) + 1):
            for j in range(int(self.get_height() / 20) + 1):
                if ((i + j) % 2 == 0):
                    pygame.draw.rect(self, (70, 180, 110), (i * 20, j * 20, 20, 20))