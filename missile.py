import pygame
import math

class Missile(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.image = pygame.Surface((4, 10))
        self.image.fill((255, 255, 0))
        self.original_image = self.image
        self.angle = angle
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=(x, y))

        # Di chuyển theo góc
        speed = 10
        self.velocity = pygame.Vector2(0, -speed).rotate(-self.angle)

    def update(self):
        self.rect.center += self.velocity
        if (self.rect.bottom < 0 or self.rect.top > 600 or
            self.rect.right < 0 or self.rect.left > 800):
            self.kill()
