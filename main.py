import pygame
from player import Player
from enemy import Enemy, EnemyDistance, EnemyShotgun, FinalBoss
from settings import WIDTH, HEIGHT, FPS
from menu import show_menu
from death_menu import DeathMenu
from resources import load_bullet_sprites
import random
import sys
import os

# Función para obtener la ruta absoluta de los archivos
def resource_path(relative_path):
    try:
        # Cuando se ejecuta desde el ejecutable
        base_path = sys._MEIPASS
    except AttributeError:
        # Cuando se ejecuta desde el entorno normal
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)

# Configurar pantalla completa
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Cargar la imagen de fondo
fondo_juego = pygame.image.load(resource_path("assets/fondo_juego.jpg"))

# Escalar el fondo al tamaño de la pantalla
fondo_juego = pygame.transform.scale(fondo_juego, (WIDTH, HEIGHT))

# Dibujar el fondo y aplicar el filtro oscuro
screen.blit(fondo_juego, (0, 0))



# Cargar música de fondo
musica_path = resource_path("./assets/audios/musica.mp3")
pygame.mixer.music.load(musica_path)

# Cargar efecto de disparo
sonido_disparo = pygame.mixer.Sound(resource_path("assets/audios/disparo.ogg")) # Cambia a un archivo OGG o WAV
sonido_disparo.set_volume(0.5)  # Ajustar volumen si es necesario

# Mostrar el menú principal
menu_action = show_menu(screen)
if menu_action == "exit":
    pygame.quit()
    sys.exit()
# Variables para las oleadas
bullet_sprites = load_bullet_sprites()
current_wave = 1
total_waves = 6  # 5 normales + 1 con el jefe final
wave_enemies_count = 6  # Número base de enemigos
enemies_to_spawn = []
wave_cleared = False
wave_transition_start_time = None
wave_transition_duration = 2000  # Duración en milisegundos (2 segundos)
player = Player(WIDTH // 2, HEIGHT // 2, bullet_sprites)


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
        enemy = random.choice([Enemy(x, y), EnemyDistance(x, y, bullet_sprites), EnemyShotgun(x, y, bullet_sprites)])
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
        final_boss = FinalBoss(x, y, bullet_sprites)
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
# Obtener la posición inicial del mouse
initial_mouse_pos = pygame.mouse.get_pos()
player.rotate_to_mouse(initial_mouse_pos)
start_wave(current_wave, player.rect.center)

enemies = []

# Temporizador para generar enemigos
enemy_spawn_timer = 0
enemy_spawn_interval = 1150  # Cada 1 segundos


# Estado inicial del juego
game_state = "playing"
# Variables de control de audio
musica_jugando = False  # Para evitar que la música se reinicie constantemente

running = True
final_boss = None

while running:
    if game_state == "playing":
        # Iniciar música si aún no está sonando
        if not musica_jugando:
            pygame.mixer.music.play(loops=-1)
            musica_jugando = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Botón izquierdo
                sonido_disparo.play()  # Reproduce el sonido al disparar
                mouse_x, mouse_y = pygame.mouse.get_pos()
                player.shoot(mouse_x, mouse_y)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                player.switch_weapon()  # Cambiar arma


        if not enemies and not enemies_to_spawn:
            wave_cleared = True

        if wave_cleared:
            wave_cleared = False
            current_wave += 1
            if current_wave <= total_waves:
                # El jugador recupera un 30% de su salud máxima al terminar la oleada
                heal_amount = int(player.max_health * 0.30)  # 30% de la salud máxima
                player.health = min(player.health + heal_amount, player.max_health)  # Recuperar salud, asegurándose de no exceder la salud máxima

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

                enemies.append(random.choice([Enemy(x, y), EnemyDistance(x, y, bullet_sprites), EnemyShotgun(x, y, bullet_sprites)]))

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

            final_boss = FinalBoss(x, y, bullet_sprites)

        # Actualizar lógica del jugador y enemigos
        player.update()
        player_pos = player.rect.center

        # Actualizar lógica del jugador y enemigos
        for enemy in enemies[:]:
            if isinstance(enemy, FinalBoss):
                enemy.update(player_pos, WIDTH, HEIGHT)
            else:
                enemy.update(player_pos)

            # Controlar disparo y movimiento de balas para enemigos que disparan
            if isinstance(enemy, (EnemyDistance, EnemyShotgun, FinalBoss)):
                enemy.shoot(player_pos)  # Enemigos disparan
                for bullet in enemy.bullets[:]:
                    bullet.update()
                    if bullet.is_out_of_bounds(WIDTH, HEIGHT or bullet.collides_with(player)):
                        enemy.bullets.remove(bullet)  # Eliminar balas fuera de pantalla

            # Verificar colisiones con las balas del jugador
            if enemy.check_collision_with_bullets(player.bullets):
                enemies.remove(enemy)


        # Verificar colisiones de las balas de enemigos con el jugador
        all_enemy_bullets = [
            bullet for enemy in enemies
            if isinstance(enemy, (EnemyDistance, EnemyShotgun, FinalBoss))
            for bullet in enemy.bullets
        ]
        if player.check_collision(enemies, [
            bullet for enemy in enemies if isinstance(enemy, (EnemyDistance, EnemyShotgun, FinalBoss))
            for bullet in enemy.bullets
        ]):
            game_state = "death_menu"
            pygame.mixer.music.stop()  # Detener música al morir
            musica_jugando = False
            death_menu = DeathMenu(screen)

        # Dibujar todo
        screen.blit(fondo_juego, (0, 0))  # Dibujar el fondo
        player.draw(screen)

        # Dibujar enemigos y sus balas
        for enemy in enemies:
            enemy.draw(screen, player.rect.center)
            for bullet in enemy.bullets:
                bullet.draw(screen)

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
                enemies.append(EnemyDistance(x, y, bullet_sprites))
            else:
                enemies.append(EnemyShotgun(x, y, bullet_sprites))


        
    elif game_state == "victory":
        # Detener la música si sigue sonando
        if musica_jugando:
            pygame.mixer.music.stop()
            musica_jugando = False  # Indicar que la música se detuvo

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # Cambiar al submenú de opciones post-victoria
                game_state = "post_victory"
                selected_option = 0  # Opción seleccionada inicialmente

        # Mostrar mensaje de victoria
        screen.blit(fondo_juego, (0, 0))
        font = pygame.font.Font(None, 74)
        text = font.render("¡Victoria! Presiona Enter para continuar.", True, (255, 255, 255))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()

    elif game_state == "post_victory":
        # Opciones del submenú
        options = ["Nueva partida", "Volver al menú principal"]
        option_rects = []  # Guardará las áreas de las opciones para detectar clics

        # Dibujar el submenú y calcular rectángulos
        screen.blit(fondo_juego, (0, 0))
        font = pygame.font.Font(None, 74)
        title = font.render("¡Victoria!", True, (255, 255, 255))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))

        option_rects.clear()
        for i, option in enumerate(options):
            color = (255, 255, 255) if i == selected_option else (200, 200, 200)
            text = font.render(option, True, color)
            text_x = WIDTH // 2 - text.get_width() // 2
            text_y = HEIGHT // 2 + i * 50
            screen.blit(text, (text_x, text_y))

            # Guardar el rectángulo para detectar clics
            rect = pygame.Rect(text_x, text_y, text.get_width(), text.get_height())
            option_rects.append(rect)

        pygame.display.flip()

        # Procesar eventos después de generar los rectángulos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEMOTION:
                # Detectar si el mouse está sobre alguna opción
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for i, rect in enumerate(option_rects):
                    if rect.collidepoint(mouse_x, mouse_y):
                        selected_option = i
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Botón izquierdo del mouse
                # Activar la opción seleccionada con un clic
                if selected_option == 0:  # Nueva partida
                    current_wave = 1
                    player.reset_health()  # Restablecer vida del jugador
                    player.reset_position(WIDTH // 2, HEIGHT // 2)  # Resetear posición
                    start_wave(current_wave, player_pos)
                    game_state = "playing"
                    # Reiniciar música para el juego
                    pygame.mixer.music.load("musica_juego.mp3")
                    pygame.mixer.music.play(-1)
                    musica_jugando = True
                elif selected_option == 1:  # Volver al menú principal
                    menu_action = show_menu(screen)
                    if menu_action == "exit":
                        running = False
                    elif menu_action == "start":
                        # Reiniciar variables si comienza desde el menú principal
                        enemies.clear()
                        enemies_to_spawn.clear()
                        current_wave = 0
                        wave_cleared = False
                        final_boss = None
                        player.reset_health()
                        player.reset_position(WIDTH // 2, HEIGHT // 2)
                        game_state = "playing"
                        # Reiniciar música para el juego
                        pygame.mixer.music.load(musica_path)
                        pygame.mixer.music.play(-1)
                        musica_jugando = True



        # Dibujar el submenú
        screen.blit(fondo_juego, (0, 0))
        font = pygame.font.Font(None, 74)
        title = font.render("¡Victoria!", True, (255, 255, 255))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))

        # Dibujar opciones y calcular rectángulos
        option_rects.clear()
        for i, option in enumerate(options):
            color = (255, 255, 255) if i == selected_option else (200, 200, 200)
            text = font.render(option, True, color)
            text_x = WIDTH // 2 - text.get_width() // 2
            text_y = HEIGHT // 2 + i * 50
            screen.blit(text, (text_x, text_y))

            # Guardar el rectángulo para detectar clics
            rect = pygame.Rect(text_x, text_y, text.get_width(), text.get_height())
            option_rects.append(rect)

        pygame.display.flip()





    elif game_state == "death_menu":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            selected_option = death_menu.handle_input(event)
            if selected_option == 0:  # Reintentar
                # Limpiar todos los enemigos y reiniciar las variables del juego
                enemies.clear()  # Limpiar enemigos
                enemies_to_spawn.clear()  # Limpiar enemigos a generar
                current_wave = 0  # Reiniciar oleada a 1
                wave_cleared = False  # Asegurarse de que la oleada no esté marcada como limpia
                final_boss = None  # Asegurarse de que el jefe final esté reiniciado
                player.reset_position(WIDTH // 2, HEIGHT // 2)  # Resetear la posición del jugador
                game_state = "playing"  # Volver al estado de juego
            elif selected_option == 1:  # Menú Principal
                menu_action = show_menu(screen)
                if menu_action == "exit":
                    running = False
                elif menu_action == "start":
                    # Limpiar enemigos y otras variables
                    enemies.clear()  
                    enemies_to_spawn.clear()
                    current_wave = 0  # Reiniciar oleada a 1
                    wave_cleared = False
                    final_boss = None

                    player.reset_position(WIDTH // 2, HEIGHT // 2)  # Resetear la posición del jugador
                    game_state = "playing"  # Volver al estado de juego

        death_menu.draw()
        pygame.display.flip()
        clock.tick(FPS)
