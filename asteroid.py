# asteroid.py
import pygame
import random
import os

class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join("assets", "asteroid.png")).convert_alpha()
        self.rect = self.image.get_rect(center=(random.randint(0, 800), random.randint(-150, -40)))
        self.speed = random.randint(2, 6)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 600:
            self.reset_position()

    def reset_position(self):
        self.rect.y = random.randint(-150, -40)
        self.rect.x = random.randint(0, 800)
        self.speed = random.randint(2, 6)
