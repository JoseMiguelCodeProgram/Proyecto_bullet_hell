import pygame
import math
import random
from settings import WIDTH, HEIGHT, player_size

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, player_size, player_size)
        self.bullets = []
        self.health = 10
        self.invulnerable = False  # Estado de invulnerabilidad
        self.invulnerability_time = 0  # Tiempo restante de invulnerabilidad
        self.last_hit_time = 0  # Última vez que recibió daño

    def update(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.x > 0:
            self.rect.x -= 5
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.x < WIDTH - player_size:
            self.rect.x += 5
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.rect.y > 0:
            self.rect.y -= 5
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.rect.y < HEIGHT - player_size:
            self.rect.y += 5

        # Actualizar balas
        for bullet in self.bullets[:]:
            bullet[0] += bullet[2] * 10  # Actualizar posición X
            bullet[1] += bullet[3] * 10  # Actualizar posición Y
            if bullet[0] < 0 or bullet[0] > WIDTH or bullet[1] < 0 or bullet[1] > HEIGHT:
                self.bullets.remove(bullet)

        # Reducir el tiempo de invulnerabilidad
        if self.invulnerable:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_hit_time >= self.invulnerability_time:
                self.invulnerable = False

    def draw(self, screen):
        # Cambiar el color si el jugador es invulnerable
        color = (0, 255, 0) if not self.invulnerable else (255, 255, 0)
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (0, 0, 255), (self.rect.x, self.rect.y - 10, player_size * (self.health / 10), 5))
        for bullet in self.bullets:
            pygame.draw.circle(screen, (255, 255, 0), (int(bullet[0]), int(bullet[1])), 5)

    def shoot(self, mouse_x, mouse_y):
        dx = mouse_x - self.rect.centerx
        dy = mouse_y - self.rect.centery
        distance = math.sqrt(dx**2 + dy**2)
        if distance != 0:
            dx /= distance
            dy /= distance
        self.bullets.append([self.rect.centerx, self.rect.centery, dx, dy])

    def take_damage(self):
        """Reduce la vida del jugador si no está invulnerable."""
        if not self.invulnerable:
            self.health -= 1
            self.invulnerable = True
            self.last_hit_time = pygame.time.get_ticks()
            self.invulnerability_time = random.randint(1500, 2000)  # Duración aleatoria entre 1.5 y 2 segundos
        return self.health <= 0

    def check_collision(self, enemies, bullets):
        """Verifica colisiones con enemigos y balas."""
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                if self.take_damage():
                    return True

        for bullet in bullets:
            if self.rect.collidepoint(bullet[0], bullet[1]):
                bullets.remove(bullet)
                if self.take_damage():
                    return True
        return False
