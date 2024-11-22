import pygame
from player import Player
from enemy import Enemy, EnemyDistance, EnemyShotgun
from settings import WIDTH, HEIGHT, FPS
from menu import show_menu
from death_menu import DeathMenu
import random

pygame.init()

# Configurar pantalla completa
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
clock = pygame.time.Clock()

# Cargar la imagen de fondo
fondo_juego = pygame.image.load("./assets/fondo_juego.jpg")
fondo_juego = pygame.transform.scale(fondo_juego, (WIDTH, HEIGHT))  # Ajustar al tamaño de la pantalla

# Mostrar el menú principal
menu_action = show_menu(screen)
if menu_action == "exit":
    pygame.quit()
    exit()

# Inicialización del jugador y lista de enemigos
player = Player(WIDTH // 2, HEIGHT // 2)
enemies = []

# Temporizador para generar enemigos
enemy_spawn_timer = 0
enemy_spawn_interval = 2000  # Cada 2 segundos

# Estado inicial del juego
game_state = "playing"

# Bucle principal
running = True
while running:
    if game_state == "playing":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                player.shoot(mouse_x, mouse_y)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:  # Cambiar arma con 'E'
                    player.switch_weapon()

        # Generar enemigos
        enemy_spawn_timer += clock.get_time()
        if enemy_spawn_timer >= enemy_spawn_interval:
            enemy_spawn_timer = 0
            edge = random.choice(["top", "bottom", "left", "right"])
            if edge == "top":
                x, y = random.randint(0, WIDTH), 0
            elif edge == "bottom":
                x, y = random.randint(0, WIDTH), HEIGHT
            elif edge == "left":
                x, y = 0, random.randint(0, HEIGHT)
            elif edge == "right":
                x, y = WIDTH, random.randint(0, HEIGHT)

            # Generar tipo de enemigo
            rand = random.random()
            if rand < 0.4:
                enemies.append(Enemy(x, y))
            elif rand < 0.8:
                enemies.append(EnemyDistance(x, y))
            else:
                enemies.append(EnemyShotgun(x, y))

        # Actualizar lógica del jugador y enemigos
        player.update()
        player_pos = player.rect.center

        for enemy in enemies[:]:
            enemy.update(player_pos)
            if isinstance(enemy, (EnemyDistance, EnemyShotgun)):
                enemy.shoot(player_pos)
                enemy.update_bullets()
            if enemy.check_collision_with_bullets(player.bullets):
                enemies.remove(enemy)

        # Verificar colisiones
        all_enemy_bullets = [
            bullet for enemy in enemies
            if isinstance(enemy, (EnemyDistance, EnemyShotgun))
            for bullet in enemy.bullets
        ]
        if player.check_collision(enemies, all_enemy_bullets):
            game_state = "death_menu"  # Cambiar al menú de muerte
            death_menu = DeathMenu(screen)

        # Dibujar todo
        screen.blit(fondo_juego, (0, 0))  # Dibujar el fondo
        player.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    elif game_state == "death_menu":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            selected_option = death_menu.handle_input(event)
            if selected_option == 0:  # Reintentar
                enemies.clear()
                player.reset_position(WIDTH // 2, HEIGHT // 2)
                game_state = "playing"
            elif selected_option == 1:  # Menú Principal
                menu_action = show_menu(screen)
                if menu_action == "exit":
                    running = False
                elif menu_action == "start":
                    enemies.clear()
                    player.reset_position(WIDTH // 2, HEIGHT // 2)
                    game_state = "playing"

        death_menu.draw()
        pygame.display.flip()
        clock.tick(FPS)
