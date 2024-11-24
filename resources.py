import pygame

# Cargar todos los sprites de balas
def load_bullet_sprites():
    return {
        "normal": [pygame.image.load(f"./assets/bullets/normal/normal_bullet_{i}.png") for i in range(1, 5)],
        "shotgun": [pygame.image.load(f"./assets/bullets/shotgun/shotgun_bullet_{i}.png") for i in range(1, 5)],
        "enemy": pygame.image.load("./assets/bullets/enemy_bullet.png"),
        "enemy_shotgun": pygame.image.load("./assets/bullets/enemy_shotgun_bullet.png"),
    }
