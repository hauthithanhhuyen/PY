from missile import Missile
import pygame
import math

WIDTH, HEIGHT = 800, 600  # dùng để giới hạn trong màn hình

class Ship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load("assets/ship.png").convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(400, 300))
        self.angle = 0
        self.velocity = pygame.Vector2(0, 0)

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.angle += 5
        if keys[pygame.K_RIGHT]:
            self.angle -= 5
        if keys[pygame.K_UP]:
            direction = pygame.Vector2(0, -1).rotate(-self.angle)
            self.velocity += direction * 0.2
        if keys[pygame.K_DOWN]:
            direction = pygame.Vector2(0, 1).rotate(-self.angle)
            self.velocity += direction * 0.1  # đi lùi nhẹ hơn

        self.velocity *= 0.99  # giảm dần

        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.center += self.velocity

        # === Không cho máy bay ra khỏi màn hình ===
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

    def shoot(self, missile_group):
        direction = pygame.Vector2(0, -1).rotate(-self.angle)
        pos = pygame.Vector2(self.rect.center) + direction * (self.rect.height // 2)
        missile = Missile(pos.x, pos.y, self.angle)
        missile_group.add(missile)
