import numpy as np
import pygame
from random import randint

pygame.init()

WIDTH,HEIGHT=800,500
BLACK,RED=(0,0,0),(255,0,0)

screen=pygame.display.set_mode((WIDTH,HEIGHT))
font=pygame.font.SysFont('fonts/04B_19.TTF',39)
Font=pygame.font.SysFont('digital-7',60)
pygame.display.set_caption('Put Fruit')
pygame.time.set_timer(pygame.USEREVENT,100)
fpsClock=pygame.time.Clock()

welcome_txt=font.render("Press Enter to Start!",True,RED)
over_text=font.render("Press Enter to Restart",True,RED)
background=pygame.image.load('images/background.jpg')
flame_clock=pygame.image.load('images/flame_clock.png')
set_x_tic=pygame.image.load('images/X-Tic.png')
set_gameover=pygame.image.load('images/gameover.png')
signal_down=pygame.image.load('images/signals/signal_down.png')
signal_up=pygame.image.load('images/signals/signal_up.png')
signal_left=pygame.image.load('images/signals/signal_left.png')
signal_right=pygame.image.load('images/signals/signal_right.png')
signal_corner=pygame.image.load('images/signals/signal_corner.png')

up=pygame.transform.scale(signal_up,(212,25)).convert_alpha()
down=pygame.transform.scale(signal_down,(212,25)).convert_alpha()
left=pygame.transform.scale(signal_left,(25,212)).convert_alpha()
right=pygame.transform.scale(signal_right,(25,212)).convert_alpha()
corner=pygame.transform.scale(signal_corner,(300,300)).convert_alpha()
flame=pygame.transform.scale(flame_clock,(212,100)).convert_alpha()
x_tic=pygame.transform.scale(set_x_tic,(150,150)).convert_alpha()
gameover=pygame.transform.scale(set_gameover,(200,70)).convert_alpha()

class SFX:
	fx_flap=pygame.mixer.Sound('sounds/sfx_wing.wav')
	fx_hit=pygame.mixer.Sound('sounds/sfx_hit.wav')
	fx_point=pygame.mixer.Sound('sounds/sfx_point.wav')

class random_value():
	def __init__(self):
		self.rand=randint(1,4)
		self.rand_0=randint(1,4)

	def rd_fruit(self):
		set_fruit=pygame.image.load('images/fruits/{}.png'.format(self.rand))
		fruits=pygame.transform.scale(set_fruit,(150,150)).convert_alpha()
		return fruits

	def rd_button(self):
		set_button=pygame.image.load('images/buttons/{}.png'.format(self.rand))
		buttons=pygame.transform.scale(set_button,(70,70)).convert_alpha()
		return buttons

class activate():
	def __init__(self):
		self.speed, self.count_rect, self.score=4, 3, 0
		self.x_matrix=np.zeros((3,3))
		self.state="Welcome"

	def play_game(self):
		if self.state=="Running": 
			draw_rect()
			if not update.alive:
				self.state="Over"
				self.x_matrix=update.matrix
				SFX.fx_hit.play()		

	def start(self):
		if self.state=="Welcome" and update.alive: self.state="Running"
		elif not update.alive:
			self.state="Running"
			self.speed, self.count_rect, self.score=4, 3, 0
			fruit.fruit_x, fruit.fruit_y=180, 175
			rd.rand=randint(1,4)
			rd.rd_fruit()
			rd.rd_button()
			update.alive=True
			update.matrix=set_matrix()
			update.draw_matrix=update.tranpose_matrix()
			update.here_fruit=np.array([[2,2,2],[2,2,2],[2,2,2]])

	def restart(self):
		rd.rand_0=randint(1,4)
		self.x_matrix=update.matrix
		self.speed=(4.5+1.2)-self.count_rect*0.4
		update.test_alive()
		if self.score==24: self.count_rect=2
		if self.score%4==0 and self.score!=0 and self.count_rect<8: self.count_rect+=1
		if self.state=="Running" and update.alive:
			self.score+=1
			update.matrix=set_matrix()
			update.draw_matrix=update.tranpose_matrix()
			update.here_fruit=np.array([[2,2,2],[2,2,2],[2,2,2]])
			SFX.fx_point.play()
			
class update_spirit():
	def __init__(self):
		self.alive=True
		self.matrix=set_matrix()
		self.draw_matrix=self.tranpose_matrix()
		self.here_fruit=np.array([[2,2,2],[2,2,2],[2,2,2]])

	def test_alive(self):
		a, b=fruit.fruit_x//175, fruit.fruit_y//175
		self.here_fruit[a][b]=1
		for i in range(3):
			for j in range(3):
				if self.matrix[i][j]==self.here_fruit[i][j]: self.alive=False

	def tranpose_matrix(self):
		tran_matrix=np.zeros((3,3))
		if rd.rand_0==1: tran_matrix=np.transpose(self.matrix)
		elif rd.rand_0==2:
			tran_matrix[0,:]=self.matrix[2,:]
			tran_matrix[1,:]=self.matrix[1,:]
			tran_matrix[2,:]=self.matrix[0,:]
		elif rd.rand_0==3:
			tran_matrix[:,0]=self.matrix[:,2]
			tran_matrix[:,1]=self.matrix[:,1]
			tran_matrix[:,2]=self.matrix[:,0]
		else: tran_matrix=self.matrix
		return tran_matrix

class set_fruit():
	def __init__(self):
		self.fruit_x, self.fruit_y=180, 175
					
	def motion_fruit(self,num):
		if num==0: 
			if self.fruit_y<175: self.fruit_y=350
			else: self.fruit_y-=175
		elif num==1: 
			if self.fruit_y>175: self.fruit_y=0
			else: self.fruit_y+=175
		elif num==2: 
			if self.fruit_x<180: self.fruit_x=355
			else: self.fruit_x-=175
		else:
			if self.fruit_x>180: self.fruit_x=5
			else: self.fruit_x+=175
		SFX.fx_flap.play()

def set_matrix():
	matrix=np.zeros((3,3))
	while True:
		if np.sum(matrix)==play.count_rect: break
		else: matrix=np.random.randint(((2,2,2),(2,2,2),(2,2,2)))
	return matrix

def draw_rect():
	buttons=rd.rd_button()
	if play.score>24:
		for i in range(3):
			for j in range(3): 
				if update.draw_matrix[i][j]==1: screen.blit(buttons,((i+1)*70+480,(j+1)*70+125))
	else:
		for i in range(3):
			for j in range(3): 
				if update.matrix[i][j]==1: screen.blit(buttons,((i+1)*70+480,(j+1)*70+125))

def draw_x_tic(matrix_x):
	for i in range(3):
		for j in range(3):
			if matrix_x[i][j]==1: screen.blit(x_tic,(i*175+5,j*170+5))

def draw_screen():
	fruits=rd.rd_fruit()
	screen.blit(background,(0,0))
	screen.blit(fruits,(fruit.fruit_x,fruit.fruit_y))
	if play.state=="Welcome":
		screen.blit(welcome_txt,(525,90))
	elif play.state=="Over":
		screen.blit(gameover,(560,100))
		screen.blit(over_text,(520,50))
		draw_x_tic(play.x_matrix)
	else:
		score_text=font.render("Your score: {}".format(play.score),True,RED)
		txt_timer=Font.render('00:{}'.format(round(play.speed,2)),True,BLACK)
		screen.blit(score_text,(575,120))
		screen.blit(flame,(552,25))
		screen.blit(txt_timer,(590,50))
		if play.score>24:
			if rd.rand_0==1: screen.blit(corner,(510,160))
			elif rd.rand_0==2:
				screen.blit(left,(520,194))
				screen.blit(right,(765,194))
			elif rd.rand_0==3:
				screen.blit(up,(549,165))
				screen.blit(down,(549,410))
				
rd=random_value()
play=activate()
update=update_spirit()
fruit=set_fruit()

def main():
	running=True
	while running:
		for event in pygame.event.get():
			if event.type==pygame.QUIT: running=False
			if event.type==pygame.USEREVENT: 
				play.speed-=0.1
				if play.speed<0: 
					update.test_alive() 
					if update.alive: play.restart()
			if event.type==pygame.KEYDOWN:
				if event.key==pygame.K_SPACE: play.restart()
				if event.key==pygame.K_KP_ENTER: play.start()
				if (event.key==pygame.K_UP or event.key==pygame.K_w) and play.state=="Running": fruit.motion_fruit(0)
				if (event.key==pygame.K_DOWN or event.key==pygame.K_s) and play.state=="Running": fruit.motion_fruit(1)
				if (event.key==pygame.K_LEFT or event.key==pygame.K_a) and play.state=="Running": fruit.motion_fruit(2)
				if (event.key==pygame.K_RIGHT or event.key==pygame.K_d) and play.state=="Running": fruit.motion_fruit(3)

		draw_screen()
		play.play_game()
		
		pygame.display.update()
		fpsClock.tick(60)
	pygame.quit()

if __name__=="__main__":
	main()