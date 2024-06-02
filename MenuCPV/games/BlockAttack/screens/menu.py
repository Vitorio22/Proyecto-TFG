import pygame, random
from games.BlockAttack.screens.blockAttack import Game

pygame.init()

class MainMenu:
    def draw_controls(self):
        
        # Tamaño de la pantalla
        SCREEN_WIDTH = 900
        SCREEN_HEIGHT = 600
        # Colores
        COLOR_BLACK = (0, 0, 0)
        COLOR_PURPLE = (170, 0, 255)
        NEON_GREEN = (57, 255, 20)
        
        control_text = [
            "CONTROLES",
            "Mover la barra: Flechas de dirección",
            "Salir: Esc"
        ]
        control_font = pygame.font.Font("games/BlockAttack/assets/fonts/Neon.ttf", 40)
        control_surf = pygame.Surface((SCREEN_WIDTH // 2 + 100, SCREEN_HEIGHT // 2))
        control_surf.fill(COLOR_BLACK)
        
        # Dibujar el texto de los controles
        for i, text in enumerate(control_text):
            control_render = control_font.render(text, True, NEON_GREEN)
            control_rect = control_render.get_rect(center=(SCREEN_WIDTH // 4 + 50, (SCREEN_HEIGHT // 4 - 50) + (i * 50)))
            control_surf.blit(control_render, control_rect)

        self.screen.blit(control_surf, control_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
        pygame.draw.rect(self.screen, COLOR_PURPLE, control_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)), 3, border_radius=5)
      
        # Dibujar el botón de volver al menú
        button_font = pygame.font.Font("games/BlockAttack/assets/fonts/Neon.ttf", 50)
        button_text = button_font.render("Volver", True, NEON_GREEN)
        button_rect = button_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
        pygame.draw.rect(self.screen, COLOR_BLACK, button_rect)
        pygame.draw.rect(self.screen, COLOR_PURPLE, button_rect, 3, border_radius=5)
        self.screen.blit(button_text, button_rect)
    
    # Creamos el texto para volver al menú
    def draw_return_text(self):
        SCREEN_WIDTH = 900
        SCREEN_HEIGHT = 600
        COLOR_BLACK = (0, 0, 0)
        COLOR_PURPLE = (170, 0, 255)
        
        button_font = pygame.font.Font("games/BlockAttack/assets/fonts/Neon.ttf", 50)
        button_text = button_font.render("ESC volver al menu", True, COLOR_PURPLE)
        button_rect = button_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
        pygame.draw.rect(self.screen, COLOR_BLACK, button_rect)
        self.screen.blit(button_text, button_rect)
    
    def __init__(self, screen):
        
        # Detener la música de la pantalla de introducción
        pygame.mixer.music.stop()
        
        # Cargamos los archivos de sonido
        sound = pygame.mixer.Sound("games/BlockAttack/assets/sounds/shoot.wav")
        
        # Definimos los colores que vamos a utilizar en RGB
        COLOR_BLACK = (0, 0, 0)
        COLOR_PURPLE = (170, 0, 255)
        NEON_GREEN = (57, 255, 20)
        COLOR_WHITE = (255, 255, 255)       

        # Definimos la pantalla del juego
        SCREEN_WIDTH = 900
        SCREEN_HEIGHT = 600
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Block Attack")                   

        # Creamos las opciones del menú
        font = pygame.font.Font("games/BlockAttack/assets/fonts/Neon.ttf", 50)
        menu_options = ["Nueva Partida", "Controles"]
        option_y = SCREEN_HEIGHT // 2 - len(menu_options) * 50
        self.option_rects = []
        for option in menu_options:
            text = font.render(option, True, NEON_GREEN)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, option_y))
            option_y += 100
            self.option_rects.append(text_rect)
        
        # Creamos una superficie para el texto y una máscara para los bordes iluminados
        self.intro_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.intro_surf.fill(COLOR_BLACK)

        # Crear lluvia de neón
        rain = []
        for i in range(100):
            x = random.randrange(SCREEN_WIDTH)
            y = random.randrange(SCREEN_HEIGHT)
            rain.append([x, y])
        
        # Agregamos la variable highlighted_option_index para resaltar la opción seleccionada
        self.highlighted_option_index = 0
        
        # Atributo para los controles
        self.show_controls = False
        
        # Bucle principal del menú
        running = True
        clock = pygame.time.Clock()
        while running:
            # Manejo de eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False
                    from NostalgiaZone import main_menu
                    main_menu()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.highlighted_option_index = (self.highlighted_option_index - 1) % len(menu_options)
                    elif event.key == pygame.K_DOWN:
                        self.highlighted_option_index = (self.highlighted_option_index + 1) % len(menu_options)
                    elif event.key == pygame.K_RETURN:
                        if menu_options[self.highlighted_option_index] == "Nueva Partida":
                            sound.play()
                            # Iniciamos el juego
                            Game(self.screen)
                        elif menu_options[self.highlighted_option_index] == "Controles":
                            sound.play()
                            self.show_controls = True  
                         
            # Dibujamos el fondo del menú
            self.screen.blit(self.intro_surf, (0, 0))
            
            if self.show_controls:
                # Dibujamos los controles
                self.draw_controls()
                clock.tick(60)
                
                # Manejo de eventos
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        sound.play()
                        self.show_controls = False
                        
            # Dibujar lluvia de neón
                for drop in rain:
                    pygame.draw.line(self.screen, COLOR_PURPLE, [drop[0], drop[1]], [drop[0]+1, drop[1]+1], 1)
                    drop[1] += 1
                    if drop[1] > SCREEN_HEIGHT:
                        drop[1] = random.randrange(-50, -10)
                        drop[0] = random.randrange(SCREEN_WIDTH)
                     
            elif not self.show_controls:
                # Dibujamos el fondo del menú
                self.screen.blit(self.intro_surf, (0, 0))
                
                # Dibujamos las opciones del menú 
                # y resaltamos la opción seleccionada
                for i, rect in enumerate(self.option_rects):
                    highlighted = (i == self.highlighted_option_index)
                    if highlighted:
                        pygame.draw.rect(self.screen, COLOR_PURPLE, rect, 3, border_radius=5)
                    else:
                        pygame.draw.rect(self.screen, COLOR_PURPLE, rect, 3, border_radius=5)
                    text_color = NEON_GREEN if highlighted else COLOR_WHITE
                    text = font.render(menu_options[i], True, text_color)
                    self.screen.blit(text, text.get_rect(center=rect.center))
                    
                # Dibujamos el texto para volver al menú principal
                self.draw_return_text()
                
                # Dibujar lluvia de neón
                for drop in rain:
                    pygame.draw.line(self.screen, COLOR_PURPLE, [drop[0], drop[1]], [drop[0]+1, drop[1]+1], 1)
                    drop[1] += 1
                    if drop[1] > SCREEN_HEIGHT:
                        drop[1] = random.randrange(-50, -10)
                        drop[0] = random.randrange(SCREEN_WIDTH)
                clock.tick(60)
                    
            # Actualizamos la pantalla
            pygame.display.flip()