from pygame import * 

import random 

init()

width = 450
height = 800
screen = display.set_mode((width,height))
display.set_caption("Subway Surfers")
homeScreenImage = image.load("homeScreen.jpg")
homeScreenImage = transform.scale(homeScreenImage, (width,height))
#gameScreenImage = image.load("game screen.jpg")
#gameScreenImage = transform.scale(gameScreenImage, (width,height))
# ^ put into handleClick method in class PlayAgainScreen


class Button(Rect):
	def __init__(self,x,y,buttonWidth,buttonHeight):
		self.x = x
		self.y = y
		self.buttonWidth = buttonWidth
		self.buttonHeight = buttonHeight
		super().__init__(x,y,buttonWidth,buttonHeight) #sets dimensions of the button
		
	def drawButton(self,screen):
		pass
		
	def checkClicked(self,pos):
		if self.collidepoint(pos):
			self.callback()
			
	def setCallBack(self, callback): 
		self.callback = callback
		


#testing whether it prints "start game" when button is clicked
#def startGame():
#	print("start game")
#	gameOver = False


class HomeScreen():
	def __init__(self):
		self.playButton = Button(93,558,271,558)
		self.playButton.setCallBack(startGame) #starts game when play button is clicked
		self.running = True
		
	def display(self,screen): #displays homescreen
		screen.blit(homeScreenImage, (0,0))
		
	def handleClick(self): #checks the click
		pos = mouse.get_pos()
		self.playButton.checkClicked(pos)
		# if self.playButton.checkClicked(pos): print("start game")


class PlayAgainScreen():
	def __init__(self):
		self.playAgainScreenImage = image.load("play again screen.png")
		self.playAgainScreenImage = transform.scale(self.playAgainScreenImage, (width,height))
		self.playAgainButton = Button(425,746,179,651)
		self.homeButton = Button(161,747,21,651)
		self.playAgainButton.setCallBack(startGame) #starts game when play-again button is clicked

	def display(self,screen): #displays play-again screen
		screen.blit(self.playAgainScreenImage, (0,0))
		
	def handleClick(self):
		pos = mouse.get_pos()
		if self.playAgainButton.checkClicked(pos):
			gameOver = False
			gameScreenImage = image.load("game screen.jpg")
			gameScreenImage = transform.scale(gameScreenImage, (width,height))

#tbh idk if i really need player as a class
class Player:
	def __init__(self):
		self.movex = 0
		self.movey = 0
		self.frame = 0
		self.character = image.load("jake running.png")
		self.character = transform.scale(self.character, (87,114)) #width and height of character
		
	'''	
	# need to change this
	
	#def control(self,x,y):
	#	self.movex += x
	#	self.movey += y
		
	def update(self):
		self.rect.x = self.rect.x + self.movex
		self.rect.y = self.rect.y + self.movey
		
		# moving left
		if self.movex < 0:
			self.frame += 1
		
		# moving right:
		if self.movex > 0:
			self.frame += 1
			if self.frame > 3*ani:
				self.frame = 0
	'''

'''
trainObstacleImage = image.load("train.png")
trainObstacleImage = transform.scale(trainObstacleImage, (200,100))
hurdleImage = image.load("hurdle.png")
hurdleImage = transform.scale(hurdleImage, (200,500))
'''

class MovingObstacles:
	def __init__(self):
	
		self.trainImage = image.load("train.png")
		self.trainImage = transform.scale(self.trainImage, (200,100))
		self.hurdleImage = image.load("hurdle.png")
		self.hurdleImage = transform.scale(self.hurdleImage, (200,500))
		# ^ idk if i should add these in the constructor or leave it outside the class??
		
		self.trains = []
		self.hurdles = []
		
		
	def create_trains(self, self.trains):
		y = 0 #obstacles will appear from the top of the screen (hopefully)
		
		while len(self.trains) < 6:
			self.trains.append(Rect(90,y,100,200)) #trains appearing on the left side
			self.trains.append(Rect(183,y,100,200)) #train appearing in the middle
			self.trains.append(Rect(313,y,100,200)) #train appearing on the right side
			y += 500
		
		return self.trains
		
		
	def create_hurdles(self, self.hurdles):
		y = 0
		
		while len(self.hurdles) < 3:
			self.hurdles.append(Rect(90,y,80,70)) #hurdles appearing on the left side
			self.hurdles.append(Rect(183,y,80,70)) #hurdles appearing in the middle
			self.hurdles.append(Rect(313,y,80,70)) #hurdles appearing on the right side
			y += 800
		
		return self.hurdles


	def draw_trains(self, self.trains, screen):
		for i in self.trains:
			screen.blit(trainImage, i)
			
		
	def draw_hurdles(self, self.hurdles, screen):
		for j in self.hurdles:
			screen.blit(hurdleImage, j)

	
character = Player() # spawning character
character = Rect(188,700,87,114)
px = 200 # how much the character moves left and right
py = 200 # how much the character moves up (jumps)
dy = 3

# game loop
def startGame():
	gameOver = False
	while not gameOver:
		for e in event.get():
			if e.type == QUIT:
				gameOver = True
			if e.type == KEYDOWN:
				if e.key == K_LEFT:
					character.move_ip(-px,0)
				if e.key == K_RIGHT:
					character.move_ip(px,0)
				if e.key == K_SPACE:
					character.move_ip(0,-py)
		if e.type == MOUSEBUTTONDOWN:
			homescreen.handleClick()
			playAgainPage.handleClick()
			
		# draw gamescreen
		screen.blit(gameScreenImage, (0,0))
		
		# spawning the obstacles
		train = MovingObstacles()
		train.create_train(screen)
		train.draw_train(screen)
		hurdle = MovingObstacles()
		hurdle.create_hurdle(screen)
		hurdle.draw_hurdle(screen)
		
		for a in self.trains:
			a.move_ip(0,dy)
			screen.blit(train,a)
		
		for a in self.trains:
			if a.y >= height:
				self.trains.remove(a)
				self.trains.append(Rect(90,0,100,200))
				self.trains.append(Rect(183,0,100,200))
				self.trains.append(Rect(313,0,100,200))	
		
		for b in self.hurdles:
			a.move_ip(0,dy)
			screen.blit(hurdle,a)
			
		for b in self.hurdles:
			if b.y <= 0:
				self.hurdles.remove(j)
				self.hurdles.append(Rect(width,0,100,80,70))
			
		# collision detection
		# when the character collides with the obstacles, the play-again screen appears
		for a in train:
			if character.colliderect(a):
				playAgainPage = PlayAgainScreen()
				playAgainPage.display(screen)
			
		for b in hurdle:
			if character.colliderect(b):
				playAgainPage = PlayAgainScreen()
				playAgainPage.display(screen)
				
			
		# draw homescreen
		homescreen = HomeScreen()
		homescreen.display(screen)
			
		# displaying character
		screen.blit(characterImage, character)
			
		display.flip()
		time.delay(10)
