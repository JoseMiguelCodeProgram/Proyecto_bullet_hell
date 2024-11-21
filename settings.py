import pygame

# Inicializar Pygame antes de cualquier cosa
pygame.init()

# Luego, puedes obtener la información de la pantalla
screen_info = pygame.display.Info()
WIDTH = screen_info.current_w
HEIGHT = screen_info.current_h
FPS = 60
player_size = 50
