import pygame

class BulletType:
    NORMAL = "normal"
    SHOTGUN = "shotgun"

class Bullet:
    def __init__(self, x, y, dx, dy, speed, color, damage, bullet_type=BulletType.NORMAL):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.speed = speed
        self.color = color
        self.damage = damage
        self.bullet_type = bullet_type
        self.radius = 5 if bullet_type == BulletType.NORMAL else 7  # Diferentes tamaños

    def update(self):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def is_out_of_bounds(self, width, height):
        return self.x < 0 or self.x > width or self.y < 0 or self.y > height
