import time

from pygame import *

import random

init()

width = 450
height = 800
screen = display.set_mode((width,height))
final_score = 0
total_coins = 0
distance_between_obstacles = 250 # number of pixels between each obstacle
display.set_caption("Subway Surfers")
homeScreenImage = image.load("homeScreen.jpg")
homeScreenImage = transform.scale(homeScreenImage, (width,height))
clock = time.Clock() # creating a clock
time_elapsed = time.get_ticks() # returns the time in ms since pygame initialised

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
		self.playAgainScreenImage = image.load("play again screen.jpg")
		self.playAgainScreenImage = transform.scale(self.playAgainScreenImage, (width,height))
		self.playAgainButton = Button(182,652,151,60)
		self.homeButton = Button(22,652,137,60)
		self.nextScreen = self
		self.playAgainButton.setCallBack(self.playAgain) # starts game when play-again button is clicked
		self.homeButton.setCallBack(self.homeAgain) # returns to home screen

	def playAgain(self):
		self.nextScreen = GameScreen()

	def homeAgain(self):
		self.nextScreen = HomeScreen()

	def display(self,screen): # displays play-again screen
		global final_score
		global total_coins
		screen.blit(self.playAgainScreenImage, (0,0))
		score_img = font.render(str(final_score), True, (148,102,164))
		coin_img = font.render(str(total_coins), True, (255,255,255))
		screen.blit(score_img, (320,293))
		screen.blit(coin_img, (328,351))

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
		self.gameScreenImage = image.load("play again screen.jpg")
		self.gameScreenImage = transform.scale(self.gameScreenImage, (width,height))
		self.character = Character() # creating the character
		self.moveObs = obstacles() # creating obstacles
		self.score = 0
		self.nextScreen = self

	def display(self, screen): # displays everything needed
		screen.blit(self.gameScreenImage, (0,0))
		self.character.display(screen)
		#score_img = font.render("Score: " + str(self.score), True, (255,255,255))
		#screen.blit(score_img, (20,20))
		self.moveObs.draw_obstacles(screen)

	def handleClick(self):
		pass

	def handleKey(self, key):
		if key == K_LEFT:
			self.character.handleMove(-125) # 125 is the number of pixels the character moves by
		if key == K_RIGHT:
			self.character.handleMove(125)

	def update(self): # moves everything
		global final_score # making these variables global so this method can access them
		global time_elapsed
		self.moveObs.generateObstacles()
		self.moveObs.move_obs()
		self.moveObs.removeObs()

		self.handleKey(key) # ensures keys are pressed

		#######################DEBUG##########################

		#######################DEBUG##########################



		return self.nextScreen



class Character(Rect):
	def __init__(self):
		super().__init__(188,700,50,100) # position of where the character spawns and its width and height
		self.characterImage = image.load("jake running.png")
		self.characterImage = transform.scale(self.characterImage, (50,100)) #width and height of character
		self.x = 190

	def display(self,screen):
		screen.blit(self.characterImage, self)
		draw.rect(screen,(255,255,255), self,1)

	def handleMove(self, offset):
		self.x += offset

	def handleClick(self):
		pass

	def handleKey(self, key):
		pass

	def update(self):
		pass


class obstacles:
	def __init__(self):
		self.trainImage = image.load("train.png")
		self.trainImage = transform.scale(self.trainImage, (70,220))
		self.hurdleImage = image.load("hurdle.png")
		self.hurdleImage = transform.scale(self.hurdleImage, (80,80))
		# self.rowArr = [Rect(70,0,70,220) ,Rect(330,0,70,220)]
		# self.rowArr2 = [Rect(70,0,70,220) ,Rect(200,0,70,220)]
		self.fullArr = [[Rect(70,0,70,220), Rect(330,0,70,220)],     [Rect(70,0,70,220) ,Rect(200,0,70,220)],    [Rect(200,0,70,220) ,Rect(330,0,70,220)]]
		self.currentArr = []
		self.posArr = [70, 140, 210]

	def generateRandomIndex(self):
		randindex = random.randint(0, 2)
		return randindex
		print(self.randindex)

	def generateObstacles(self):
		while len(self.currentArr) < 1:
			self.currentArr.append(self.fullArr[random.randint(0,2)])

	#self.rowArr.append(Rect(70),0,70,220))

	def draw_obstacles(self, screen):
		for i in self.currentArr[0]:
			screen.blit(self.trainImage, i)
			draw.rect(screen, (255,0,0), i, 1)

	def move_obs(self):
		for i in self.currentArr[0]:
			i.move_ip(0, 5)
			screen.blit(self.trainImage, i)

	def removeObs(self):
		for i in self.currentArr[0]:
			if i.y >= height:
				self.currentArr.pop(0)
				self.currentArr.append(self.fullArr[random.randint(0,2)])
				i.y = -100







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
