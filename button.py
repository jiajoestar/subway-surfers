from pygame import *

# needed to set up pygame!
init()
# screen size
width = 1200
height = 700

#create the screen to draw to
screen = display.set_mode((width, height))

endProgram = False 


class Button(Rect):
	def __init__(self, x, y, text, colour):
		self.text = text
		self.colour = colour
		super().__init__(x,y,200,100)
		mainfont = font.SysFont("Comic Sans", 20)
		self.textImg = mainfont.render(text, True, (255,255,255))
		
	def draw(self, screen):
		draw.rect(screen, self.colour, self)
		screen.blit(self.textImg, (self.x, self.y))
		
	def checkClick(self, pos):
		if self.collidepoint(pos):
			self.callback()
		
	def setCallBack(self, callback):
		self.callback = callback
		
def startGame():
	print("start game")
	
def endGame():
	print("end game")
			
		
startButton = Button(20,20, "start", (255,192,203))
startButton.setCallBack(startGame)
quitButton = Button(250,20, "quit", (173,216,230))
quitButton.setCallBack(endGame)


while not endProgram: # pygame event loop 
	for e in event.get(): 
		if e.type == QUIT: 
			endProgram = True
		elif e.type == MOUSEBUTTONDOWN:
			pos = mouse.get_pos()
			startButton.checkClick(pos)
			quitButton.checkClick(pos)
        
	startButton.draw(screen)
	quitButton.draw(screen)

	display.update()
