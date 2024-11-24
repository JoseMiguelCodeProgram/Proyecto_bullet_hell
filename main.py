import pygame
from player import Player
from enemy import Enemy, EnemyDistance, EnemyShotgun, FinalBoss
from settings import WIDTH, HEIGHT, FPS
from menu import show_menu
from death_menu import DeathMenu
import random

pygame.init()

# Configurar pantalla completa
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Cargar la imagen de fondo
fondo_juego = pygame.image.load("./assets/fondo_juego.jpg")
fondo_juego = pygame.transform.scale(fondo_juego, (WIDTH, HEIGHT))  # Ajustar al tamaño de la pantalla

# Mostrar el menú principal
menu_action = show_menu(screen)
if menu_action == "exit":
    pygame.quit()
    exit()
# Variables para las oleadas
current_wave = 1
total_waves = 6  # 5 normales + 1 con el jefe final
wave_enemies_count = 1  # Número base de enemigos
enemies_to_spawn = []
wave_cleared = False
wave_transition_start_time = None
wave_transition_duration = 2000  # Duración en milisegundos (2 segundos)


def start_wave(wave_number, player_pos):
    """Inicia una nueva oleada basada en el número de la oleada."""
    global enemies_to_spawn, wave_enemies_count
    enemies_to_spawn.clear()  # Asegurar que la lista esté vacía
    num_enemies = wave_enemies_count + (wave_number - 1) * 3  # Incrementa enemigos por oleada

    # Generar enemigos regulares
    for _ in range(num_enemies):
        edge = random.choice(["top", "bottom", "left", "right"])
        if edge == "top":
            x, y = random.randint(0, WIDTH), 0
        elif edge == "bottom":
            x, y = random.randint(0, WIDTH), HEIGHT
        elif edge == "left":
            x, y = 0, random.randint(0, HEIGHT)
        elif edge == "right":
            x, y = WIDTH, random.randint(0, HEIGHT)

        # Crear enemigo aleatorio y rotarlo hacia el jugador
        enemy = random.choice([Enemy(x, y), EnemyDistance(x, y), EnemyShotgun(x, y)])
        enemy.set_angle_to_player(player_pos)  # Configura el ángulo hacia el jugador
        enemies_to_spawn.append(enemy)

    # Generar el jefe en la última oleada
    if wave_number == 6:
        edge = random.choice(["top", "bottom", "left", "right"])
        if edge == "top":
            x, y = random.randint(0, WIDTH), 0
        elif edge == "bottom":
            x, y = random.randint(0, WIDTH), HEIGHT
        elif edge == "left":
            x, y = 0, random.randint(0, HEIGHT)
        elif edge == "right":
            x, y = WIDTH, random.randint(0, HEIGHT)
        
        # Crear y añadir al jefe final
        final_boss = FinalBoss(x, y)
        final_boss.set_angle_to_player(player_pos)
        enemies_to_spawn.append(final_boss)



def draw_wave_message(screen, wave_number):
    """Dibuja el mensaje de la oleada en el centro de la pantalla."""
    font = pygame.font.Font(None, 74)
    text = font.render(f"Oleada {wave_number}", True, (255, 255, 255))
    shadow = font.render(f"Oleada {wave_number}", True, (0, 0, 0))  # Sombra del texto
    screen.blit(shadow, (WIDTH // 2 - shadow.get_width() // 2 + 2, HEIGHT // 2 - shadow.get_height() // 2 + 2))
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))


# Inicialización del jugador y lista de enemigos
player = Player(WIDTH // 2, HEIGHT // 2)
# Obtener la posición inicial del mouse
initial_mouse_pos = pygame.mouse.get_pos()
player.rotate_to_mouse(initial_mouse_pos)
start_wave(current_wave, player.rect.center)

enemies = []

# Temporizador para generar enemigos
enemy_spawn_timer = 0
enemy_spawn_interval = 2000  # Cada 2 segundos

# Estado inicial del juego
game_state = "playing"

# Bucle principal
running = True
final_boss =  None
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
        if not enemies and not enemies_to_spawn:
            wave_cleared = True

        if wave_cleared:
            wave_cleared = False
            current_wave += 1
            if current_wave <= total_waves:
                # Iniciar la transición antes de la nueva oleada
                game_state = "wave_transition"
                wave_transition_start_time = pygame.time.get_ticks()
            else:
                game_state = "victory"  # Estado de victoria tras el jefe final
        
        # Generar enemigos si quedan por generar
        if enemies_to_spawn:
            enemy_spawn_timer += clock.get_time()
            if enemy_spawn_timer >= enemy_spawn_interval:
                enemy_spawn_timer = 0
                enemies.append(enemies_to_spawn.pop(0))
                
                
        # Generar enemigos continuamente si el jefe está vivo
        if current_wave == 6 and final_boss is not None and final_boss.health > 0:
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

                enemies.append(random.choice([Enemy(x, y), EnemyDistance(x, y), EnemyShotgun(x, y)]))
        
        # Inicializar al jefe final en la última oleada
        if current_wave == 6 and final_boss is None:
            edge = random.choice(["top", "bottom", "left", "right"])
            if edge == "top":
                x, y = random.randint(0, WIDTH), 0
            elif edge == "bottom":
                x, y = random.randint(0, WIDTH), HEIGHT
            elif edge == "left":
                x, y = 0, random.randint(0, HEIGHT)
            elif edge == "right":
                x, y = WIDTH, random.randint(0, HEIGHT)

            final_boss = FinalBoss(x, y)

                
        # Actualizar lógica del jugador y enemigos
        player.update()
        player_pos = player.rect.center

        for enemy in enemies[:]:
            if isinstance(enemy, FinalBoss):
                enemy.update(player_pos, WIDTH, HEIGHT)
            else:
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
            enemy.draw(screen, player.rect.center)
        pygame.display.flip()
        clock.tick(FPS)
        
        
    # Lógica para el estado de transición entre oleadas
    elif game_state == "wave_transition":
        current_time = pygame.time.get_ticks()
        if current_time - wave_transition_start_time >= wave_transition_duration:
            # Finalizar la transición y comenzar la oleada
            game_state = "playing"
            start_wave(current_wave, player_pos)# Include player_pos here

        else:
            # Dibujar mensaje de la oleada
            screen.blit(fondo_juego, (0, 0))  # Dibujar el fondo
            draw_wave_message(screen, current_wave)
            pygame.display.update()  # Cambiado de flip() a update() para evitar interferencias con otras actualizaciones
            clock.tick(FPS)  # Mantener el framerate estable
            
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


        
    elif game_state == "victory":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Volver al menú
                    menu_action = show_menu(screen)
                    if menu_action == "exit":
                        running = False
                    else:
                        current_wave = 1
                        start_wave(current_wave)
                        game_state = "playing"

        # Dibujar mensaje de victoria
        font = pygame.font.Font(None, 74)
        text = font.render("¡Victoria! Presiona Enter para continuar.", True, (255, 255, 255))
        screen.blit(fondo_juego, (0, 0))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()


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
