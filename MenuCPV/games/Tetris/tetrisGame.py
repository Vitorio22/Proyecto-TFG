import json
import sys
import pygame  
import random

import requests
from games.Tetris.main import getFont
from button import Button 

# Configuraciones de imagen y sonido
pygame.display.set_caption("Tetris")
icon = pygame.image.load("games/Tetris/assets/images/CPV.png")
flip_sound = pygame.mixer.Sound("games/Tetris/assets/sounds/flip.wav")
pygame.mixer.music.load("games/Tetris/assets/sounds/Tetris.mp3")
pygame.mixer.music.set_volume(0.2)

pygame.display.set_icon(icon)
pygame.font.init()

screenWidth = 900
screenHeight = 850
gameWidth = 300  
gameHeight = 600  
blockSize = 30
 
top_left_x = (screenWidth - gameWidth) // 2
top_left_y = screenHeight - gameHeight - 100
 
# Formas de las piezas del tetris
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]
 
Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]
 
I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]
 
O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]
 
J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]
 
L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]
 
T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

# Formas de las figuras
shapes = [S, Z, I, O, J, L, T]
# Colores de las figuras del tetris
shape_colors = [(87, 35, 100), (255, 160, 122), (0, 255, 255), (128, 0, 128), (255, 165, 0), (0, 128, 128), (255, 255, 0)]

screen = pygame.display.set_mode((screenWidth, screenHeight))
scoreText = 0

def show_message_centered(message):
		# Tamaño de la pantalla
		SCREEN_WIDTH = 800
		SCREEN_HEIGHT = 600
		# Colores
		FONDO_COLOR = (29, 62, 90)
		COLOR_PURPLE = (170, 0, 255)

		message_font = pygame.font.Font("games/Tetris/assets/fonts/Arcade.ttf", 40)
		message_surf = message_font.render(message, True, COLOR_PURPLE)
		message_rect = message_surf.get_rect(center=(SCREEN_WIDTH // 1.8, SCREEN_HEIGHT // 1.8))

		screen.fill(FONDO_COLOR)
		screen.blit(message_surf, message_rect)
		pygame.display.flip()
		pygame.time.delay(2000)

# Esta funcion define la ventana para introducir el nombre del jugador y guardar la puntuación
def save_score():
    # Tamaño de la pantalla
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 800
    # Colores
    COLOR_BLACK = (0, 0, 0)
    COLOR_PURPLE = (170, 0, 255)
    COLOR_BLUE = (0, 0, 255)
    
    player_name = ""
    score = scoreText
    input_active = True
    
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if player_name != "":
                    input_active = False
                    send_score(player_name, score)
                else:
                    show_message_centered("Debes introducir un nombre")
            
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                player_name = player_name[:-1]
            elif event.type == pygame.KEYDOWN:
                player_name += event.unicode
        control_text = [
            "Puntuacion: " + str(scoreText),
            "Introduce tu nombre: " + player_name,
        ]
        control_font = pygame.font.Font("games/Tetris/assets/fonts/Arcade.ttf", 40)
        control_surf = pygame.Surface((SCREEN_WIDTH // 2 + 100, SCREEN_HEIGHT // 2))
        control_surf.fill(COLOR_BLACK)
        for i, text in enumerate(control_text):
            control_render = control_font.render(text, True, COLOR_BLUE)
            control_rect = control_render.get_rect(center=(SCREEN_WIDTH // 4 + 50, (SCREEN_HEIGHT // 4 - 50) + (i * 50)))
            control_surf.blit(control_render, control_rect)
        screen.blit(control_surf, control_surf.get_rect(center=(SCREEN_WIDTH // 2.5, SCREEN_HEIGHT // 2)))
        pygame.draw.rect(screen, COLOR_PURPLE, control_surf.get_rect(center=(SCREEN_WIDTH // 2.5, SCREEN_HEIGHT // 2)), 3, border_radius=5)
        # Dibujar mensaje de pulsar enter
        button_font = pygame.font.Font("games/Tetris/assets/fonts/Arcade.ttf", 50)
        button_text = button_font.render("Pulsa Enter", True, COLOR_BLUE)
        button_rect = button_text.get_rect(center=(SCREEN_WIDTH // 2.5, SCREEN_HEIGHT - 100))
        pygame.draw.rect(screen, COLOR_BLACK, button_rect)
        pygame.draw.rect(screen, COLOR_PURPLE, button_rect, 3, border_radius=5)
        screen.blit(button_text, button_rect)
        pygame.display.flip()
    
    return player_name, score

# Esta funcion envia la puntuación al servidor    
def send_score(player_name, score):
    # URL del endpoint para guardar la puntuación
    url = "http://localhost:5000/save_score_tetris"
    
    headers = {"Content-Type": "application/json"}
    data = json.dumps({"nombre": player_name, "puntuacion": score})
    
    response = requests.post(url, headers=headers, data=data)
    
    if response.status_code == 200:
        print("Puntuación guardada exitosamente")
    else:
        print("Error al guardar la puntuación")
    
class Piece(object):
    rows = 20  # Coordenada y
    columns = 10  # Coordenada x
 
    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0 
 
# Creación del grid del juego
def createGrid(locked_positions={}):
    grid = [[(0,0,0) for x in range(10)] for x in range(20)]
 
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j,i) in locked_positions:
                c = locked_positions[(j,i)]
                grid[i][j] = c
    return grid

# Función para convertir la forma de la pieza en coordenadas
def convertShape(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]
 
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))
 
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)
 
    return positions

# Función para verificar si la posición es válida
def putSpace(shape, grid):
    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = convertShape(shape)
 
    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
 
    return True

# Función para verificar si la pieza está en el límite del grid
def checkLost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False
 
# Función para obtener una pieza aleatoria
def getShape():
    global shapes, shape_colors
    return Piece(5, 0, random.choice(shapes))

# Función para dibujar el texto en pantalla
def positionMiddleText(text, color, size, surface):
    font = getFont(size)
    label = font.render(text, 1, (255,255,255,255))
 
    surface.blit(label, (top_left_x + gameWidth/2 - (label.get_width() / 2), top_left_y + gameHeight/1.30 - label.get_height()/2))

# Función para dibujar el grid del juego
def drawGrid(surface, row, col):
    sx = top_left_x
    sy = top_left_y
    for i in range(row):
        pygame.draw.line(surface, (128,128,128), (sx, sy+ i*30), (sx + gameWidth, sy + i * 30))  # horizontal lines
        for j in range(col):
            pygame.draw.line(surface, (128,128,128), (sx + j * 30, sy), (sx + j * 30, sy + gameHeight))  # vertical lines

# Funcion para eliminar las filas completas del grid y añadir la puntuación al marcador
def deleteRow(grid, locked):
    # Elimina las filas cuando están completas. Añado la puntuación
    inc = 0
    global scoreText
    
    for i in range(len(grid)-1,-1,-1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            ind = i
            scoreText += 50
            
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)
 
# Muestra la siguiente figura que va a aparecer en el grid
def showNextShapes(shape, surface):
    font = pygame.font.Font('games/Tetris/assets/fonts/Arcade.ttf', 35)
    label = font.render('Siguiente forma', 1, (255, 255, 255, 255))
    
    sx = top_left_x + gameWidth + 50
    sy = top_left_y + gameHeight/2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]
 
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*30, sy + i*30, 30, 30), 0)
 
    surface.blit(label, (sx + 10, sy- 30))
 
# Delimita el grid y establece un fondo 
def putTitle(surface):
    background = pygame.image.load("games/Tetris/assets/background/fondoTetris1.jpg").convert()
    surface.blit(background, (top_left_x + gameWidth / 2 - (background.get_width() / 2), 30))
    
    # Dibuja las figuras en el grid
    for i in range(len(grid)):
        for j in range(len(grid[i])): 
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j* 30, top_left_y + i * 30, 30, 30), 0)
 
    score_text = getFont(30).render("Puntuacion: " + str(scoreText), True, (255, 255, 255))
    screen.blit(score_text, (30, 30))

    # Demilita el grid
    drawGrid(surface, 20, 10)
    pygame.draw.rect(surface, (0,0,0,0), (top_left_x, top_left_y, gameWidth, gameHeight), 5) 

# Funcion principal del juego
def main():
    global grid
 
    locked_positions = {}
    grid = createGrid(locked_positions)
 
    change_piece = False
    run = True
    current_piece = getShape()
    next_piece = getShape()
    clock = pygame.time.Clock()
    fall_time = 0
    # Bucle principal del juego   
    while run:
        fall_speed = 0.27
        grid = createGrid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()
 
        # Mueve la pieza hacia abajo
        if fall_time/1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (putSpace(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()
            # Eventos de teclado para mover las figuras
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not putSpace(current_piece, grid):
                        current_piece.x += 1
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not putSpace(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_UP:
                    flip_sound.play()
                    current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                    if not putSpace(current_piece, grid):
                        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)
 
                if event.key == pygame.K_DOWN:
                    # Método para que con el espacio la figura baje al final del grid
                    current_piece.y += 1
                    if not putSpace(current_piece, grid):
                        current_piece.y -= 1
                
                if event.key == pygame.K_SPACE:
                   while putSpace(current_piece, grid):
                       current_piece.y += 1
                   current_piece.y -= 1
                   # print(convertShape(current_piece))
 
        shape_pos = convertShape(current_piece)
 
        # Añade la figura al grid para que se quede fija cuando llegue al final
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = getShape()
            change_piece = False
 
            deleteRow(grid, locked_positions)
 
        putTitle(screen)
        showNextShapes(next_piece, screen)
        pygame.display.update()

        if checkLost(locked_positions):
            run = False
 
    positionMiddleText("Has perdido", 40, (128, 0, 128), screen)
    pygame.display.flip()
    pygame.time.delay(2000)
    screen.fill((0,0,0))
    pygame.mixer.music.stop()
    save_score()
    from NostalgiaZone import main_menu
    main_menu()
# Muestra el menu del juego    
def gameMenu():
    screen = pygame.display.set_mode((900, 850))
    background = pygame.image.load("games/Tetris/assets/background/fondoTetris1.jpg")
    run = True
    while run:
        screen.blit(background, (0, 0))
        positionMiddleText("Presiona cualquier tecla", 60, (255, 160, 122), surface=screen)
        drawGrid
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                pygame.mixer.music.play(-1)
                main() 
    pygame.quit()
 
gameMenu()