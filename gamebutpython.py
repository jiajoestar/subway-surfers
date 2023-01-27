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
		super().__init__(x,y,buttonWidth,buttonHeight) #sets position and dimensions of the button
		
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
		#self.playAgainButton.setCallBack(startGame) # starts game when play-again button is clicked

	def display(self,screen): # displays play-again screen
		screen.blit(self.playAgainScreenImage, (0,0))
		
	def handleClick(self):
		pos = mouse.get_pos()
		if self.playAgainButton.checkClicked(pos):
			gameOver = False
			

class GameScreen():
	def __init__(self):
		self.gameScreenImage = image.load("game screen.jpg")
		self.gameScreenImage = transform.scale(self.gameScreenImage, (width,height))
		self.character = Character()
		self.px = 200 # how much the character moves left and right
		#self.py = 200 # how much the character moves up
		self.moveObs = MovingObstacles() # creating obstacles
		self.moveObs.create_trains(screen)
		self.moveObs.create_hurdles(screen)
#		self.hurdle = MovingObstacles()
#		self.hurdle.create_hurdles(screen)
		
	def display(self, screen): # displays 
		screen.blit(self.gameScreenImage, (0,0))
		self.moveObs.draw_trains(screen)
		self.moveObs.draw_hurdles(screen)
		
	def handleClick(self):
		pass
	
	def handleKey(self, key):
		if e.key == K_LEFT:
			self.character.move_ip(-self.px,0)
		if e.key == K_RIGHT:
			self.character.move_ip(self.px,0)
#		if e.key == K_SPACE:
#			self.character.move_ip(0,-self.py)
	
	def update(self): # moves everything
		self.moveObs.removeObs()
		self.moveObs.movingObs()
		
		# checks collisions
		if self.moveObs.checkCollision(self.character):
			playAgainPage = PlayAgainScreen()
			playAgainPage.display(screen)


class MovingObstacles(Rect):
	def __init__(self):
		self.trainImage = image.load("train.png")
		self.trainImage = transform.scale(self.trainImage, (200,100))
		self.hurdleImage = image.load("hurdle.png")
		self.hurdleImage = transform.scale(self.hurdleImage, (200,500))
		self.trains = []
		self.hurdles = []
		self.dy = 3 # how fast the obstacles move
		
	def create_trains(self, screen):
		y = 0 # obstacles will appear from the top of the screen
		while len(self.trains) < 6:
			self.trains.append(Rect(40,y,50,100)) # trains appearing on the left side
			self.trains.append(Rect(100,y,50,100)) # train appearing in the middle
			self.trains.append(Rect(300,y,50,100)) # train appearing on the right side
			y += 500
		return self.trains
		
	def create_hurdles(self, screen): 
		y = 0
		while len(self.hurdles) < 3:
			self.hurdles.append(Rect(40,y,80,70)) # hurdles appearing on the left side
			self.hurdles.append(Rect(100,y,80,70)) # hurdles appearing in the middle
			self.hurdles.append(Rect(300,y,80,70)) # hurdles appearing on the right side
			y += 800
		return self.hurdles

	def draw_trains(self, screen): 
		for i in self.trains:
			screen.blit(self.trainImage, i)
		
	def draw_hurdles(self, screen):
		for j in self.hurdles:
			screen.blit(self.hurdleImage, j)
			
	def movingObs(self):
		for i in self.trains:
			i.move_ip(0,self.dy)
			screen.blit(self.trainImage,i)
		
		for j in self.hurdles:
			j.move_ip(0,self.dy)
			screen.blit(self.hurdleImage,j)
	
	def checkCollision(self,character): # when the character collides with obstacles, play-again screen appears
		for i in self.trains:
			if character.colliderect(i):
				return True
			
		for j in self.hurdles:
			if character.colliderect(j):
				return True
		
		return False
		
	def removeObs(self):
		for i in self.trains:
			if i.y >= height:
				self.trains.remove(i)
				self.trains.append(Rect(40,0,50,100))
				self.trains.append(Rect(100,0,50,100))
				self.trains.append(Rect(300,0,50,100))
				
		for j in self.hurdles:
			if j.y <= 0:
				self.hurdles.remove(j)
				self.hurdles.append(Rect(40,100,80,70))
				self.hurdles.append(Rect(100,100,80,70))
				self.hurdles.append(Rect(300,100,80,70))


class Character(Rect):
	def __init__(self):
		super().__init__(188,700,87,114)# position of where the character spawns and its width and height
		self.characterImage = image.load("jake running.png")
		self.characterImage = transform.scale(self.characterImage, (87,114)) #width and height of character
		
	def display(screen):
		screen.blit(self.characterImage, (0,0))

currentScreen = HomeScreen()


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
