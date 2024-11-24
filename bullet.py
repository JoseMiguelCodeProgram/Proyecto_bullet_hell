import pygame
import math
import os
import sys

def resource_path(relative_path):
    try:
        # Cuando se ejecuta como ejecutable
        base_path = sys._MEIPASS
    except AttributeError:
        # Cuando se ejecuta en el entorno de desarrollo
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class BulletType:
    NORMAL = "normal"
    SHOTGUN = "shotgun"

class Bullet:
    def __init__(self, x, y, dx, dy, speed, color, damage, bullet_type, sprites=None, size=40):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.speed = speed
        self.color = color
        self.damage = damage
        self.bullet_type = bullet_type
        self.size = size

        # Cargar sprites con verificación de tipo
        if sprites:
            self.sprites = []
            for sprite in sprites:
                if isinstance(sprite, str):  # Si es una ruta, cargar el archivo
                    loaded_sprite = pygame.image.load(resource_path(sprite)).convert_alpha()
                    loaded_sprite = pygame.transform.scale(loaded_sprite, (self.size, self.size))
                    self.sprites.append(loaded_sprite)
                elif isinstance(sprite, pygame.Surface):  # Si ya es un Surface, usar directamente
                    self.sprites.append(pygame.transform.scale(sprite, (self.size, self.size)))
                else:
                    raise TypeError(f"Elemento inválido en sprites: {type(sprite)}")
        else:
            self.sprites = []

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

    def is_out_of_bounds(self, screen_width, screen_height):
        buffer = 1300  # Margen extra
        return (
            self.x < -buffer or self.x > screen_width + buffer or
            self.y < -buffer or self.y > screen_height + (buffer - 300)
        )
