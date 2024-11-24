import pygame
from settings import WIDTH, HEIGHT
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

class DeathMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 70)
        self.options = ["Reintentar", "Menú Principal"]
        self.selected_option = 0
        # Cargar y escalar la imagen de fondo
        self.background = pygame.image.load(resource_path('./assets/game_over.jpg'))
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

    def draw(self):
        """Dibuja el menú de muerte."""
        # Dibujar la imagen de fondo
        self.screen.blit(self.background, (0, 0))

        # Dibujar el texto del título
        title_text = self.font.render("¡Has Muerto!", True, (255, 0, 0))
        self.screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))

        # Dibujar las opciones
        for i, option in enumerate(self.options):
            color = (255, 255, 255) if i != self.selected_option else (255, 255, 0)
            option_text = self.font.render(option, True, color)
            option_rect = option_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 80))
            self.screen.blit(option_text, option_rect)

    def handle_input(self, event):
        """Gestiona la entrada del usuario para navegar por las opciones."""
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        # Detectar navegación con teclado
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:  # Selección con Enter
                return self.selected_option

        # Detectar navegación con el mouse
        for i, option in enumerate(self.options):
            option_text = self.font.render(option, True, (255, 255, 255))
            option_rect = option_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 80))
            if option_rect.collidepoint(mouse_pos):
                self.selected_option = i  # Cambiar opción seleccionada con el mouse
                if mouse_click[0]:  # Seleccionar con clic izquierdo
                    return self.selected_option
        return None
