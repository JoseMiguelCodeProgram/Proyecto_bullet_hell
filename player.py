import pygame
import math
import random
from settings import WIDTH, HEIGHT, player_size
from bullet import Bullet, BulletType

class Player:
    def __init__(self, x, y, bullet_sprites):
        self.rect = pygame.Rect(x, y, player_size, player_size)
        self.bullets = []
        self.health = 10
        self.max_health = 10  # Salud máxima
        self.invulnerable = False
        self.invulnerability_time = 0
        self.last_hit_time = 0
        self.weapons = [BulletType.NORMAL, BulletType.SHOTGUN]
        self.current_weapon_index = 0

        self.bullet_sprites = bullet_sprites  # Agrega esta línea

        # Animación del jugador
        self.sprites = [
            pygame.transform.scale(pygame.image.load(f"./assets/player/jugador_{i}.png"), (player_size, player_size))
            for i in range(1, 6)
        ]
        self.current_frame = 0
        self.animation_speed = 0.1
        self.animation_timer = 0


    def update(self):
        # Movimiento
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.x > 0:
            self.rect.x -= 5
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.x < WIDTH - player_size:
            self.rect.x += 5
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.rect.y > 0:
            self.rect.y -= 5
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.rect.y < HEIGHT - player_size:
            self.rect.y += 5

        # Actualizar animación
        self.animation_timer += self.animation_speed
        if self.animation_timer >= 1:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.sprites)

        # Actualizar balas
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.is_out_of_bounds(WIDTH, HEIGHT):
                self.bullets.remove(bullet)

        # Reducir el tiempo de invulnerabilidad
        if self.invulnerable:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_hit_time >= self.invulnerability_time:
                self.invulnerable = False

    def draw(self, screen):
        # Calcular el ángulo hacia el mouse
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dx = mouse_x - self.rect.centerx
        dy = mouse_y - self.rect.centery
        angle = math.degrees(math.atan2(-dy, dx))  # -dy porque el eje Y está invertido

        # Rotar el sprite del jugador
        rotated_sprite = pygame.transform.rotate(self.sprites[self.current_frame], angle)
        rotated_rect = rotated_sprite.get_rect(center=self.rect.center)

        # Dibujar la sombra
        shadow_color = (0, 150, 50, 100)  # Gris oscuro con transparencia
        shadow_surface = pygame.Surface((player_size, player_size), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surface, shadow_color, (0, 0, player_size, player_size))
        screen.blit(shadow_surface, (self.rect.x, self.rect.y + player_size//4))
        
        # Dibujar sprite rotado
        screen.blit(rotated_sprite, rotated_rect)

        # Dibujar barra de vida
        pygame.draw.rect(screen, (0, 0, 255), (self.rect.x, self.rect.y - 10, player_size * (self.health / 10), 5))

        # Dibujar las balas
        for bullet in self.bullets:
            bullet.draw(screen)

    def shoot(self, mouse_x, mouse_y):
        current_weapon = self.weapons[self.current_weapon_index]
    
        dx = mouse_x - self.rect.centerx
        dy = mouse_y - self.rect.centery
        distance = math.sqrt(dx**2 + dy**2)
        if distance != 0:
            dx /= distance
            dy /= distance
    
        if current_weapon == BulletType.NORMAL:
            # Disparo normal con animación
            new_bullet = Bullet(
                x=self.rect.centerx,
                y=self.rect.centery,
                dx=dx,
                dy=dy,
                speed=10,
                color=(255, 255, 0),
                damage=1,
                bullet_type=BulletType.NORMAL,
                sprites=self.bullet_sprites["normal"],
                size=30
            )
            self.bullets.append(new_bullet)
    
        elif current_weapon == BulletType.SHOTGUN:
            # Disparo tipo escopeta con animación
            spread_angle = 45  # Ángulo total del abanico
            bullet_count = 5  # Número de balas
            for i in range(bullet_count):
                spread = (i - bullet_count // 2) * (spread_angle / bullet_count)
                angle = math.atan2(dy, dx) + math.radians(spread)
                bullet_dx = math.cos(angle)
                bullet_dy = math.sin(angle)
                new_bullet = Bullet(
                    x=self.rect.centerx,
                    y=self.rect.centery,
                    dx=bullet_dx,
                    dy=bullet_dy,
                    speed=8,
                    color=(255, 100, 0),
                    damage=2,
                    bullet_type=BulletType.SHOTGUN,
                    sprites=self.bullet_sprites["shotgun"],
                    size=30
                )
                self.bullets.append(new_bullet)


    def reset_position(self, x, y):
        """Reinicia la posición del jugador."""
        self.rect.center = (x, y)
        self.health = 10

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
        # Verificar colisiones con enemigos
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                if self.take_damage():
                    return True

        # Verificar colisiones con balas enemigas
        for bullet in bullets:
            if self.rect.collidepoint(bullet.x, bullet.y):  # Extraer coordenadas de la bala
                bullets.remove(bullet)  # Eliminar la bala que colisiona
                if self.take_damage():
                    return True

        return False

    
    def switch_weapon(self):
        """Cambiar al siguiente arma disponible."""
        self.current_weapon_index = (self.current_weapon_index + 1) % len(self.weapons)

    def rotate_to_mouse(self, mouse_pos):
        dx = mouse_pos[0] - self.rect.centerx
        dy = mouse_pos[1] - self.rect.centery
        angle = math.degrees(math.atan2(dy, dx))  # -dy porque el eje Y está invertido
        self.sprites = [pygame.transform.rotate(sprite, angle) for sprite in self.sprites]
