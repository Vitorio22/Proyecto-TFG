import pygame
from games.BlockAttack.screens.intro import Intro

class Main:
    def __init__(self):
        # Inicializamos pygame
        pygame.init()

        # Inicializamos el mixer de pygame para reproducir sonidos
        pygame.mixer.init()

        # Crear una instancia de la clase Intro
        
        Intro(pygame.display.set_mode((900, 600)))