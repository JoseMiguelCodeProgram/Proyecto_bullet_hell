import pygame
import math
import random
from settings import WIDTH, HEIGHT

class Enemy:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.speed = random.uniform(2.0, 6.0)  # Velocidad aleatoria entre 2.0 y 6.0
        self.health = random.randint(3, 6)  # Vidas aleatorias

    def update(self, player_pos):
        dx = player_pos[0] - self.rect.centerx
        dy = player_pos[1] - self.rect.centery

        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance != 0:
            dx /= distance
            dy /= distance

        # Movimiento proporcional a la velocidad aleatoria
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

    def take_damage(self):
        """Reduce la vida del enemigo y devuelve True si muere."""
        self.health -= 1
        return self.health <= 0
    
    def check_collision_with_bullets(self, bullets):
        """
        Verifica si el enemigo colisiona con alguna bala y reduce su salud.
        Retorna True si el enemigo muere.
        """
        for bullet in bullets[:]:  # Iterar sobre las balas
            if self.rect.collidepoint(bullet[0], bullet[1]):  # Verificar colisión
                bullets.remove(bullet)  # Eliminar la bala
                if self.take_damage():  # Reducir salud y verificar si muere
                    return True
        return False


    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)
        # Dibujar barra de vida
        pygame.draw.rect(screen, (0, 255, 100), (self.rect.x, self.rect.y - 10, 50 * (self.health / 6), 5))

class EnemyDistance(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.reload_time = random.randint(500, 1000)  # Tiempo de recarga aleatorio
        self.bullets = []
        self.last_shot_time = 0

    def shoot(self, player_pos):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.reload_time:
            dx = player_pos[0] - self.rect.centerx
            dy = player_pos[1] - self.rect.centery
            distance = math.sqrt(dx ** 2 + dy ** 2)
            if distance != 0:
                dx /= distance
                dy /= distance
            self.bullets.append([self.rect.centerx, self.rect.centery, dx, dy])
            self.last_shot_time = current_time

    def update_bullets(self):
        for bullet in self.bullets[:]:
            bullet[0] += bullet[2] * 8  # Incrementar la velocidad
            bullet[1] += bullet[3] * 8
            if bullet[0] < 0 or bullet[0] > WIDTH or bullet[1] < 0 or bullet[1] > HEIGHT:
                self.bullets.remove(bullet)


    def draw(self, screen):
        
        pygame.draw.rect(screen, (255, 10, 50), self.rect)
        for bullet in self.bullets:
            pygame.draw.circle(screen, (255, 255, 0), (int(bullet[0]), int(bullet[1])), 5)

class EnemyShotgun(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.reload_time = random.randint(1000, 1500)  # Tiempo de recarga más largo
        self.bullets = []
        self.last_shot_time = 0
        self.bullet_speed = 7  # Velocidad de las balas
        self.bullet_count = 5  # Número de balas disparadas
        self.spread_angle = 45  # Ángulo total del abanico en grados

    def shoot(self, player_pos):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.reload_time:
            # Calcular el ángulo hacia el jugador
            dx = player_pos[0] - self.rect.centerx
            dy = player_pos[1] - self.rect.centery
            angle_to_player = math.atan2(dy, dx)
            
            # Generar balas en un abanico
            for i in range(self.bullet_count):
                spread = (i - self.bullet_count // 2) * (self.spread_angle / self.bullet_count)
                angle = angle_to_player + math.radians(spread)
                bullet_dx = math.cos(angle)
                bullet_dy = math.sin(angle)
                self.bullets.append([self.rect.centerx, self.rect.centery, bullet_dx, bullet_dy])
            
            self.last_shot_time = current_time

    def update_bullets(self):
        for bullet in self.bullets[:]:
            bullet[0] += bullet[2] * self.bullet_speed
            bullet[1] += bullet[3] * self.bullet_speed
            if bullet[0] < 0 or bullet[0] > WIDTH or bullet[1] < 0 or bullet[1] > HEIGHT:
                self.bullets.remove(bullet)

    def draw(self, screen):
        
        pygame.draw.rect(screen, (255, 50, 10), self.rect)
        for bullet in self.bullets:
            pygame.draw.circle(screen, (255, 150, 0), (int(bullet[0]), int(bullet[1])), 5)
