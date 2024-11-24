import pygame
import os
import sys

# Función para gestionar rutas de recursos
def resource_path(relative_path):
    try:
        # Cuando se ejecuta como ejecutable
        base_path = sys._MEIPASS
    except AttributeError:
        # Cuando se ejecuta en el entorno de desarrollo
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Cargar todos los sprites de balas
def load_bullet_sprites():
    return {
        "normal": [
            pygame.image.load(resource_path(f"assets/bullets/normal/normal_bullet_{i}.png"))
            for i in range(1, 5)
        ],
        "shotgun": [
            pygame.image.load(resource_path(f"assets/bullets/shotgun/shotgun_bullet_{i}.png"))
            for i in range(1, 5)
        ],
        "enemy": [pygame.image.load(resource_path("assets/bullets/enemy_bullet.png"))],  # Convertir en lista
        "enemy_shotgun": [pygame.image.load(resource_path("assets/bullets/enemy_shotgun_bullet.png"))],  # Convertir en lista
    }
