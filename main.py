import pygame
from player import Player
from enemy import Enemy, EnemyDistance, EnemyShotgun
from settings import WIDTH, HEIGHT, FPS
import random

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Inicialización del jugador y lista de enemigos
player = Player(WIDTH // 2, HEIGHT // 2)
enemies = []

# Temporizador para generar enemigos
enemy_spawn_timer = 0
enemy_spawn_interval = 2000  # Cada 2 segundos

# Main Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            player.shoot(mouse_x, mouse_y)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:  # Cambiar arma con 'E'
                player.switch_weapon()

    # Generar enemigos (lógica corregida para aparecer en bordes)
    enemy_spawn_timer += clock.get_time()
    if enemy_spawn_timer >= enemy_spawn_interval:
        enemy_spawn_timer = 0

        # Elegir un borde: 0=superior, 1=inferior, 2=izquierdo, 3=derecho
        edge = random.choice(["top", "bottom", "left", "right"])
        if edge == "top":
            x = random.randint(0, WIDTH)  # Posición horizontal aleatoria
            y = 0  # En el borde superior
        elif edge == "bottom":
            x = random.randint(0, WIDTH)  # Posición horizontal aleatoria
            y = HEIGHT  # En el borde inferior
        elif edge == "left":
            x = 0  # En el borde izquierdo
            y = random.randint(0, HEIGHT)  # Posición vertical aleatoria
        elif edge == "right":
            x = WIDTH  # En el borde derecho
            y = random.randint(0, HEIGHT)  # Posición vertical aleatoria
            
        # Generar tipo de enemigo
        rand = random.random()
        if rand < 0.4:  # 40% probabilidad de enemigo normal
            enemies.append(Enemy(x, y))
        elif rand < 0.8:  # 40% probabilidad de enemigo a distancia
            enemies.append(EnemyDistance(x, y))
        else:  # 20% probabilidad de enemigo con escopeta
            enemies.append(EnemyShotgun(x, y))


    # Actualizar lógica del jugador y enemigos
    player.update()
    player_pos = player.rect.center

    # Actualizar lógica de los enemigos
    for enemy in enemies[:]:  # Iterar sobre los enemigos
        enemy.update(player_pos)

        # Si es un enemigo a distancia, disparar y mover balas
        if isinstance(enemy, EnemyDistance):
            enemy.shoot(player_pos)
            enemy.update_bullets()

        # Si es un enemigo con escopeta, disparar y mover balas
        elif isinstance(enemy, EnemyShotgun):
            enemy.shoot(player_pos)
            enemy.update_bullets()

        # Verificar colisiones con las balas del jugador
        if enemy.check_collision_with_bullets(player.bullets):
            enemies.remove(enemy)  # Eliminar enemigo si muere

    # Verificar colisiones del jugador
    all_enemy_bullets = [
        bullet for enemy in enemies 
        if isinstance(enemy, (EnemyDistance, EnemyShotgun)) 
        for bullet in enemy.bullets
    ]
    if player.check_collision(enemies, all_enemy_bullets):
        print("¡El jugador murió!")
        running = False

    # Dibujar todo
    screen.fill((0, 0, 0))
    player.draw(screen)
    for enemy in enemies:
        enemy.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)
