import pygame, random
from games.BlockAttack.screens.menu import MainMenu

class Intro:
    def __init__(self, screen):
        
        # Cargamos los archivos de sonido
        pygame.mixer.music.load("games/BlockAttack/assets/sounds/intro.wav")
        sound = pygame.mixer.Sound("games/BlockAttack/assets/sounds/shoot.wav")
        
        # Reproducimos la musica de fondo
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.1)
        
        # Definimos los colores que vamos a utilizar en RGB
        COLOR_BLACK = (0, 0, 0)
        COLOR_PURPLE = (170, 0, 255)
        NEON_GREEN = (57, 255, 20)
        COLOR_GRAY = (128, 128, 128)           

        # Definimos la pantalla del juego
        SCREEN_WIDTH = 900
        SCREEN_HEIGHT = 600
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Block Attack")                   

        # Creamos el texto y le aplicamos los colores y efectos necesarios
        font = pygame.font.Font("games/BlockAttack/assets/fonts/DRIVE-TH.TTF", 64)
        self.text = font.render("BL0CK ATT4CK", True, NEON_GREEN)

        # Creamos una superficie para el texto y una máscara para los bordes iluminados
        self.text_surf = pygame.Surface((self.text.get_width() + 6, self.text.get_height() + 6), pygame.SRCALPHA)
        mask_surf = pygame.Surface(self.text.get_size(), pygame.SRCALPHA)
        buildings_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        buildings_surf.set_colorkey(COLOR_BLACK)           

        # Dibujamos la máscara de los bordes iluminados
        pygame.draw.rect(mask_surf, NEON_GREEN, (3, 3, *self.text.get_size()), border_radius=3)
        pygame.draw.rect(mask_surf, COLOR_PURPLE, (6, 6, *self.text.get_size()), border_radius=3)
        mask_surf.blit(self.text, (0, 0))           

        # Dibujamos la superficie del texto con el color morado estilo neon
        self.text_surf.blit(mask_surf, (3, 3))
        self.text_surf.blit(mask_surf, (0, 0))
        self.text_surf.blit(mask_surf, (6, 6))          

        # Establecemos la posición inicial y la velocidad del título
        x_pos = 100
        y_pos = 100
        x_speed = 3
        y_speed = 3        

        # Crear lluvia de neón
        self.rain = []
        for i in range(100):
            x = random.randrange(SCREEN_WIDTH)
            y = random.randrange(SCREEN_HEIGHT)
            self.rain.append([x, y])
            
        # Creamos una lista para almacenar los edificios
        buildings = []         

        # Definimos la altura y la anchura de los edificios
        building_width = 80
        building_height = 400          

        # Generamos los edificios y los agregamos a la lista
        for i in range(14):
            # Generamos la altura aleatoria del edificio
            height = random.randint(200, building_height)
            
            # Creamos la superficie del edificio con un color aleatorio
            building_surf = pygame.Surface((building_width, height), pygame.SRCALPHA)
            
            # Agregamos ventanas al edificio
            window_size = 8
            window_spacing = 10
            num_windows_x = int((building_width - window_spacing) / (window_size + window_spacing))
            num_windows_y = int((height - window_spacing) / (window_size + window_spacing))
            
            for x in range(num_windows_x):
                for y in range(num_windows_y):
                    window_x = x * (window_size + window_spacing) + window_spacing
                    window_y = y * (window_size + window_spacing) + window_spacing
                    window_color = (random.randint(80, 200), random.randint(80, 200), random.randint(80, 200))
                    pygame.draw.rect(building_surf, window_color, (window_x, window_y, window_size, window_size), 1)
            
            # Dibujamos el relieve del edificio
            pygame.draw.rect(building_surf, COLOR_PURPLE, (0, 0, building_width, height), 3)
            pygame.draw.line(building_surf, COLOR_PURPLE, (3, height-3), (3, 3), 3)
            pygame.draw.line(building_surf, COLOR_PURPLE, (3, 3), (building_width-3, 3), 3)
            pygame.draw.line(building_surf, COLOR_PURPLE, (building_width-3, 3), (building_width-3, height-3), 3)
            pygame.draw.line(building_surf, COLOR_GRAY, (6, height-6), (6, 6), 2)
            pygame.draw.line(building_surf, COLOR_GRAY, (6, 6), (building_width-6, 6), 2)
            pygame.draw.line(building_surf, COLOR_GRAY, (building_width-6, 6), (building_width-6, height-6), 2)
            
            # Agregamos el edificio a la lista de edificios
            x = i * (building_width + 10) + random.randint(0, 10)
            y = SCREEN_HEIGHT - height
            buildings.append([building_surf, (x, y)])
            
        # Bucle principal de la introducción
        running = True
        clock = pygame.time.Clock()
        while running:
            
            
            # Manejo de eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.mixer.music.stop()
                    from nostalgiaZone import main_menu
                    main_menu()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    sound.play().set_volume(0.2)
                    pygame.mixer.music.stop()
                    # Navegamos a la pantalla de menú
                    MainMenu(self.screen)
                 
            # Movimiento del título
            x_pos += x_speed
            y_pos += y_speed

            # Rebotar el título en los bordes de la pantalla
            if x_pos > SCREEN_WIDTH - self.text_surf.get_width() or x_pos < 0:
                x_speed = -x_speed
            if y_pos > SCREEN_HEIGHT - self.text_surf.get_height() or y_pos < 0:
                y_speed = -y_speed

            # Dibujamos el fondo y los edificios
            screen.fill(COLOR_BLACK)
            for building in buildings:
                screen.blit(*building)

            # Dibujar lluvia de neón
            for drop in self.rain:
                pygame.draw.line(screen, COLOR_PURPLE, [drop[0], drop[1]], [drop[0]+1, drop[1]+1], 1)
                drop[1] += 1
                if drop[1] > SCREEN_HEIGHT:
                    drop[1] = random.randrange(-50, -10)
                    drop[0] = random.randrange(SCREEN_WIDTH)

            # Dibujamos el título
            screen.blit(self.text_surf, (x_pos, y_pos))

            # Actualizamos la pantalla
            pygame.display.flip()
            clock.tick(60)