import pygame
import math
import random
from settings import WIDTH, HEIGHT
from bullet import Bullet, BulletType

class Enemy:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.speed = random.uniform(2.0, 6.0)
        self.health = random.randint(3, 6)

        # Animación del enemigo
        self.sprites = [
            pygame.transform.scale(pygame.image.load(f"./assets/enemy/enemy_simple_{i}.png"), (150, 150))
            for i in range(1, 9)
        ]
        self.current_frame = 0
        self.animation_speed = 0.1
        self.animation_timer = 0

        self.angle = 0  # Ángulo inicial hacia el jugador
        
    def set_angle_to_player(self, player_pos):
        """Configura el ángulo hacia el jugador."""
        dx = player_pos[0] - self.rect.centerx
        dy = player_pos[1] - self.rect.centery
        self.angle = math.degrees(math.atan2(-dy, dx))  # Calcula el ángulo inicial hacia el jugador
    
    def update(self, player_pos):
        dx = player_pos[0] - self.rect.centerx
        dy = player_pos[1] - self.rect.centery
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance != 0:
            dx /= distance
            dy /= distance

        # Movimiento
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

        # Actualizar animación
        self.animation_timer += self.animation_speed
        if self.animation_timer >= 1:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.sprites)

    def draw(self, screen, player_pos):
        # Calcular el ángulo hacia el jugador
        dx = player_pos[0] - self.rect.centerx
        dy = player_pos[1] - self.rect.centery
        angle = math.degrees(math.atan2(-dy, dx)) - 90  # Ajustar según orientación del sprite

        # Rotar el sprite del enemigo
        rotated_sprite = pygame.transform.rotate(self.sprites[self.current_frame], angle)
        rotated_rect = rotated_sprite.get_rect(center=self.rect.center)  # Mantener el centro

        # Dibujar sprite rotado
        screen.blit(rotated_sprite, rotated_rect.topleft)

        # Dibujar barra de vida
        pygame.draw.rect(
            screen,
            (0, 255, 100),
            (self.rect.x, self.rect.y - 10, 50 * (self.health / 6), 5),
        )



    def take_damage(self):
        """Reduce la vida del enemigo y devuelve True si muere."""
        self.health -= 1
        return self.health <= 0
    
    def check_collision_with_bullets(self, bullets):
        for bullet in bullets:
            if self.rect.collidepoint(bullet.x, bullet.y):
                bullets.remove(bullet)
                if self.take_damage():
                    return True
        return False



class EnemyDistance(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.bullets = []
        self.reload_time = 1000  # Tiempo de recarga (en milisegundos)
        self.last_shot_time = 0  # Tiempo del último disparo
        self.sprites = [
            pygame.transform.scale(pygame.image.load(f"./assets/enemy_distance/enemy_distance_{i}.png"), (100, 100))
            for i in range(1, 5)
        ]

    def shoot(self, player_pos):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.reload_time:
            self.last_shot_time = current_time  # Actualizar tiempo del último disparo
            
            # Calcular dirección hacia el jugador
            dx = player_pos[0] - self.rect.centerx
            dy = player_pos[1] - self.rect.centery
            distance = math.sqrt(dx**2 + dy**2)
            if distance != 0:
                dx /= distance
                dy /= distance
            
            # Crear una nueva bala
            new_bullet = Bullet(
                x=self.rect.centerx,
                y=self.rect.centery,
                dx=dx,
                dy=dy,
                speed=6,
                color=(255, 0, 0),
                damage=1,
                bullet_type=BulletType.NORMAL
            )
            self.bullets.append(new_bullet)

    def update_bullets(self):
        """Actualizar las balas disparadas por el enemigo."""
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.is_out_of_bounds(WIDTH, HEIGHT):
                self.bullets.remove(bullet)

    def draw(self, screen, player_pos):
        super().draw(screen, player_pos)
        for bullet in self.bullets:
            bullet.draw(screen)
            
        pygame.draw.rect(screen, (0, 255, 100), (self.rect.x, self.rect.y - 10, 50 * (self.health / 6), 5))


class EnemyShotgun(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.reload_time = random.randint(1000, 1500)  # Tiempo de recarga más largo
        self.bullets = []
        self.last_shot_time = 0
        self.bullet_speed = 7  # Velocidad de las balas
        self.bullet_count = 5  # Número de balas disparadas
        self.spread_angle = 45  # Ángulo total del abanico en grados
        self.sprites = [
            pygame.transform.scale(pygame.image.load(f"./assets/enemy_shotgun/enemy_shotgun_{i}.png"), (100, 100))
            for i in range(1, 7)
        ]
        self.current_frame = 0  # Animación del enemigo
        self.animation_speed = 0.1
        self.animation_timer = 0

    def shoot(self, player_pos):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.reload_time:
            # Calcular el ángulo hacia el jugador
            dx = player_pos[0] - self.rect.centerx
            dy = player_pos[1] - self.rect.centery
            angle_to_player = math.atan2(dy, dx)  # Ángulo en radianes hacia el jugador

            # Generar balas en un abanico
            for i in range(self.bullet_count):
                spread = (i - self.bullet_count // 2) * (self.spread_angle / self.bullet_count)
                angle = angle_to_player + math.radians(spread)  # Ángulo de cada bala
                bullet_dx = math.cos(angle)  # Dirección X de la bala
                bullet_dy = math.sin(angle)  # Dirección Y de la bala

                # Crear una nueva bala
                new_bullet = Bullet(
                    x=self.rect.centerx,
                    y=self.rect.centery,
                    dx=bullet_dx,
                    dy=bullet_dy,
                    speed=self.bullet_speed,
                    color=(255, 150, 0),  # Color específico para estas balas
                    damage=2  # Daño de cada bala de escopeta
                )
                self.bullets.append(new_bullet)

            self.last_shot_time = current_time

    def update(self, player_pos):
        """Actualiza el movimiento, las balas y la rotación."""
        super().update(player_pos)  # Movimiento básico hacia el jugador
        self.update_bullets()  # Actualizar las balas

    def update_bullets(self):
        """Actualizar las balas y eliminarlas si salen de la pantalla."""
        for bullet in self.bullets[:]:
            bullet.update()  # Método de actualización de cada bala
            if bullet.is_out_of_bounds(WIDTH, HEIGHT):  # Verificar si la bala salió de los límites
                self.bullets.remove(bullet)

    def draw(self, screen, player_pos):
        """Dibuja al enemigo Shotgun con rotación y sus balas."""
        # Llama al método `draw` de la clase base
        super().draw(screen, player_pos)

        # Dibujar las balas del shotgun
        for bullet in self.bullets:
            bullet.draw(screen)

class FinalBoss(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.health = 50  # Salud alta
        self.reload_time = 400  # Reducimos el tiempo para disparar más rápido (doble de velocidad)
        self.bullets = []
        self.last_shot_time = 0

        # Cargar el sprite único del jefe
        self.sprite = pygame.transform.scale(
            pygame.image.load("./assets/enemy_boss/enemy_boss.png"), (150, 150)
        )  # Ajusta el tamaño según sea necesario

    def shoot(self, player_pos):
        """Dispara múltiples balas tipo SHOTGUN hacia el jugador."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.reload_time:
            self.last_shot_time = current_time

            # Disparo tipo escopeta: balas en un cono
            for angle_offset in range(-30, 31, 15):
                angle = math.atan2(
                    player_pos[1] - self.rect.centery,
                    player_pos[0] - self.rect.centerx,
                ) + math.radians(angle_offset)
                dx = math.cos(angle)
                dy = math.sin(angle)
                new_bullet = Bullet(
                    x=self.rect.centerx,
                    y=self.rect.centery,
                    dx=dx,
                    dy=dy,
                    speed=10,  # Velocidad personalizada
                    color=(255, 50, 50),  # Color rojo para las balas del jefe
                    damage=5,  # Más daño porque es el jefe
                    bullet_type=BulletType.SHOTGUN  # Usar el tipo SHOTGUN
                )
                self.bullets.append(new_bullet)

    def update(self, player_pos, width, height):
        """Actualiza el movimiento del jefe, dispara y elimina balas fuera de pantalla."""
        super().update(player_pos)
        self.shoot(player_pos)

        # Actualizar posición de las balas
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.is_out_of_bounds(width, height):  # Eliminar balas fuera de pantalla
                self.bullets.remove(bullet)

    def draw(self, screen, player_pos):
        """Dibuja al jefe con rotación, barra de salud y sus balas."""
        # Calcular el ángulo hacia el jugador
        dx = player_pos[0] - self.rect.centerx
        dy = player_pos[1] - self.rect.centery
        angle = math.degrees(math.atan2(-dy, dx))  # -dy porque el eje Y está invertido

        # Rotar el sprite único
        rotated_sprite = pygame.transform.rotate(self.sprite, angle)
        rotated_rect = rotated_sprite.get_rect(center=self.rect.center)

        # Dibujar el sprite rotado
        screen.blit(rotated_sprite, rotated_rect.topleft)

        # Dibujar barra de salud extendida
        pygame.draw.rect(
            screen,
            (255, 0, 0),  # Color rojo para la barra de salud
            (self.rect.x, self.rect.y - 20, 100 * (self.health / 50), 10),  # Barra extendida
        )

        # Dibujar las balas del jefe
        for bullet in self.bullets:
            bullet.draw(screen)
