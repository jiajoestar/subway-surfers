from pygame import * 

#import random 

init()

width = 450
height = 800
screen = display.set_mode((width,height))
display.set_caption("Subway Surfers")
homeScreenImage = image.load("homeScreen.jpg")
homeScreenImage = transform.scale(homeScreenImage, (width,height))


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
		

class HomeScreen():
	def __init__(self):
		self.playButton = Button(93,558,271,558)
		self.playButton.setCallBack(self.playClick) # starts game when play button is clicked
		#self.running = True
		self.nextScreen = self
		
	def display(self,screen): # displays homescreen
		screen.blit(homeScreenImage, (0,0))
		
	def handleClick(self): # checks the click
		pos = mouse.get_pos()
		self.playButton.checkClicked(pos)
		#if self.playButton.checkClicked(pos): print("start game")
		return self.nextScreen
		
	def playClick(self):
		self.nextScreen = GameScreen()
	
	def handleKey(self, key):
		pass
		
	def update(self):
		pass # move everything


class PlayAgainScreen():
	def __init__(self):
		self.playAgainScreenImage = image.load("play again screen.png")
		self.playAgainScreenImage = transform.scale(self.playAgainScreenImage, (width,height))
		self.playAgainButton = Button(425,746,179,651)
		self.homeButton = Button(161,747,21,651)
		self.playAgainButton.setCallBack(startGame) # starts game when play-again button is clicked

	def display(self,screen): # displays play-again screen
		screen.blit(self.playAgainScreenImage, (0,0))
		
	def handleClick(self):
		pos = mouse.get_pos()
		if self.playAgainButton.checkClicked(pos):
			gameOver = False
			

dy = 3 # how fast the obstacles move
class GameScreen():
	def __init__(self):
		self.gameScreenImage = image.load("game screen.jpg")
		self.gameScreenImage = transform.scale(self.gameScreenImage, (width,height))
		self.character = Character()
		self.px = 200 # how much the character moves left and right
		#self.py = 200 # how much the character moves up
		self.train = MovingObstacles() # creating trains
		self.train.create_trains(screen)
		self.hurdle = MovingObstacles() # creating hurdles
		self.hurdle.create_hurdles(screen)
		
	def display(self, screen): # displays 
		screen.blit(gameScreenImage, (0,0))
		currentScreen.display(screen)
		self.train.draw_trains(screen)
		self.hurdle.draw_hurdles(screen)
		
	def handleClick(self):
		pass
	
	def handleKey(self, key):
		if e.key == K_LEFT:
			self.character.move_ip(-self.px,0)
		if e.key == K_RIGHT:
			self.character.move_ip(self.px,0)
		#if e.key == K_SPACE:
		#	self.character.move_ip(0,-self.py)
	
	def update(self): # moves everything
		#pass
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


class MovingObstacles:
	def __init__(self):
		self.trainImage = image.load("train.png")
		self.trainImage = transform.scale(self.trainImage, (200,100))
		self.hurdleImage = image.load("hurdle.png")
		self.hurdleImage = transform.scale(self.hurdleImage, (200,500))
		self.trains = []
		self.hurdles = []
		
	def create_trains(self, screen):
		y = 0 # obstacles will appear from the top of the screen (hopefully)
		
		while len(self.trains) < 6:
			self.trains.append(Rect(90,y,100,200)) # trains appearing on the left side
			self.trains.append(Rect(183,y,100,200)) # train appearing in the middle
			self.trains.append(Rect(313,y,100,200)) # train appearing on the right side
			y += 500
		
		return self.trains
		
	def create_hurdles(self, screen): 
		y = 0
		
		while len(self.hurdles) < 3:
			self.hurdles.append(Rect(90,y,80,70)) # hurdles appearing on the left side
			self.hurdles.append(Rect(183,y,80,70)) # hurdles appearing in the middle
			self.hurdles.append(Rect(313,y,80,70)) # hurdles appearing on the right side
			y += 800
		
		return self.hurdles

	def draw_trains(self, screen): 
		for i in self.trains:
			screen.blit(self.trainImage, i)
		
	def draw_hurdles(self, screen):
		for j in self.hurdles:
			screen.blit(self.hurdleImage, j)



class Character(Rect):
	def __init__(self):
		super().__init__(188,700,87,114)# position of where the character spawns and its width and height
		self.characterImage = image.load("jake running.png")
		self.characterImage = transform.scale(self.characterImage, (87,114)) #width and height of character

currentScreen = HomeScreen()
gameScreen = GameScreen()

# game loop
gameOver = False
while not gameOver:
	for e in event.get():
		if e.type == QUIT:
			gameOver = True
		if e.type == KEYDOWN:
			currentScreen.handleKey(e.key)
		if e.type == MOUSEBUTTONDOWN:
			currentScreen = currentScreen.handleClick()
	currentScreen.update()
	currentScreen.display(screen)
	
	display.flip()
	time.delay(10)
