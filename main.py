
import pygame
import os 
import time
import random
import os
from os import path


pygame.font.init()
pygame.mixer.init(44100, -16,2,512)

WIDTH, HEIGHT = 750,750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brickshooter")

# Import des vaisseau
RED_SHIP = pygame.image.load(os.path.join("assets","pixel_ship_red_small.png"))
BLUE_SHIP = pygame.image.load(os.path.join("assets","pixel_ship_blue_small.png"))
GREEN_SHIP = pygame.image.load(os.path.join("assets","pixel_ship_orange_small.png"))

# Vaisseau du joueur 
YELLOW_SHIP = pygame.image.load(os.path.join("assets","faucon.png"))

# Import des balles

RED_LASER = pygame.image.load(os.path.join("assets","redlaser.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets","redlaser.png"))
GREEN_LASER= pygame.image.load(os.path.join("assets","redlaser.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets","finallaser1.png"))

# Map
MAP = pygame.transform.scale(pygame.image.load(os.path.join("assets","background.png")), (WIDTH, HEIGHT))

bulletSound = pygame.mixer.Sound(os.path.join("assets","pew.wav"))
explosionSound = pygame.mixer.Sound(os.path.join("assets","explosion.wav"))
Music = pygame.mixer.music.load(os.path.join("assets","ssbb.mp3"))

#Save Files settings

HS_FILE="highscore.txt"


class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x +  13 , self.y -55)) # laser fix 

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)


class Ship:
    COOLDOWN = 15
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            bulletSound.play()
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
	def __init__(self, x, y, health=100):
		super().__init__(x,y,health)
		self.ship_img = YELLOW_SHIP
		self.laser_img = YELLOW_LASER
		self.mask = pygame.mask.from_surface(self.ship_img)
		self.max_health = health

	def move_lasers(self, vel, objs):
		self.cooldown()
		for laser in self.lasers:
			laser.move(vel)
			if laser.off_screen(HEIGHT):
				self.lasers.remove(laser)
			else:
				for obj in objs:
					if laser.collision(obj):
						explosionSound.play()
						objs.remove(obj)
						if laser in self.lasers:
							self.lasers.remove(laser)

	def draw(self, window):
		super().draw(window)
		self.Drawhealth(window)

	def Drawhealth(self,window):
		pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() +10, self.ship_img.get_width(), 10))
		pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() +10, self.ship_img.get_width()* (self.health/self.max_health), 10))



class Enemy(Ship):
	COLOR_MAP = {
				"red": (RED_SHIP,RED_LASER),
				"green": (GREEN_SHIP,GREEN_LASER),
				"blue": (BLUE_SHIP,BLUE_LASER)
				}

	def __init__(self,x,y,color, health=100):
		super().__init__(x, y, health)
		self.ship_img, self.laser_img = self.COLOR_MAP[color]
		self.mask = pygame.mask.from_surface(self.ship_img)

	def move(self, vel):
		self.y += vel

	def shoot(self):
		if self.cool_down_counter == 0:
			laser = Laser(self.x-25, self.y+60, self.laser_img)
			self.lasers.append(laser)
			self.cool_down_counter = 1

	def score(self):
		score += 10
		


def collide(obj1, obj2):
	offset_x = obj2.x - obj1.x - 13 # hitbox fix 
	offset_y = obj2.y - obj1.y + 55
	return obj1.mask.overlap(obj2.mask, (offset_x,offset_y)) != None 



def main():
	pygame.mixer.music.play(1)
	main_font = pygame.font.SysFont("comicsans", 50)
	score_font = pygame.font.SysFont("comicsans", 30)
	enemy_left_font = pygame.font.SysFont("comicsans", 30)
	lost_font = pygame.font.SysFont("comicsans", 60)
	bonus_font = pygame.font.SysFont("comicsans", 60)


	run = True 
	FPS = 60   # image par seconde
	level = 0
	lives = 4
	Score = - 60
	enemies = []
	wave_length = 1
	enemy_vel = 2
	player_vel = 4
	laser_vel = 6
	lenght = 0
	counter = 0
	player = Player( 300, 600)
	Bonus = False
	clock  = pygame.time.Clock()
	green = 0, 255, 0
	lost = False
	lost_count = 0
	__file__ = 'modulename.py'
	def redraw_window():
		
		WIN.blit(MAP, (0,0))
		#Draw text++
		lives_label = main_font.render(f"Vie: {lives}",1, (255,255,255))
		level_label = main_font.render(f"Niveau: {level}", 1,(255,255,255))
		enemy_left_label = score_font.render(f"Ennemis restant: " + str(lenght), 1,(255,255,255))
		Score_label = score_font.render(f"Score: {Score}", 1,(255,255,255))
		highscore_label = score_font.render(f"Meilleur Score: {highscore}",1,(255,255,255))
		
		WIN.blit(highscore_label, (10,150))
		WIN.blit(lives_label, (10,10))
		WIN.blit(Score_label, (10,100))
		WIN.blit(enemy_left_label, (WIDTH - level_label.get_width() - 55, 100))
		WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

		for enemy in enemies:
			enemy.draw(WIN)

		player.draw(WIN)

		if lost:
			lost_label = lost_font.render("Game Over !",1, (255,255,255))
			WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))	

		pygame.display.update()


	def pause():
		paused = True

		while paused:
			for event in pygame.event.get():
					WIN.blit(MAP, (0,0))
					paused_label = score_font.render(f"Appuiyez sur P pour continuer ou echap pour quitter.",1,(255,255,255))
					WIN.blit(paused_label, (WIDTH/2 - paused_label.get_width()/2, 350))	
					pygame.display.update()
					clock.tick(5)
					keys = pygame.key.get_pressed()
					if keys[pygame.K_p]:
						paused = False
					if keys[pygame.K_ESCAPE]:
						quit()
					if event.type == pygame.QUIT:
						quit()

		
		pygame.display.update()
		clock.tick(5)
		

	while run:
		dir = path.dirname(__file__)
		with open(path.join(dir,HS_FILE),'r') as f:
			highscore = int(f.read())	



		lenght = len(enemies)
		clock.tick(FPS)
		redraw_window()
		if lives <= 0 or player.health <= 0:
			lost = True
			lost_count +=1

		if lost:
			if lost_count > FPS * 3:
				run = False
			else:
				continue

		if len(enemies) == 0:
			player.health = 100
			level += 1 
			wave_length += 5
			lives +=1
			Score += wave_length * 10 
			n = random.randint(1,4)
			if n == 1:
				player_vel = 8
				laser_vel = 12
			else:
				player_vel = 4
				laser_vel = 6

			for i in range(wave_length):
				enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red","blue","green"]))
				enemies.append(enemy)


		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()


		keys = pygame.key.get_pressed()
		if keys[pygame.K_LEFT]and player.x - player_vel > 0: # Deplacement à gauche  
			player.x -= player_vel
		if keys[pygame.K_RIGHT]and player.x + player_vel + player.get_width() < WIDTH: # Deplacement à droite
			player.x += player_vel
		if keys[pygame.K_UP] and player.y - player_vel > 0: # Deplacement vers le haut
			player.y -= player_vel
		if keys[pygame.K_DOWN] and player.y + player_vel + player.get_height() < HEIGHT: # Deplacement vers le bas 
			player.y += player_vel
		if keys[pygame.K_SPACE]:
			player.shoot()
			bulletSound.play()
		if keys[pygame.K_p]:
			pause()
		if keys[pygame.K_ESCAPE]:
			quit()
		if keys[pygame.K_TAB]:
			main_menu()




		for enemy in enemies[:]:
			enemy.move(enemy_vel)
			enemy.move_lasers(laser_vel, player)

			if random.randrange(0, 2*90) ==1:
				enemy.shoot()

			if collide(enemy, player):
				player.health ==100
				enemies.remove(enemy)

			elif enemy.y + enemy.get_height() > HEIGHT:
				lives -= 1
				enemies.remove(enemy)


		if Score > highscore:
				highscore = Score
				with open(path.join(dir, HS_FILE), 'w') as f:
					f.write(str(Score))



		player.move_lasers(-laser_vel, enemies)




def main_menu():
	title_font = pygame.font.SysFont("comicsans",40)
	rules_font = pygame.font.SysFont("comicsans",30)
	run = True
	while run:
		WIN.blit(MAP,(0,0))
		title_label = title_font.render("Click gauche pour jouer", 1, (255,255,255))
		WIN.blit(title_label, (WIDTH/2- title_label.get_width()/2,150))
		rules_label = rules_font.render("Appuiyez sur P pour pause/play", 1, (255,255,255))
		WIN.blit(rules_label, (WIDTH/2- rules_label.get_width()/2,350))
		rules_label = rules_font.render("Tab pour le menu ou echap pour quitter le jeu", 1, (255,255,255))
		WIN.blit(rules_label, (WIDTH/2- rules_label.get_width()/2,400))
		rules_label = rules_font.render("Fleches pour se déplacer, espace pour tirer", 1, (255,255,255))
		WIN.blit(rules_label, (WIDTH/2- rules_label.get_width()/2,450))
		credit_label = rules_font.render("Created by Samy L & Victor S", 1, (255,255,255))
		WIN.blit(credit_label, (WIDTH/2- credit_label.get_width()/2,650))
		pygame.display.update()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				main()
	pygame.quit() 

main_menu()