import pygame

class tilemap(pygame.Surface):
      
	def checkerboard(self, color):
		for i in range(int(self.get_width() / 50) + 1):
			for j in range(int(self.get_height() / 50) + 1):
				if ((i + j) % 2 == 0):
					pygame.draw.rect(self, color, (i * 50, j * 50, 50, 50))
