import json
import pygame, sys, requests
from random import randrange as rnd

pygame.init()
pygame.mixer.init()

class Game():
    # Esta funcion define el mensaje de advertencia y su posicion en la pantalla
    def show_message_centered(self, message):
        # Tamaño de la pantalla
        SCREEN_WIDTH = 900
        SCREEN_HEIGHT = 600
        # Colores
        COLOR_BLACK = (0, 0, 0)
        NEON_GREEN = (57, 255, 20)

        message_font = pygame.font.Font("games/BlockAttack/assets/fonts/Neon.ttf", 40)
        message_surf = message_font.render(message, True, NEON_GREEN)
        message_rect = message_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        self.screen.fill(COLOR_BLACK)
        self.screen.blit(message_surf, message_rect)
        pygame.display.flip()
        pygame.time.delay(2000)
    
    # Esta funcion define la ventana para introducir el nombre del jugador y guardar la puntuación
    def save_score(self):
        # Tamaño de la pantalla
        SCREEN_WIDTH = 900
        SCREEN_HEIGHT = 600
        # Colores
        COLOR_BLACK = (0, 0, 0)
        COLOR_PURPLE = (170, 0, 255)
        NEON_GREEN = (57, 255, 20)
        
        player_name = ""
        score = self.score
        input_active = True
        
        while input_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    if player_name != "":
                        input_active = False
                        self.send_score(player_name, score)
                    else:
                        self.show_message_centered("Debes introducir un nombre")
                
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                elif event.type == pygame.KEYDOWN:
                    player_name += event.unicode

            control_text = [
                "Puntuación: " + str(self.score),
                "Introduce tu nombre: " + player_name,
            ]
            control_font = pygame.font.Font("games/BlockAttack/assets/fonts/Neon.ttf", 40)
            control_surf = pygame.Surface((SCREEN_WIDTH // 2 + 100, SCREEN_HEIGHT // 2))
            control_surf.fill(COLOR_BLACK)
            for i, text in enumerate(control_text):
                control_render = control_font.render(text, True, NEON_GREEN)
                control_rect = control_render.get_rect(center=(SCREEN_WIDTH // 4 + 50, (SCREEN_HEIGHT // 4 - 50) + (i * 50)))
                control_surf.blit(control_render, control_rect)
            self.screen.blit(control_surf, control_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
            pygame.draw.rect(self.screen, COLOR_PURPLE, control_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)), 3, border_radius=5)

            # Dibujar mensaje de pulsar enter
            button_font = pygame.font.Font("games/BlockAttack/assets/fonts/Neon.ttf", 50)
            button_text = button_font.render("Pulsa Enter", True, NEON_GREEN)
            button_rect = button_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
            pygame.draw.rect(self.screen, COLOR_BLACK, button_rect)
            pygame.draw.rect(self.screen, COLOR_PURPLE, button_rect, 3, border_radius=5)
            self.screen.blit(button_text, button_rect)

            pygame.display.flip()
        
        return player_name, score
    
    def send_score(self, player_name, score):
        # URL del endpoint para guardar la puntuación
        url = "http://localhost:5000/save_score_blockAttack"
        
        headers = {"Content-Type": "application/json"}
        data = json.dumps({"nombre": player_name, "puntuacion": score})
        
        response = requests.post(url, headers=headers, data=data)
        
        if response.status_code == 200:
            print("Puntuación guardada exitosamente")
        else:
            print("Error al guardar la puntuación")
    
    def __init__(self, screen):
        
        # Defino el tamaño de la pantalla y el número de fotogramas por segundo
        WIDTH, HEIGHT = 900, 600
        GAME_AREA_HEIGHT = HEIGHT - 100
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        fps = 30
        
        # Defino unas variales globales
        self.score = 0
        lives = 3
        brick_hit = 0
        combo_time = 0

        # Configuración de la barra
        paddle_w = 150
        paddle_h = 20
        paddle_speed = 30
        paddle = pygame.Rect(WIDTH // 2 - paddle_w // 2, GAME_AREA_HEIGHT - paddle_h - 10, paddle_w, paddle_h)
        
        # Configuración de la bola
        ball_radius = 15
        ball_speed = 6
        ball_rect = int(ball_radius * 2 ** 0.5)
        ball = pygame.Rect(rnd(ball_rect, WIDTH - ball_rect), GAME_AREA_HEIGHT // 2, ball_rect, ball_rect)
        dx, dy = 1, -1
        
        # Configuración de los bloques
        rows = 8
        columns = 10
        block_width = (WIDTH - (columns + 1) * 10) // columns
        block_height = 25
        block_list = [(pygame.Rect(10 + (block_width + 10) * i, 10 + (block_height + 10) * j, block_width, block_height), 1)
                      for i in range(columns) for j in range(rows)]
        color_list = [pygame.Color(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for _ in block_list]
        sc = pygame.display.set_mode((WIDTH, HEIGHT))
        clock = pygame.time.Clock()
       
        # Cargo los sonidos
        sound_bounce = pygame.mixer.Sound('games/BlockAttack/assets/sounds/pong.wav')
        sound_bounce.set_volume(0.2)
        sound_block_hit = pygame.mixer.Sound('games/BlockAttack/assets/sounds/punch4.wav')
        sound_block_hit.set_volume(0.2)
        sound_game_over = pygame.mixer.Sound('games/BlockAttack/assets/sounds/fail.wav')
        sound_win = pygame.mixer.Sound('games/BlockAttack/assets/sounds/nextlvl.wav')
        
        # Configuración de la música
        pygame.mixer.music.load('games/BlockAttack/assets/sounds/music_game.wav')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.2)
        
        # Imagen de fondo
        img = pygame.image.load('games/BlockAttack/assets/background/1.jpg').convert()
        
        # Configuración de la puntuación y las vidas
        score_font = pygame.font.Font('games/BlockAttack/assets/fonts/Neon.ttf', 36)
        score_area = pygame.Rect(0, GAME_AREA_HEIGHT, WIDTH, HEIGHT - GAME_AREA_HEIGHT)
        combo_area = pygame.Rect(-400, GAME_AREA_HEIGHT, WIDTH, HEIGHT - GAME_AREA_HEIGHT)
        heart = pygame.image.load('games/BlockAttack/assets/img/heart_1.png').convert_alpha()
        heart = pygame.transform.scale(heart, (170, 100))
        heart_rect = heart.get_rect()
        
        # Esta función detecta las colisiones entre la pelota y los bloques
        def detect_collision(dx, dy, ball, rect):
            if rect.colliderect(ball):
                # Determinar la posición relativa del impacto
                diff_x = ball.centerx - rect.centerx
                diff_y = ball.centery - rect.centery

                # Determina la dirección de rebote en función de la posición relativa del bloque
                if abs(diff_x) > abs(diff_y):
                    dx = -dx  # Cambia la dirección horizontal
                else:
                    dy = -dy  # Cambia la dirección vertical

            return dx, dy

        # Bucle principal del juego
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                    
            # Dibujo la imagen de fondo        
            sc.blit(img, (0, 0))
            
            # Dibujo la puntuación y las vidas
            score_text = score_font.render(f'SCORE: {self.score}', True, pygame.Color('red'))
            score_text_rect = score_text.get_rect(center=score_area.center)
            sc.blit(score_text, score_text_rect)
            for i in range(lives):
                heart_rect.center = (WIDTH - 60 * (i + 1), GAME_AREA_HEIGHT + 50)
                sc.blit(heart, heart_rect)
            
            # Dibujo los bloques
            for i, (rect, _) in enumerate(block_list):
                pygame.draw.rect(sc, color_list[i], rect)
                    
            # Dibujo la barra y la bola       
            pygame.draw.rect(sc, pygame.Color('darkorange'), paddle)
            pygame.draw.circle(sc, pygame.Color('white'), ball.center, ball_radius)
            
            # Incrementar la velocidad de la bola cada 1000 puntos
            if self.score % 1000 == 0 and self.score != 0:
                ball_speed += 0.1

            # Movimiento de la bola
            ball.x += ball_speed * dx
            ball.y += ball_speed * dy
            
            # Comprobación de colisiones
            if ball.left < ball_radius or ball.right > WIDTH - ball_radius:
                dx = -dx
            
            # Comprobación de colision con el techo
            if ball.top < ball_radius:
                dy = -dy
                
            # Comprobación de colision con la barra
            if ball.colliderect(paddle) and dy > 0:
                # Calcula la posición relativa de impacto
                relative_position = ball.centerx - paddle.centerx
                # Ajusta la dirección horizontal de la bola según la posición relativa de impacto
                dx = round(7 * relative_position / paddle_w)
                dy = -dy
                sound_bounce.play()
                    
            # Comprobación de colision con los bloques
            hit_index = ball.collidelist([rect for rect, _ in block_list])
            if hit_index != -1:
                hit_rect = block_list.pop(hit_index)[0]
                hit_color = color_list.pop(hit_index)
                dx, dy = detect_collision(dx, dy, ball, hit_rect)
                
                # Efecto de explosión al romper un bloque
                hit_rect.inflate_ip(ball.width * 3, ball.height * 3)
                sound_block_hit.play()
                pygame.draw.rect(sc, hit_color, hit_rect)
            
                # Incrementar la puntuación y llevar la cuenta de los ladrillos golpeados
                self.score += 5
                brick_hit += 1
                
                # Combo x2 al golpear 5 ladrillos seguidos y duracion del texto de combo
                if brick_hit % 5 == 0:
                    combo_time = 100
                    self.score += 10 * brick_hit
                    combo_text = score_font.render(f'x{brick_hit}', True, pygame.Color('yellow'))
                    combo_text_rect = combo_text.get_rect(center=combo_area.center)
                    sc.blit(combo_text, combo_text_rect)
                    ball_speed += 0.1
               
            # Efecto de combo
            if combo_time:
                combo_time -= 1
                combo_area.x += 5
                combo_text_rect.center = combo_area.center
                sc.blit(combo_text, combo_text_rect)
                pygame.draw.rect(sc, pygame.Color('yellow'), combo_area, 12)
            else:
                combo_area.x = -400
                
            # Comprobación de fin de partida
            if ball.bottom > HEIGHT:
                lives -= 1
                brick_hit = 0
                ball.center = (paddle.centerx, paddle.top - ball_radius)
                dx, dy = 1, -1
                fps = 40
                ball_speed = 10
                if lives == 0:
                    game_over_text = score_font.render('GAME OVER!', True, pygame.Color('red'))
                    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                    sc.blit(game_over_text, game_over_rect)
                    pygame.mixer.music.stop()
                    sound_game_over.play().set_volume(0.3)
                    pygame.display.flip()
                    pygame.time.delay(4000) # Espera 5 segundos antes de cerrar el juego
                    self.screen.fill((0, 0, 0))
                    self.save_score()
                    from NostalgiaZone import main_menu
                    main_menu()
                    
            elif not len(block_list):
                win_text = score_font.render('WIN!!!', True, pygame.Color('green'))
                win_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                sc.blit(win_text, win_rect)
                pygame.mixer.music.stop()
                sound_win.play().set_volume(0.3)
                pygame.display.flip()
                pygame.time.delay(4000)# Espera 4 segundos antes de cerrar el juego
                self.screen.fill((0, 0, 0))
                self.save_score()
                from NostalgiaZone import main_menu
                main_menu()
                
            # Movimiento de la barra
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT] and paddle.left - paddle_speed > 0:
                paddle.left -= paddle_speed
            if key[pygame.K_RIGHT] and paddle.right + paddle_speed < WIDTH:
                paddle.right += paddle_speed
                
            # Actualización de la pantalla
            pygame.display.flip()
            clock.tick(fps)