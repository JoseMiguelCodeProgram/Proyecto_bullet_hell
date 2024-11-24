import pygame
from settings import WIDTH, HEIGHT
import os
import sys

def resource_path(relative_path):
    try:
        # Cuando se ejecuta desde un ejecutable
        base_path = sys._MEIPASS
    except AttributeError:
        # Cuando se ejecuta en el entorno de desarrollo
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

pygame.init()

# Colores
WHITE = (255, 255, 255)
GREEN = (10, 150, 50)
BLACK_TRANSPARENT = (0, 0, 0, 150)  # Negro semitransparente

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 100)
        self.small_font = pygame.font.Font(None, 50)
        self.options = ["Start Game", "Instructions", "Exit"]
        self.selected_option = 0
        self.show_instructions = False

        # Cargar la imagen de fondo
        self.background = pygame.image.load(resource_path('assets/Background.jpg'))
        # Ajustar la imagen para que cubra toda la pantalla
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

    def draw(self):
        self.screen.blit(self.background, (0, 0))  # Dibujar la imagen de fondo

        # Dibujar título con fondo
        title_bg = pygame.Surface((WIDTH, 120), pygame.SRCALPHA)  # Fondo transparente para el título
        title_bg.fill(BLACK_TRANSPARENT)
        self.screen.blit(title_bg, (0, 30))
        title = self.font.render("Plantz Assault", True, GREEN)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

        if not self.show_instructions:
            # Dibujar opciones del menú
            mouse_pos = pygame.mouse.get_pos()
            for i, option in enumerate(self.options):
                option_rect = pygame.Rect(
                    WIDTH // 2 - 150, 200 + i * 70, 300, 60
                )  # Área interactiva de la opción

                # Fondo para cada opción
                option_bg = pygame.Surface((300, 60), pygame.SRCALPHA)
                option_bg.fill(BLACK_TRANSPARENT)
                self.screen.blit(option_bg, option_rect.topleft)

                # Cambiar color del texto al pasar el mouse
                color = GREEN if option_rect.collidepoint(mouse_pos) else WHITE
                text = self.small_font.render(option, True, color)
                self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 210 + i * 70))
        else:
            # Dibujar instrucciones con fondo
            instructions_bg = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            instructions_bg.fill(BLACK_TRANSPARENT)
            self.screen.blit(instructions_bg, (0, 0))

            instructions_title = self.font.render("Instructions", True, WHITE)
            self.screen.blit(instructions_title, (WIDTH // 2 - instructions_title.get_width() // 2, 100))

            instructions_text = [
                "Use arrow keys to move.",
                "or 'WASD'",
                "Click to shoot.",
                "Press 'E' to switch weapons.",
                "Press 'Esc' to go back to the menu."
            ]
            y_offset = 200
            for line in instructions_text:
                text = self.small_font.render(line, True, WHITE)
                self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y_offset))
                y_offset += 50

    def handle_input(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        if not self.show_instructions:
            for i, option in enumerate(self.options):
                option_rect = pygame.Rect(
                    WIDTH // 2 - 150, 200 + i * 70, 300, 60
                )  # Área interactiva de la opción
                if option_rect.collidepoint(mouse_pos) and mouse_click[0]:  # Click izquierdo
                    return i
        else:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:  # Regresar al menú con 'Esc'
                self.show_instructions = False
        return None
    

def show_menu(screen):
    menu = Menu(screen)
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
        
        selected = menu.handle_input()
        if selected == 0:  # Start Game
            return "start"
        elif selected == 1:  # Instructions
            menu.show_instructions = True  # Mostrar instrucciones
        elif selected == 2:  # Exit
            return "exit"

        menu.draw()
        pygame.display.flip()
        clock.tick(30)
