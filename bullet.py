import pygame
import math

class BulletType:
    NORMAL = "normal"
    SHOTGUN = "shotgun"

class Bullet:
    def __init__(self, x, y, dx, dy, speed, color, damage, bullet_type, sprites=None):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.speed = speed
        self.color = color
        self.damage = damage
        self.bullet_type = bullet_type
        self.sprites = sprites or []  # Lista de sprites
        self.current_sprite_index = 0  # Índice del sprite actual
        self.animation_speed = 0.2  # Velocidad de cambio de sprite
        self.animation_counter = 0  # Contador para controlar la animación

        # Configurar la imagen inicial si hay sprites
        self.image = self.sprites[0] if self.sprites else None
        self.rect = self.image.get_rect() if self.image else pygame.Rect(self.x, self.y, 10, 10)

    def update(self):
        # Actualizar posición
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed

        # Actualizar animación
        if self.sprites:
            self.animation_counter += self.animation_speed
            if self.animation_counter >= 1:
                self.animation_counter = 0
                self.current_sprite_index = (self.current_sprite_index + 1) % len(self.sprites)
                self.image = self.sprites[self.current_sprite_index]

        # Actualizar el rectángulo para colisiones
        if self.image:
            self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 5)
