import numpy as np
import pygame

pygame.init()

WIDTH,HEIGHT=800,500
BLACK,RED=(0,0,0),(255,0,0)

screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Put Fruit')
fpsClock=pygame.time.Clock()
font=pygame.font.SysFont('fonts/04B_19.TTF',39)

background=pygame.image.load('images/background.jpg')
set_apple=pygame.image.load('images/apple.png')
apples=pygame.transform.scale(set_apple,(150,150)).convert_alpha()
set_x_tic=pygame.image.load('images/X-Tic.png')
x_tic=pygame.transform.scale(set_x_tic,(150,150)).convert_alpha()
set_red_button=pygame.image.load('images/red-button.png')
red_rect=pygame.transform.scale(set_red_button,(70,70)).convert_alpha()
set_gameover=pygame.image.load('images/gameover.png')
gameover=pygame.transform.scale(set_gameover,(200,70))

class SFX:
	fx_flap=pygame.mixer.Sound('sounds/sfx_wing.wav')
	fx_hit=pygame.mixer.Sound('sounds/sfx_hit.wav')
	fx_point=pygame.mixer.Sound('sounds/sfx_point.wav')
	fx_no6=pygame.mixer.Sound('sounds/no6.wav')

class activate():
	def __init__(self):
		self.score,self.count_rect=0,3
		self.x_matrix=np.zeros((3,3))
		self.state="Welcome"

	def play_game(self):
		if self.state=="Running":
			draw_rect()
			if not update.alive:
				self.state="Over"
				SFX.fx_hit.play()		

	def start(self):
		if self.state=="Welcome" and update.alive: self.state="Running"
		elif not update.alive:
			self.state="Running"
			self.score,self.count_rect=0,3
			update.alive=True
			update.matrix=set_matrix()
			update.here_apple=np.array([[2,2,2],[2,2,2],[2,2,2]])

	def restart(self):
		self.x_matrix=update.matrix
		update.test_alive()
		if self.score%4==0 and self.count_rect<8: self.count_rect+=1
		if self.state=="Running" and update.alive:
			SFX.fx_point.play()
			update.matrix=set_matrix()
			update.here_apple=np.array([[2,2,2],[2,2,2],[2,2,2]])

	def draw_word(self):
		if self.state=="Welcome":
			welcome_txt=font.render("Press Enter to Start!",True,RED)
			screen.blit(welcome_txt,(525,90))
		elif self.state=="Over":
			screen.blit(gameover,(560,100))
			over_text=font.render("Press Enter to Restart",True,RED)
			screen.blit(over_text,(520,50))
			draw_x_tic(self.x_matrix)
		else:
			score_text=font.render("Your score: {}".format(self.score),True,RED)
			screen.blit(score_text,(545,90))
		
class update_matrix():
	def __init__(self):
		self.alive=True
		self.matrix=set_matrix()
		self.here_apple=np.array([[2,2,2],[2,2,2],[2,2,2]])

	def test_alive(self):
		a,b=apple.apple_x//175,apple.apple_y//175
		self.here_apple[a][b]=1
		for i in range(3):
			for j in range(3):
				if self.matrix[i][j]==self.here_apple[i][j]: self.alive=False	

class set_apple():
	def __init__(self):
		self.apple_x,self.apple_y=180,175
					
	def motion_apple(self,num):
		if num==0: 
			if self.apple_y<175: self.apple_y=350
			else: self.apple_y-=175
		elif num==1: 
			if self.apple_y>175: self.apple_y=0
			else: self.apple_y+=175
		elif num==2: 
			if self.apple_x<180: self.apple_x=355
			else: self.apple_x-=175
		else:
			if self.apple_x>180: self.apple_x=5
			else: self.apple_x+=175
		SFX.fx_flap.play()

def set_matrix():
	matrix=np.zeros((3,3))
	while True:
		if np.sum(matrix)==aller.count_rect: break
		else: matrix=np.random.randint(((2,2,2),(2,2,2),(2,2,2)))
	return matrix

def draw_rect():
	for i in range(3):
		for j in range(3):
			if update.matrix[i][j]==1: screen.blit(red_rect,((i+1)*70+480,(j+1)*70+125))

def draw_x_tic(matrix_x):
	for i in range(3):
		for j in range(3):
			if matrix_x[i][j]==1: screen.blit(x_tic,(i*175+5,j*170+5))

def draw_screen():
	screen.blit(background,(0,0))
	screen.blit(apples,(apple.apple_x,apple.apple_y))
	
aller=activate()
update=update_matrix()
apple=set_apple()

running=True
while running:
	for event in pygame.event.get():
		if event.type==pygame.QUIT: running=False
		if event.type==pygame.KEYDOWN:
			if event.key==pygame.K_SPACE:
				aller.score+=1
				aller.restart()
			if event.key==pygame.K_KP_ENTER: aller.start()
			if event.key==pygame.K_UP or event.key==pygame.K_w: apple.motion_apple(0)
			if event.key==pygame.K_DOWN or event.key==pygame.K_s: apple.motion_apple(1)
			if event.key==pygame.K_LEFT or event.key==pygame.K_a: apple.motion_apple(2)
			if event.key==pygame.K_RIGHT or event.key==pygame.K_d: apple.motion_apple(3)

	draw_screen()
	aller.draw_word()
	aller.play_game()
	
	pygame.display.update()
	fpsClock.tick(60)

pygame.quit()