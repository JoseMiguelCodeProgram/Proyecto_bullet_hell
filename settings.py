import pygame

# Inicializar Pygame antes de cualquier cosa
pygame.init()

# Luego, puedes obtener la información de la pantalla
screen_info = pygame.display.Info()
WIDTH, HEIGHT = pygame.display.get_desktop_sizes()[0]

FPS = 60
player_size = 50
