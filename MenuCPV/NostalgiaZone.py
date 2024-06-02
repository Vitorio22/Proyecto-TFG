import pygame, sys, requests, threading
from button import Button
from api.routes import app

# Inicializamos pygame
pygame.init()
pygame.mixer.init()

# Configuramos la música del menú

# Función para iniciar el servidor de Flask en un hilo aparte
def run_flask_server():
    app.run(debug=False, use_reloader=False)

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask_server)
    flask_thread.daemon = True
    flask_thread.start()

# Cargamos las imagenes de logo y fondo
SCREEN = pygame.display.set_mode((900, 600))
pygame.display.set_caption("CPV")
icon = pygame.image.load("assets/images/CPV.png")
pygame.display.set_icon(icon)
BG = pygame.image.load("assets/images/fondo.png")

# Función para obtener la fuente
def get_font(size): 
    return pygame.font.Font("assets/fonts/Arcade.ttf", size)

# Función para la pantalla de puntuaciones
def score_menu():
    while True:
        btnTitle = Button(image=pygame.image.load("assets/images/titleScore.png"), pos=(450, 100), 
                            text_input="", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        btnBlockAttack = Button(image=pygame.image.load("assets/images/blockAttackScore.png"), pos=(260, 270), 
                                text_input="", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        btnAsteroids = Button(image=pygame.image.load("assets/images/asteroidsScore.png"), pos=(620, 270), 
                              text_input="", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        btnTetris = Button(image=pygame.image.load("assets/images/tetrisScore.png"), pos=(430, 450), 
                           text_input="", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        SCORE_MOUSE_POS = pygame.mouse.get_pos()
        
        SCREEN.fill("black")
        
        for button in [btnTitle, btnBlockAttack, btnAsteroids, btnTetris]:
            button.changeColor(SCORE_MOUSE_POS)
            button.update(SCREEN)
        
        btnBack = Button(image=None, pos=(800, 560), 
                            text_input="Volver", font=get_font(50), base_color="WHITE", hovering_color="Blue")

        btnBack.changeColor(SCORE_MOUSE_POS)
        btnBack.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btnAsteroids.checkForInput(SCORE_MOUSE_POS):
                    from api.scores import get_score_asteroids
                    get_score_asteroids()
                if btnBlockAttack.checkForInput(SCORE_MOUSE_POS):
                    from api.scores import get_score_blockAttack
                    get_score_blockAttack()
                if btnTetris.checkForInput(SCORE_MOUSE_POS):
                    from api.scores import get_score_tetris
                    get_score_tetris()
                if btnBack.checkForInput(SCORE_MOUSE_POS):
                    main_menu()
                    
        pygame.display.update()
        
def asteroids():
    from games.Asteroids.asteroids import Game
    pygame.display.update()
    game = Game()
    game.run()

def blockAttack():
    from games.BlockAttack.main import Main
    pygame.display.update()
    game = Main()
    game.run()

def tetris():
    from games.Tetris.main import mainMenu
    pygame.display.update()
    game = mainMenu()
    game.run()

# Función para la pantalla de créditos
def credits():
     while True:

        btnTitle = Button(image=pygame.image.load("assets/images/titleCredits.png"), pos=(450, 100), 
                            text_input="", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        SCORE_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")
        background = pygame.image.load("assets/images/credit.png")
        SCREEN.blit(background, (0, 0))
        
        for button in [btnTitle]:
            button.changeColor(SCORE_MOUSE_POS)
            button.update(SCREEN)
        
        btnBack = Button(image=None, pos=(800, 560), 
                            text_input="Volver", font=get_font(50), base_color="white", hovering_color="Blue")

        btnBack.changeColor(SCORE_MOUSE_POS)
        btnBack.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btnBack.checkForInput(SCORE_MOUSE_POS):
                    main_menu()

        pygame.display.update()

# Función para el menú principal
def main_menu():
    pygame.display.set_mode((900, 600))
    pygame.mixer.music.load("assets/sounds/menu.wav")
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1)
    while True:
        SCREEN.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        
        btnTitle = Button(image=pygame.image.load("assets/images/title1.2.png"), pos=(450, 100), 
                          text_input="", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        btnBlockAttack = Button(image=pygame.image.load("assets/images/blockAttack.png"), pos=(160, 260), 
                                text_input="", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        btnAsteroids = Button(image=pygame.image.load("assets/images/asteroids.png"), pos=(480, 260), 
                              text_input="", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        btnTetris = Button(image=pygame.image.load("assets/images/tetris.png"), pos=(770, 260), 
                           text_input="", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        btnScore = Button(image=pygame.image.load("assets/images/score.png"), pos=(620, 440), 
                          text_input="", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        btnCredits = Button(image=pygame.image.load("assets/images/credits.png"), pos=(320, 440), 
                            text_input="", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        for button in [btnBlockAttack, btnAsteroids, btnTetris, btnScore, btnCredits, btnTitle]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btnScore.checkForInput(MENU_MOUSE_POS):
                    score_menu()
                if btnAsteroids.checkForInput(MENU_MOUSE_POS):
                    pygame.mixer.music.stop()
                    asteroids()
                if btnBlockAttack.checkForInput(MENU_MOUSE_POS):
                    pygame.mixer.music.stop()
                    blockAttack()
                if btnTetris.checkForInput(MENU_MOUSE_POS):
                    pygame.mixer.music.stop()
                    tetris()
                if btnCredits.checkForInput(MENU_MOUSE_POS):
                    credits()

        pygame.display.update()

main_menu()