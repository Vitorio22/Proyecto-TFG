import pygame, random, sys, requests, json
from pygame.locals import *

WIDTH = 900
HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroids")
clock = pygame.time.Clock()

#funcion para escribir
def draw_text(surface, text, size, x, y):
	font = pygame.font.Font("games/Asteroids/assets/fonts/ARCADE_I.TTF", size)
	text_surface = font.render(text, True, WHITE)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)
	surface.blit(text_surface, text_rect)

#funcion que dibuja la vida del jugador/nave
def draw_shield_bar(surface, x, y, percentage):
	BAR_LENGHT = 100
	BAR_HEIGHT = 10
	fill = (percentage / 100) * BAR_LENGHT
	border = pygame.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
	fill = pygame.Rect(x, y, fill, BAR_HEIGHT)
	pygame.draw.rect(surface, GREEN, fill)
	pygame.draw.rect(surface, WHITE, border, 2)

#clase jugador/nave
class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("games/Asteroids/assets/img/player.png").convert()
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.centerx = WIDTH // 2
		self.rect.bottom = HEIGHT - 10
		self.speed_x = 0
		self.shield = 100
	#movimiento
	def update(self):
		self.speed_x = 0
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_LEFT]:
			self.speed_x = -5
		if keystate[pygame.K_RIGHT]:
			self.speed_x = 5
		self.rect.x += self.speed_x
		if self.rect.right > WIDTH:
			self.rect.right = WIDTH
		if self.rect.left < 0:
			self.rect.left = 0
	#disparo
	def shoot(self, all_sprites, bullets):
		bullet = Bullet(self.rect.centerx, self.rect.top)
		all_sprites.add(bullet)
		bullets.add(bullet)
		laser_sound.play()

#Clase meteorito
class Meteor(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = random.choice(meteor_images)
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(WIDTH - self.rect.width)
		self.rect.y = random.randrange(-140, -100)
		self.speedy = random.randrange(4, 10)
		self.speedx = random.randrange(-5, 5)
	#movimiento
	def update(self):
		self.rect.y += self.speedy
		self.rect.x += self.speedx
		if self.rect.top > HEIGHT + 10 or self.rect.left < -40 or self.rect.right > WIDTH + 40:
			self.rect.x = random.randrange(WIDTH - self.rect.width)
			self.rect.y = random.randrange(-140, - 100)
			self.speedy = random.randrange(4, 10)

#Clase bala/laser
class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.image = pygame.image.load("games/Asteroids/assets/img/laser1.png")
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.y = y
		self.rect.centerx = x
		self.speedy = -10
	#movimiento
	def update(self):
		self.rect.y += self.speedy
		if self.rect.bottom < 0:
			self.kill()

#Clase explosion
class Explosion(pygame.sprite.Sprite):
	def __init__(self, center):
		super().__init__()
		self.image = explosion_anim[0]
		self.rect = self.image.get_rect()
		self.rect.center = center 
		self.frame = 0
		self.last_update = pygame.time.get_ticks()
		self.frame_rate = 50 # VELOCIDAD DE LA EXPLOSION

	def update(self):
		now = pygame.time.get_ticks()
		if now - self.last_update > self.frame_rate:
			self.last_update = now
			self.frame += 1
			if self.frame == len(explosion_anim):
				self.kill()
			else:
				center = self.rect.center
				self.image = explosion_anim[self.frame]
				self.rect = self.image.get_rect()
				self.rect.center = center

#pantalla de inicio
def show_go_screen(screen):
	screen.blit(background, [0,0])
	draw_text(screen, "Asteroids", 65, WIDTH // 2, HEIGHT // 6)
	draw_text(screen, "Moverse = < > ", 27, WIDTH // 2, HEIGHT // 2.5)
	draw_text(screen, "Disparar = espacio ", 27, WIDTH // 2, HEIGHT // 2)
	draw_text(screen, "Press key to play", 20, WIDTH // 2, HEIGHT * 3/4)
	pygame.display.flip()
	waiting = True
	while waiting:
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYUP:
				waiting = False
			
#lista de meteoritos
meteor_images = []
meteor_list = ["games/Asteroids/assets/img/meteorGrey_big1.png", "games/Asteroids/assets/img/meteorGrey_big2.png", "games/Asteroids/assets/img/meteorGrey_big3.png",
			 "games/Asteroids/assets/img/meteorGrey_big4.png", "games/Asteroids/assets/img/meteorGrey_med1.png", 
		   "games/Asteroids/assets/img/meteorGrey_med2.png", "games/Asteroids/assets/img/meteorGrey_small1.png"
				]
for img in meteor_list:
	meteor_images.append(pygame.image.load(img).convert())


#Explosion
explosion_anim = []
for i in range(9):
	file = "games/Asteroids/assets/img/regularExplosion0{}.png".format(i)
	img = pygame.image.load(file).convert()
	img.set_colorkey(BLACK)
	img_scale = pygame.transform.scale(img, (70,70))
	explosion_anim.append(img_scale)

# Cargar imagen de fondo
background = pygame.image.load("games/Asteroids/assets/background/background.png").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Cargar sonidos
laser_sound = pygame.mixer.Sound("games/Asteroids/assets/sounds/laser5.ogg")
explosion_sound = pygame.mixer.Sound("games/Asteroids/assets/sounds/explosion.mp3")
pygame.mixer.music.load("games/Asteroids/assets/sounds/music.ogg")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(loops=-1)

#GAME OVER
game_over = True
running = True
class Game:
	
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
 
	def show_message_centered(self, message):
		# Tamaño de la pantalla
		SCREEN_WIDTH = 800
		SCREEN_HEIGHT = 600
		# Colores
		FONDO_COLOR = (29, 62, 90)
		WHITE = (255, 255, 255)

		message_font = pygame.font.Font("games/Asteroids/assets/fonts/ARCADE_I.TTF", 18)
		message_surf = message_font.render(message, True, WHITE)
		message_rect = message_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

		self.screen.fill(FONDO_COLOR)
		self.screen.blit(message_surf, message_rect)
		pygame.display.flip()
		pygame.time.delay(2000)
	
	#Guardar puntuaciones en un fichero externo (json)
	def save_score(self):
		# Tamaño de la pantalla
		SCREEN_WIDTH = 1000
		SCREEN_HEIGHT = 600
		# Colores
		WHITE = (255, 255, 255)
		FONDO_COLOR = (29, 62, 90)
		
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
				"Puntuacion: " + str(self.score),
				"Introduce tu nombre: " + player_name,
			]
			control_font = pygame.font.Font("games/Asteroids/assets/fonts/ARCADE_I.TTF", 20)
			control_surf = pygame.Surface((SCREEN_WIDTH // 2 + 100, SCREEN_HEIGHT // 2))
			control_surf.fill(FONDO_COLOR)
			for i, text in enumerate(control_text):
				control_render = control_font.render(text, True, WHITE)
				control_rect = control_render.get_rect(center=(SCREEN_WIDTH // 4 + 50, (SCREEN_HEIGHT // 4 - 50) + (i * 50)))
				control_surf.blit(control_render, control_rect)
			self.screen.blit(control_surf, control_surf.get_rect(center=(SCREEN_WIDTH // 2.2, SCREEN_HEIGHT // 2)))
			pygame.draw.rect(self.screen, WHITE, control_surf.get_rect(center=(SCREEN_WIDTH // 2.2, SCREEN_HEIGHT // 2)), 3, border_radius=5)

			# Dibujar mensaje de pulsar enter
			button_font = pygame.font.Font("games/Asteroids/assets/fonts/ARCADE_I.TTF", 30)
			button_text = button_font.render("Pulsa Enter", True, WHITE)
			button_rect = button_text.get_rect(center=(SCREEN_WIDTH // 2.2, SCREEN_HEIGHT - 100))
			pygame.draw.rect(self.screen, FONDO_COLOR, button_rect)
			pygame.draw.rect(self.screen, WHITE, button_rect, 3, border_radius=5)
			self.screen.blit(button_text, button_rect)

			pygame.display.flip()
		
		return player_name, score

	def send_score(self, player_name, score):
		# URL del endpoint para guardar la puntuación
		url = "http://localhost:5000/save_score_asteroids"
		
		headers = {"Content-Type": "application/json"}
		data = json.dumps({"nombre": player_name, "puntuacion": score})
		
		response = requests.post(url, headers=headers, data=data)
		
		if response.status_code == 200:
			print("Puntuación guardada exitosamente")
		else:
			print("Error al guardar la puntuación")
	
	def __init__(self):
	 
		self.score = 0
		running = True
		game_over = True
		while running:
			if game_over:

				show_go_screen(screen)
				game_over = False
				all_sprites = pygame.sprite.Group()
				meteor_list = pygame.sprite.Group()
				bullets = pygame.sprite.Group()
				player = Player()
				all_sprites.add(player)
				for i in range(8):
					meteor = Meteor()
					all_sprites.add(meteor)
					meteor_list.add(meteor)

			clock.tick(60)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						player.shoot(all_sprites ,bullets)

			all_sprites.update()
			#colisiones - meteoro - laser
			hits = pygame.sprite.groupcollide(meteor_list, bullets, True, True)
			for hit in hits:
				self.score += 10
				explosion_sound.play()
				explosion = Explosion(hit.rect.center)
				all_sprites.add(explosion)
				meteor = Meteor()
				all_sprites.add(meteor)
				meteor_list.add(meteor)
   
			# Checar colisiones - jugador - meteoro
			hits = pygame.sprite.spritecollide(player, meteor_list, True)
			for hit in hits:
				player.shield -= 25
				meteor = Meteor()
				all_sprites.add(meteor)
				meteor_list.add(meteor)
				if player.shield <= 0:
					game_over = True
					self.save_score()
					pygame.mixer.music.stop()
					from NostalgiaZone import main_menu
					main_menu()
	 
			pygame.display.flip()

			screen.blit(background, [0, 0])
			all_sprites.draw(screen)
			# Marcador
			draw_text(screen, str(self.score), 25, WIDTH // 2, 10)
			# Escudo
			draw_shield_bar(screen, 5, 5, player.shield)