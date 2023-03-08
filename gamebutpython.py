from pygame import * 

import random 

init()

width = 450
height = 800
screen = display.set_mode((width,height))
final_score = 0
display.set_caption("Subway Surfers")
homeScreenImage = image.load("homeScreen.jpg")
homeScreenImage = transform.scale(homeScreenImage, (width,height))


class Button(Rect):
	def __init__(self,x,y,buttonWidth,buttonHeight):
		self.x = x
		self.y = y
		self.buttonWidth = buttonWidth
		self.buttonHeight = buttonHeight
		super().__init__(x,y,buttonWidth,buttonHeight) # sets position and dimensions of the button
		
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
		self.nextScreen = self
		
	def display(self,screen): # displays homescreen
		screen.blit(homeScreenImage, (0,0))
		
	def handleClick(self): # checks the click
		pos = mouse.get_pos()
		self.playButton.checkClicked(pos)
		return self.nextScreen
		
	def playClick(self): # changes homescreen to game screen when play button is clicked
		self.nextScreen = GameScreen() 
	
	def handleKey(self, key):
		pass
		
	def update(self):
		return self.nextScreen


class PlayAgainScreen():
	def __init__(self):
		self.playAgainScreenImage = image.load("play again screen.png")
		self.playAgainScreenImage = transform.scale(self.playAgainScreenImage, (width,height))
		self.playAgainButton = Button(182,652,151,60)
		self.homeButton = Button(22,652,137,60)
		self.nextScreen = self
		self.playAgainButton.setCallBack(self.playAgain) # starts game when play-again button is clicked
		self.homeButton.setCallBack(self.homeAgain) # returns to home screen
		#self.score = 0
	
	def playAgain(self):
		self.nextScreen = GameScreen()
		
	def homeAgain(self):
		self.nextScreen = HomeScreen()
		
	def display(self,screen): # displays play-again screen
		global final_score
		screen.blit(self.playAgainScreenImage, (0,0))
		score_img = font.render(str(final_score), True, (148,102,164))
		screen.blit(score_img, (320,293))
		
	def handleClick(self):
		pos = mouse.get_pos()
		if self.playAgainButton.checkClicked(pos):
			print("play again")
			
		if self.homeButton.checkClicked(pos):
			print("home screen")
			
		return self.nextScreen
			
	def playClick(self):
		self.nextScreen = GameScreen()
		
	def handleKey(self, key):
		pass
		
	def update(self):
		return self.nextScreen

font = font.SysFont('freesansbold.ttf', 28)

class GameScreen():
	def __init__(self):
		self.gameScreenImage = image.load("game screen.jpg")
		self.gameScreenImage = transform.scale(self.gameScreenImage, (width,height))
		self.character = Character() # creating the character
		self.moveObs = MovingObstacles() # creating obstacles
		self.x2Multiplier = PowerUps() # creating multipliers
		self.moveObs.create_trains(screen)
		self.moveObs.create_hurdles(screen)
		self.x2Multiplier.create_multipliers(screen)
		self.score = 0
		self.nextScreen = self
		
	def display(self, screen): # displays everything needed
		screen.blit(self.gameScreenImage, (0,0))
		self.character.display(screen)
		self.moveObs.draw_trains(screen)
		self.moveObs.draw_hurdles(screen)
		self.x2Multiplier.draw_multipliers(screen)
		score_img = font.render("Score: " + str(self.score), True, (255,255,255))
		screen.blit(score_img, (20,20))

	def handleClick(self):
		pass
	
	def handleKey(self, key):
		if key == K_LEFT:
			self.character.handleMove(-125) # 125 is the number of pixels the character moves by 
		if key == K_RIGHT:
			self.character.handleMove(125)
	
	def update(self): # moves everything
		global final_score
		self.moveObs.removeObs()
		self.moveObs.movingObs()
		self.handleKey(key) # ensures keys are pressed 
		
		# checks obstacle collisions
		if self.moveObs.checkCollision(self.character):
			final_score = self.score
			self.nextScreen = PlayAgainScreen() # when the character collides with the obstacles, the play-again screen appears
			
		else:
			self.score += 1 # when character dodges obstacle, +1 point
			
		if self.x2Multiplier.checkCollision(self.character):
			self.score = self.score * 2
		
		return self.nextScreen


class MovingObstacles(Rect):
	def __init__(self):
		self.trainImage = image.load("train.png")
		self.trainImage = transform.scale(self.trainImage, (70,220))
		self.hurdleImage = image.load("hurdle.png")
		self.hurdleImage = transform.scale(self.hurdleImage, (80,80))
		self.trains = []
		self.hurdles = []
		self.dy = 3 # how fast the obstacles move
		self.character = Character()
		
	def create_trains(self, screen):
		y = 0 # obstacles will appear from the top of the screen 
		while len(self.trains) < 3:
			self.trains.append(Rect(70,y - random.randint(0, 500),70,220)) # trains appearing on the left
			self.trains.append(Rect(185,y - random.randint(0, 500),70,220)) # train appearing in the middle
			self.trains.append(Rect(300,y - random.randint(0, 500),70,220)) # train appearing on the right
		return self.trains
		
	def create_hurdles(self, screen): 
		y = -random.randint(0,500)
		while len(self.hurdles) < 2:
			self.hurdles.append(Rect(70,y - random.randint(0, 500),80,80)) # hurdles appearing on the left
			self.hurdles.append(Rect(190,y - random.randint(0, 500),80,80)) # hurdles appearing in the middle
			self.hurdles.append(Rect(300,y - random.randint(0, 500),80,80)) # hurdles appearing on the right
			y += random.randint(800,2000)
		return self.hurdles

	def draw_trains(self, screen): 
		for i in self.trains:
			#draw.rect(screen,(255,0,0),i)
			screen.blit(self.trainImage, i)
		
	def draw_hurdles(self, screen):
		for j in self.hurdles:
			#draw.rect(screen,(255,0,0),j)
			screen.blit(self.hurdleImage, j)
			
	def movingObs(self):
		for i in self.trains:
			i.move_ip(0,self.dy)
			screen.blit(self.trainImage,i)
		
		for j in self.hurdles:
			j.move_ip(0,self.dy)
			screen.blit(self.hurdleImage,j)
	
	def checkCollision(self, character): # when the character collides with obstacles, play-again screen appears
		for i in self.trains:
			if self.character.colliderect(i):
				print("Collision wth train") # checking collision 
				return True
			
		for j in self.hurdles:
			if self.character.colliderect(j):
				print("Collision with hurdles")
				return True
		
		return False
		
	def removeObs(self):
		for i in self.trains:
			if i.y >= height:
				self.trains.remove(i)
				y = 0 # obstacles will appear from the top of the screen
				if len(self.trains) <= 3:
					self.trains.append(Rect(i.x,y - random.randint(0, 500),100,200)) # trains appearing on the left side
				
				
		for j in self.hurdles:
			if j.y >= height:
				self.hurdles.remove(j)
				y = 0
				if len(self.hurdles) <= 2:
					self.hurdles.append(Rect(j.x,y - random.randint(0,500),80,70))


class PowerUps(Rect):
	def __init__(self):
		self.multiplierImage = image.load("multiplier.png")
		self.multiplierImage = transform.scale(self.multiplierImage, (50,50))
		self.multipliers = []
		self.dy = 3
		self.character = Character()
		
	def create_multipliers(self, screen):
		y = 0 # multipliers will appear from the top of the screen 
		while len(self.multipliers) < 3:
			self.multipliers.append(Rect(50,y - random.randint(0, 500),50,50)) # appearing on the left
			self.multipliers.append(Rect(130,y - random.randint(0, 500),50,50)) # appearing in the middle
			self.multipliers.append(Rect(260,y - random.randint(0, 500),50,50)) # appearing on the right
			y += random.randint(800,2000)
		return self.multipliers
		
	def draw_multipliers(self, screen): 
		for k in self.multipliers:
			screen.blit(self.multiplierImage, k)
			
	def moveMultipliers(self):
		for k in self.multipliers:
			k.move_ip(0,self.dy)
			screen.blit(self.multiplierImage,k)
			
	def checkCollision(self, character): # play-again screen appears
		for i in self.multipliers:
			if self.character.colliderect(i):
				print("Collision wth multipliers") # checking collision 
				return True
		return False
		
	def removeMultipliers(self):
		for k in self.multipliers:
			if k.y >= height:
				self.multipliers.remove(k)
				y = 0 # multipliers appear from top of screen
				if len(self.multipliers) <= 3:
					self.multipliers.append(Rect(k.x,y - random.randint(0, 500),50,50))
				


class Character(Rect):
	def __init__(self):
		super().__init__(188,700,87,114) # position of where the character spawns and its width and height
		self.characterImage = image.load("jake running.png")
		self.characterImage = transform.scale(self.characterImage, (87,114)) #width and height of character
		self.x = 190
		
	def display(self,screen):
		screen.blit(self.characterImage, (self.x,650))
		
	def handleMove(self, offset): 
		self.x += offset
		
	def handleClick(self):
		pass
		
	def handleKey(self, key):
		pass
		
	def update(self):
		pass


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
	currentScreen = currentScreen.update()
	currentScreen.display(screen)
		
	display.flip()
	time.delay(10)
