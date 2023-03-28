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
		self.playAgainScreenImage = image.load("play again screen.png")
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
		self.gameScreenImage = image.load("game screen.jpg")
		self.gameScreenImage = transform.scale(self.gameScreenImage, (width,height))
		self.character = Character() # creating the character
		self.moveObs = MovingObstacles() # creating obstacles
		self.x2Multiplier = PowerUps() # creating multipliers
		self.coin = PowerUps() # creating coins
		self.moveObs.create_trains(screen)
		self.moveObs.create_hurdles(screen)
		self.x2Multiplier.create_multipliers(screen)
		self.coin.create_coins(screen)
		self.score = 0
		self.coins_collected = 0
		self.nextScreen = self
		
	def display(self, screen): # displays everything needed
		screen.blit(self.gameScreenImage, (0,0))
		self.character.display(screen)
		self.moveObs.draw_trains(screen)
		self.moveObs.draw_hurdles(screen)
		self.x2Multiplier.draw_multipliers(screen)
		self.coin.draw_coins(screen)
		score_img = font.render("Score: " + str(self.score), True, (255,255,255))
		screen.blit(score_img, (20,20))
		coin_img = font.render("Coins: " + str(self.coins_collected), True, (255,255,255))
		screen.blit(coin_img, (20,50))

	def handleClick(self):
		pass
	
	def handleKey(self, key):
		if key == K_LEFT:
			self.character.handleMove(-125) # 125 is the number of pixels the character moves by 
		if key == K_RIGHT:
			self.character.handleMove(125)
	
	def update(self): # moves everything
		global final_score # making these variables global so this method can access them
		global total_coins
		global time_elapsed
		global distance_between_obstacles
		self.moveObs.removeObs()
		self.moveObs.movingObs()
		self.x2Multiplier.removeMultipliers()
		self.x2Multiplier.moveMultipliers()
		self.coin.remove_coins()
		self.coin.move_coins()
		self.handleKey(key) # ensures keys are pressed 
		
		'''
		for train in self.moveObs.trains:
			for train2 in self.moveObs.trains:
				if (train.y - train2.y) < 250:
					print("error")
					# break
				else:
					print("not an error")
		'''
		
		# checks obstacle collisions
		if self.moveObs.checkCollision(self.character):
			final_score = self.score
			self.nextScreen = PlayAgainScreen() # when the character collides with the obstacles, the play-again screen appears
		else:
			self.score += 1 # when character dodges obstacle, +1 point
		
		# multiplier lasts for a set amount of time	
		if self.x2Multiplier.checkCollision(self.character):
				if time_elapsed / 3000 > 0: # multiplier lasts for 3 seconds
					self.score = self.score * 2 # x2 multiplier in effect; current score is multiplied by 2
		
		if self.coin.checkCollision(self.character):
			self.coins_collected = self.coins_collected + 1 # for every coin collected, the coin counter is incremented
			total_coins = self.coins_collected # play-again screen will display the number of coins collected from the game
		
		'''
		# creating an obstacle for the set distance
		for i in self.moveObs.trains:
			if i.y < (height - distance_between_obstacles) :
				self.moveObs.create_trains(screen)
		'''
		
		return self.nextScreen
		

class MovingObstacles(Rect):
	def __init__(self):
		self.trainImage = image.load("train.png")
		self.trainImage = transform.scale(self.trainImage, (70,220))
		self.hurdleImage = image.load("hurdle.png")
		self.hurdleImage = transform.scale(self.hurdleImage, (80,80))
		self.trains = []
		self.hurdles = []
		self.spaceBoxTrain = Rect(0,y - random.randint(0,1000),70,300) # collision boxes around trains
		self.spaceBoxHurdle = Rect(0,y - random.randint(0,1000),80,200) # collision boxes around 
		self.dy = 5 # how fast the obstacles move
		self.createNew = False # used for creating new obstacles
		self.count = 0
	
	def isFree(self, obj): # ensures objects do not overlap each other
		global distance_between_obstacles
		for t in self.trains + self.hurdles: 
			if obj.colliderect(t): return False
		return True
	
	def create_trains(self, screen):
		global distance_between_obstacles
		y = 0 # obstacles will appear from the top of the screen 
		while len(self.trains) < 3:
			t1 = Rect(70,y - random.randint(0,1000),70,220)
			t2 = Rect(185,y - random.randint(0,1000),70,220)
			t3 = Rect(300,y - random.randint(0,1000),70,220)
			
			while not self.isFree(t1): # while not free, do it again
				t1 = Rect(70,y - random.randint(0,1000),70,220)
			while not self.isFree(t2):
				t2 = Rect(185,y - random.randint(0,1000),70,220)
			while not self.isFree(t3):
				t3 = Rect(300,y - random.randint(0,1000),70,220)
				
			# checking if the space between the two trains is big enough to move	
			if (t2.bottom - t1.y) < 250:
				print("can't move")
			
			#for train in self.trains:
			#	print(train.y)
				
			self.trains.append(t1) # trains appearing on the left
			self.trains.append(t2) # train appearing in the middle
			self.trains.append(t3) # train appearing on the right
		return self.trains
		
	def create_hurdles(self, screen):
		global distance_between_obstacles
		y = 0 # -random.randint(0,1000)
		while len(self.hurdles) < 3:
			h1 = Rect(70,y - random.randint(2500,3000),80,80)
			h2 = Rect(190,y - random.randint(2000,2500),80,80)
			h3 = Rect(300,y - random.randint(1500,2000),80,80)
			
			while not self.isFree(h1):
				h1 = Rect(70,y - random.randint(0,3000),80,80)
			while not self.isFree(h2):
				h2 = Rect(190,y - random.randint(0,2500),80,80)
			while not self.isFree(h3):
				h3 = Rect(300,y - random.randint(0,3000),80,80)
				
				
			self.hurdles.append(h1) # hurdles appearing on the left
			self.hurdles.append(h2) # hurdles appearing in the middle
			self.hurdles.append(h3) # hurdles appearing on the right
			y += random.randint(800,2000)
		return self.hurdles

	def draw_trains(self, screen): 
		for i in self.trains:
			screen.blit(self.trainImage, i)
			draw.rect(screen, (255,0,0), i, 1)
		
	def draw_hurdles(self, screen):
		for j in self.hurdles:
			screen.blit(self.hurdleImage, j)
			draw.rect(screen, (255,0,0), j, 1)
			
	def movingObs(self): # making the obstacles move
		for i in self.trains:
			i.move_ip(0,self.dy)
			screen.blit(self.trainImage,i)
		
		for j in self.hurdles:
			j.move_ip(0,self.dy)
			screen.blit(self.hurdleImage,j)
		
		# need to create?
		
		y = 0 # obstacles will appear from the top of the screen
		if self.createNew:
			self.count += 1
		
		if self.createNew and self.count > 100: # if self.count is over 100fps
			if len(self.trains) <= 3:
					self.trains.append(Rect(i.x,y - random.randint(0,500),70,220))
			if len(self.hurdles) <= 2:
					self.hurdles.append(Rect(j.x,y - random.randint(0,500),80,80))
			self.createNew = False
			self.count = 0
			
	def checkCollision(self, character): # when the character collides with obstacles, play-again screen appears
		for i in self.trains:
			if character.colliderect(i):
				print("Collision with train") # checking collision 
				return True
			
		for j in self.hurdles:
			if character.colliderect(j):
				print("Collision with hurdles")
				return True
		
		return False
		
	# creating a space around the obstacles so that obstacles do not spawn on top of each other and the obstacles won't spawn in a line
	#def spaceCollision(self):
		
		
	def removeObs(self): # when the obstacles reach the end of the screen, they disappear
		for i in self.trains:
			if i.y >= height:
				self.trains.remove(i)
				y = 0 # obstacles will appear from the top of the screen
				self.createNew = True
				
		for j in self.hurdles:
			if j.y >= height:
				self.hurdles.remove(j)
				y = 0
				self.createNew = True


class PowerUps(Rect): # includes coins
	def __init__(self):
		self.multiplierImage = image.load("multiplier.png")
		self.multiplierImage = transform.scale(self.multiplierImage, (50,50))
		self.multipliers = []
		self.coinImage = image.load("coin.png")
		self.coinImage = transform.scale(self.coinImage, (30,30))
		self.coins = []
		self.dy = 5 # how fast the power-up and coins move
		self.createNew = False # used for creating new multipliers and coins
		self.count = 0
		
	def isFree(self, obj): # ensures objects do not overlap each other
		for m in self.multipliers + self.coins:
			if obj.colliderect(m): return False
		return True	
		
	def create_multipliers(self, screen):
		y = 0 # multipliers will appear from the top of the screen 
		while len(self.multipliers) < 3: 
			m1 = Rect(80,y - random.randint(0, 500),50,50)
			m2 = Rect(190,y - random.randint(0, 500),50,50)
			m3 = Rect(300,y - random.randint(0, 500),50,50)
			
			while not self.isFree(m1): # multipliers will not overlap each other
				m1 = Rect(80,y - random.randint(0, 500),50,50)
			while not self.isFree(m2):
				m2 = Rect(190,y - random.randint(0, 500),50,50)
			while not self.isFree(m3):
				m3 = Rect(300,y - random.randint(0, 500),50,50)
			
			self.multipliers.append(m1) # appearing on the left
			self.multipliers.append(m2) # appearing in the middle
			self.multipliers.append(m3) # appearing on the right
			y += random.randint(800,2000)
		return self.multipliers
		
	def create_coins(self, screen):
		y = 0 # coins will appear from the top of the screen 
		while len(self.coins) < 3:
			c1 = Rect(80,y - random.randint(0, 500),30,30)
			c2 = Rect(200,y - random.randint(0, 500),30,30)
			c3 = Rect(320,y - random.randint(0, 500),30,30)
			
			while not self.isFree(c1): # coins will not overlap each other
				c1 = Rect(80,y - random.randint(0, 500),30,30)
			while not self.isFree(c2):
				c2 = Rect(200,y - random.randint(0, 500),30,30)
			while not self.isFree(c3):
				c3 = Rect(320,y - random.randint(0, 500),30,30)
			
			self.coins.append(c1) # appearing on the left
			self.coins.append(c2) # appearing in the middle
			self.coins.append(c3) # appearing on the right
			y += random.randint(800,2000)
		return self.coins
		
	def draw_multipliers(self, screen): # displaying multipliers onto the screen
		for k in self.multipliers:
			screen.blit(self.multiplierImage, k)
			
	def draw_coins(self, screen): # displaying coins onto the screen
		for l in self.coins:
			screen.blit(self.coinImage, l)
			
	def moveMultipliers(self): # making the multipliers move 
		for k in self.multipliers:
			k.move_ip(0, self.dy)
			screen.blit(self.multiplierImage, k)
			
		y = 0
		if self.createNew:
			self.count += 1
			
		if self.createNew and self.count > 100: # if self.count is over 100fps
			if len(self.multipliers) <= 3:
					self.multipliers.append(Rect(k.x,y - random.randint(0,500),50,50))
			self.createNew = False
			self.count = 0
			
	def move_coins(self): # making the coins move
		for l in self.coins:
			l.move_ip(0, self.dy)
			screen.blit(self.coinImage, l)
			
		y = 0
		if self.createNew:
			self.count += 1
			
		if self.createNew and self.count > 100: # if self.count is over 100fps
			if len(self.coins) <= 3:
					self.coins.append(Rect(l.x,y - random.randint(0,500),30,30))
			self.createNew = False
			self.count = 0
			
	def checkCollision(self, character): # collision detection; does the character collect the item?
		for k in self.multipliers:
			if character.colliderect(k):
				print("Collision with multipliers") # checking collision
				self.multipliers.remove(k) # when character collides with multiplier, multiplier looks as if it has been collected 
				return True
				
		for l in self.coins:
			if character.colliderect(l):
				print("Collision with coins")
				self.coins.remove(l) # when character collides with coin, coin looks as if it has been collected
				return True
				
		return False
		
	def removeMultipliers(self):
		for k in self.multipliers:
			if k.y >= height: # when multipliers reach the end of the screen they disappear
				self.multipliers.remove(k) 
				y = 0 # multipliers appear from top of screen
				if len(self.multipliers) <= 3:
					self.multipliers.append(Rect(k.x,y - random.randint(0, 500),50,50))
				
	def remove_coins(self):
		for l in self.coins:
			if l.y >= height:
				self.coins.remove(l) # when coins reach the end of the screen they disappear
				y = 0 # coins appear from top of screen
				if len(self.coins) <= 3:
					self.coins.append(Rect(l.x,y - random.randint(0, 500),50,50))


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
