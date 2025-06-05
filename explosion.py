# explosion.py
import pygame
import os

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(os.path.join("assets", "explosion.png")).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.timer = 20

    def update(self):
        self.timer -= 1
        if self.timer <= 0:
            self.kill()