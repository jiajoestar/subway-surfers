from pygame import * 

import random 

init()

width = 450
height = 800
screen = display.set_mode((width,height))
display.set_caption("Subway Surfers")
homeScreenImage = image.load("homeScreen.jpg")
homeScreenImage = transform.scale(homeScreenImage, (width,height))

class Button(Rect):
	def __init__(self,x,y, callback): # removed buttonWidth, buttonHeight, action=None
		self.x = x
		self.y = y
		self.callback = callback
		super().__init__(x,y,271,106) # button width and height
		#gameOver = True 
		
	def drawButton(self,screen):
		pass
		
		
	def checkClicked(self,pos):
		if self.collidepoint(pos):
			self.callback()
			#gameOver = False (so when the button's clicked the game starts)
			
	def setCallBack(self, callback): #i need this in order for it to be responsive but i need an attribute callback?
		self.callback = callBack #can't set callback to None as None is not callable 
		

def startGame():
	print("start game")


class HomeScreen():
	def __init__(self):
		self.playButton = Button(93,558,0)
		self.running = True
		
	def display(self,screen):
		screen.blit(homeScreenImage, (0,0))
		
	def handleClick(self):
		pos = mouse.get_pos()
		if self.playButton.checkClicked(pos):
			self.playButton.setCallBack(startGame)
			#gameOver = False

'''
class PlayAgainScreen():
	def __init__(self):
		playAgainScreenImage = image.load("play again screen.png")
		playAgainScreenImage = transform.scale(playAgainScreenImage, (width,height))
		playAgainButton = Button(#,#)
		homeButton = Button(#,#)

	def display(self,screen):
		screen.blit(playAgainScreenImage, (0,0))
		
	#def displayLeaderboard(self):
		#pass
	
	def handleClick(self):
		pos = mouse.get_pos()
		if self.playAgainButton.checkClicked(pos):
			gameOver = False
	



class Player:
	def __init__(self):
		self.movex = 0
		self.movey = 0
		self.frame = 0
		self.images = []
		for i in range(1,5):
			img = image.load("jake running.png")
			self.images.append(img)
			self.image = self.images[0]
			self.rect = self.images.get_rect()
		
	def control(self,x,y):
		self.movex += x
		self.movey += y
		
	def update(self):
		self.rect.x = self.rect.x + self.movex
		self.rect.y = self.rect.y + self.movey
		
		# moving left
		if self.movex < 0:
			self.frame += 1
			if self.frame > 3*ani:
				self.frame = 0
				self.image = transform.flip(self.images[self.frame // ani], True, False)
		
		# moving right:
		if self.movex > 0:
			self.frame += 1
			if self.frame > 3*ani:
				self.frame = 0
				self.image = self.images[self.frame // ani]



class Polynomial:
	def __init__(self,coefficients,x):
		self.coefficients = coefficients
		self.x = x
	
	def scale(self,x):
		return Polynomial(self.coefficients * self.x)


obstacleOne = image.load("obstacle1.png")
obstacleOne = transform.scale(obstacleOne, (200,100))
obstacleTwo = image.load("obstacle2.png")
obstacleTwo = transform.scale(obstacleTwo, (200,500))

class MovingObstacles(Polynomial):
	def __init__(self):
		self.obstacles1 = []
		self.obstacles2 = []
		
	def create_obstacle1(self, self.obstacles1):
		x = 0
		
		while len(self.obstacles1)
		
	def create_obstacle2(self):
		pass

	def draw_obstacle1(self, self.obstacles1, screen):
		for i in self.obstacles1:
			screen.blit(obstacleOne, i)
			
		
	def draw_obstacle2(self,obstacle2):
		pass
	
	

class PowerUps:
	def __init__(self,x,y):
		self.x = random.randint(0,720)
		self.y = random.randint(0,1280)
		
	def boosterSneakers(self, self.x, self.y):
		pass
		
	def drawBoosterSneakers(self):
		boosterSneakersImage = image.load("booster sneakers.png")
		boosterSneakersImage = transform.scale(boosterSneakersImage, (self.x, self.y))
		
	def multiplier(self, self.x, self.y):
		pass
		
	def drawMultipliers(self):
		multiplierImage = image.load("multiplier.png")
		multiplierImage = transform.scale(multiplierImage, (self.x, self.y))
		
	def coinMagnet(self, self.x, self.y):
		pass
		
	def drawCoinMagnet(self):
		coinMagnetImage = image.load("coin magnet.png")
		coinMagnetImage = transform.scale(coinMagnetImage, (self.x, self.y))
		


character = Player() # spawning character
px = 200 # how much the character moves left and right
py = 200 # how much the character moves up (jumps)
character.rect.x = 0 # go to x
character.rect.y = 0 # go to y
'''
#homescreen = HomeScreen()

# game loop
gameOver = False
while not gameOver:
	for e in event.get():
		if e.type == QUIT:
			gameOver = True
		if e.type == KEYDOWN:
			if e.key == K_LEFT:
				character.control(-px,0)
			if e.key == K_RIGHT:
				character.control(px,0)
			if e.key == K_SPACE:
				character.control(0,-py)
		if e.type == MOUSEBUTTONDOWN:
			homescreen.handleClick()
		
	'''
	# spawning the obstacles
	obstacle1 = MovingObstacles(screen)
	obstacle1.create_obstacle1(screen)
	obstacle1.draw_obstacle1(screen)
	obstacle2 = MovingObstacles(screen)
	obstacle2.create_obstacle2(screen)
	obstacle2.draw_obstacle2(screen)
	
	# collision detection
	for i in obstacle1:
		if character.colliderect(i):
			playAgainPage = PlayAgainScreen(screen)
			playAgainPage.display(screen)
			playAgainPage.displayLeaderboard(screen)
	
	for j in obstacle2:
		if character.colliderect(j):
			playAgainPage = PlayAgainScreen(screen)
			playAgainPage.display(screen)
			playAgainPage.displayLeaderboard(screen)
	'''
	
	# draw background
	homescreen = HomeScreen()
	homescreen.display(screen)
	
	#character.update()
	
	
	display.flip()
	time.delay(10)
