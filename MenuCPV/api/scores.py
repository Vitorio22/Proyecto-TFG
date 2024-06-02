import pygame, sys, requests
from button import Button

SCREEN = pygame.display.set_mode((900, 600))

# Función para obtener la fuente
def get_font(size): 
    return pygame.font.Font("assets/fonts/Arcade.ttf", size)

# Función para recuperar y mostrar las puntuaciones de Asteroids
def get_score_asteroids():
    
        btnTitle = Button(image=pygame.image.load("assets/images/titleAsteroidsScore.png"), pos=(450, 150), 
                                text_input="", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        # Redimensionar la imagen del título
        btnTitle.image = pygame.transform.scale(btnTitle.image, (700, 200))
        
        SCORE_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill("black")
        
        for button in [btnTitle]:
            button.changeColor(SCORE_MOUSE_POS)
            button.update(SCREEN)
        
        btnBack = Button(image=None, pos=(800, 560), 
                            text_input="Volver", font=get_font(50), base_color="white", hovering_color="Blue")

        btnBack.changeColor(SCORE_MOUSE_POS)
        btnBack.update(SCREEN)
        
        # Obtenemos las puntuaciones de Block Attack
        r = requests.get("http://localhost:5000/get_score_asteroids")
        response = r.json()
        scores = response['scores']
        
        # Crear la imagen de la tabla con bordes verdes
        table_width = 400
        table_height = len(scores) * 30 + 60  # Altura de la tabla basada en la cantidad de puntuaciones
        table_surface = pygame.Surface((table_width, table_height))
        table_surface.fill("black")
        
        # Mostramos las etiquetas de la columna
        text = get_font(30).render("Nombre", True, "white")
        table_surface.blit(text, (30, 0))
        text = get_font(30).render("Puntuacion", True, "white")
        table_surface.blit(text, (table_width - 150, 0))
        
        # Dibujar la linea verde para dividir la tabla horizontalmente
        pygame.draw.line(table_surface, (255, 255, 255), (0, 30), (table_width, 30), 2)
        
        # Dibujar la linea verde para dividir la tabla verticalmente
        pygame.draw.line(table_surface, (255, 255, 255), (table_width - 150, 0), (table_width - 150, table_height), 2)

        # Dibujar los bordes verdes de la tabla
        pygame.draw.rect(table_surface, (255, 255, 255), (0, 0, table_width, table_height), 2)

        # Mostrar las puntuaciones en la tabla
        for i, score in enumerate(scores):
            name = score['Nombre']
            score_value = score['Puntuacion']
            text = get_font(30).render(f"{i+1}. {name}", True, "white")
            table_surface.blit(text, (30, 30 + i * 30))
            score_text = get_font(30).render(str(score_value), True, "white")
            table_surface.blit(score_text, (table_width - 100, 30 + i * 30))

        # Calcular la posición para centrar la tabla en la pantalla
        table_x = (SCREEN.get_width() - table_width) // 2
        table_y = (SCREEN.get_height() - table_height) // 2

        # Mostrar la tabla en la pantalla
        SCREEN.blit(table_surface, (table_x, table_y))

        while True:
            SCORE_MOUSE_POS = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if btnBack.checkForInput(SCORE_MOUSE_POS):
                        return
                    
            btnBack.changeColor(SCORE_MOUSE_POS)
            btnBack.update(SCREEN)
            
            pygame.display.update()

# Función para recuperar y mostrar las puntuaciones de Block Attack
def get_score_blockAttack():
    
        btnTitle = Button(image=pygame.image.load("assets/images/titleBlockAttackScore.png"), pos=(450, 150), 
                                text_input="", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        # Redimensionar la imagen del título
        btnTitle.image = pygame.transform.scale(btnTitle.image, (700, 200))
        
        SCORE_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill("black")
        
        for button in [btnTitle]:
            button.changeColor(SCORE_MOUSE_POS)
            button.update(SCREEN)
        
        btnBack = Button(image=None, pos=(800, 560), 
                            text_input="Volver", font=get_font(50), base_color="white", hovering_color="Blue")

        btnBack.changeColor(SCORE_MOUSE_POS)
        btnBack.update(SCREEN)
        
        # Obtenemos las puntuaciones de Block Attack
        r = requests.get("http://localhost:5000/get_score_blockAttack")
        response = r.json()
        scores = response['scores']
        
        # Crear la imagen de la tabla con bordes verdes
        table_width = 400
        table_height = len(scores) * 30 + 60  # Altura de la tabla basada en la cantidad de puntuaciones
        table_surface = pygame.Surface((table_width, table_height))
        table_surface.fill("black")
        
        # Mostramos las etiquetas de la columna
        text = get_font(30).render("Nombre", True, "white")
        table_surface.blit(text, (30, 0))
        text = get_font(30).render("Puntuacion", True, "white")
        table_surface.blit(text, (table_width - 150, 0))
        
        # Dibujar la linea verde para dividir la tabla horizontalmente
        pygame.draw.line(table_surface, (0, 255, 0), (0, 30), (table_width, 30), 2)
        
        # Dibujar la linea verde para dividir la tabla verticalmente
        pygame.draw.line(table_surface, (0, 255, 0), (table_width - 150, 0), (table_width - 150, table_height), 2)

        # Dibujar los bordes verdes de la tabla
        pygame.draw.rect(table_surface, (0, 255, 0), (0, 0, table_width, table_height), 2)

        # Mostrar las puntuaciones en la tabla
        for i, score in enumerate(scores):
            name = score['Nombre']
            score_value = score['Puntuacion']
            text = get_font(30).render(f"{i+1}. {name}", True, "white")
            table_surface.blit(text, (30, 30 + i * 30))
            score_text = get_font(30).render(str(score_value), True, "white")
            table_surface.blit(score_text, (table_width - 100, 30 + i * 30))

        # Calcular la posición para centrar la tabla en la pantalla
        table_x = (SCREEN.get_width() - table_width) // 2
        table_y = (SCREEN.get_height() - table_height) // 2

        # Mostrar la tabla en la pantalla
        SCREEN.blit(table_surface, (table_x, table_y))

        while True:
            SCORE_MOUSE_POS = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if btnBack.checkForInput(SCORE_MOUSE_POS):
                        return
                    
            btnBack.changeColor(SCORE_MOUSE_POS)
            btnBack.update(SCREEN)
            
            pygame.display.update()

def get_score_tetris():
    
        btnTitle = Button(image=pygame.image.load("assets/images/titleTetrisScore.png"), pos=(450, 150), 
                                text_input="", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        # Redimensionar la imagen del título
        btnTitle.image = pygame.transform.scale(btnTitle.image, (700, 200))
        
        SCORE_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill("black")
        COLOR_PINK = (255, 0, 255)
        
        for button in [btnTitle]:
            button.changeColor(SCORE_MOUSE_POS)
            button.update(SCREEN)
        
        btnBack = Button(image=None, pos=(800, 560), 
                            text_input="Volver", font=get_font(50), base_color="white", hovering_color="Blue")

        btnBack.changeColor(SCORE_MOUSE_POS)
        btnBack.update(SCREEN)
        
        # Obtenemos las puntuaciones de Block Attack
        r = requests.get("http://localhost:5000/get_score_tetris")
        response = r.json()
        scores = response['scores']
        
        # Crear la imagen de la tabla con bordes verdes
        table_width = 400
        table_height = len(scores) * 30 + 60  # Altura de la tabla basada en la cantidad de puntuaciones
        table_surface = pygame.Surface((table_width, table_height))
        table_surface.fill("black")
        
        # Mostramos las etiquetas de la columna
        text = get_font(30).render("Nombre", True, "white")
        table_surface.blit(text, (30, 0))
        text = get_font(30).render("Puntuacion", True, "white")
        table_surface.blit(text, (table_width - 150, 0))
        
        # Dibujar la linea verde para dividir la tabla horizontalmente
        pygame.draw.line(table_surface, (COLOR_PINK), (0, 30), (table_width, 30), 2)
        
        # Dibujar la linea verde para dividir la tabla verticalmente
        pygame.draw.line(table_surface, (COLOR_PINK), (table_width - 150, 0), (table_width - 150, table_height), 2)

        # Dibujar los bordes verdes de la tabla
        pygame.draw.rect(table_surface, (COLOR_PINK), (0, 0, table_width, table_height), 2)

        # Mostrar las puntuaciones en la tabla
        for i, score in enumerate(scores):
            name = score['Nombre']
            score_value = score['Puntuacion']
            text = get_font(30).render(f"{i+1}. {name}", True, "white")
            table_surface.blit(text, (30, 30 + i * 30))
            score_text = get_font(30).render(str(score_value), True, "white")
            table_surface.blit(score_text, (table_width - 100, 30 + i * 30))

        # Calcular la posición para centrar la tabla en la pantalla
        table_x = (SCREEN.get_width() - table_width) // 2
        table_y = (SCREEN.get_height() - table_height) // 2

        # Mostrar la tabla en la pantalla
        SCREEN.blit(table_surface, (table_x, table_y))

        while True:
            SCORE_MOUSE_POS = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if btnBack.checkForInput(SCORE_MOUSE_POS):
                        return
                    
            btnBack.changeColor(SCORE_MOUSE_POS)
            btnBack.update(SCREEN)
            
            pygame.display.update()
