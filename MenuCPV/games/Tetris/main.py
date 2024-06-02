import pygame, sys
from button import Button
 
pygame.init()

screen = pygame.display.set_mode((900, 600))
pygame.display.set_caption("Tetris")
icon = pygame.image.load("games/Tetris/assets/images/CPV.png")
pygame.display.set_icon(icon)

background = pygame.image.load("games/Tetris/assets/background/fondoTetris.jpg")

def getFont(size):
    return pygame.font.Font("games/Tetris/assets/fonts/Arcade.ttf", 50)
    
def playGame():
    from games.Tetris.tetrisGame import main
    mousePos = pygame.mouse.get_pos()
    btnBack = Button(image=None, pos=(800, 560), 
                            text_input="Volver", font=getFont(50), base_color="white", hovering_color="Blue")
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btnBack.checkForInput(mousePos):
                    mainMenu()

    pygame.display.update()

def controls():
    while True:
        
        mousePos = pygame.mouse.get_pos()

        screen.fill("black")
        background = pygame.image.load("games/Tetris/assets/images/fondoControles.png")
        screen.blit(background, (0, 0))
        
        btnBack = Button(image=None, pos=(800, 560), 
                            text_input="Volver", font=getFont(50), base_color="white", hovering_color="Blue")

        btnBack.changeColor(mousePos)
        btnBack.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btnBack.checkForInput(mousePos):
                    mainMenu()

        pygame.display.update()

def mainMenu():
    while True:
        screen.blit(background, (0, 0))

        mousePos = pygame.mouse.get_pos()
        
        btnTitle = Button(image=pygame.image.load("games/Tetris/assets/images/tetrisLogo1.png"), pos=(450, 120), 
                            text_input="", font=getFont(75), base_color="#d7fcd4", hovering_color="White")
        btnPlay = Button(image=pygame.image.load("games/Tetris/assets/images/btnPlay.png"), pos=(250, 380), 
                            text_input="", font=getFont(75), base_color="#d7fcd4", hovering_color="White")
        btnControls = Button(image=pygame.image.load("games/Tetris/assets/images/btnControls.png"), pos=(650, 380), 
                            text_input="", font=getFont(75), base_color="#d7fcd4", hovering_color="White") 

        for button in [btnPlay, btnControls, btnTitle]:
            button.changeColor(mousePos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btnPlay.checkForInput(mousePos):
                    playGame()
                if btnControls.checkForInput(mousePos):
                    controls()

        pygame.display.update()

mainMenu()