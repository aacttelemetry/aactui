import pygame
import cmath
import random
import math

x1 = 5
y1 = 5
x2 = 5
y2 = 10


def deg0():
	global x1
	global x2
	for x in range(10):
		x2 -= 5
	

#30deg = 
#60deg = 
def deg90():
	global y2
	for x in range(10):
		y2 += 5
def deg120():
	global x1
	global y1
	global y2
	global x2
	for x in range(22):
		x2 += 2.5
		y2 += 4.33
#150deg = 
def deg180():
	global x2
	for x in range(11):
		x2 += 5
#210deg = 
#240deg = 
def deg270():
	global y2
	for x in range(29):
		y2 -= 5 
#300deg = 
#330deg = 
#360deg = 


xDistance = (abs(x1 - x2))
yDistance = (abs(y1 - y2))
#x2Distance = (abs(x2 - x3))
#y2Distance = (abs(y2 - y3))

def findPytha(a,b):
	x = cmath.sqrt(((a**2) + (b**2)))
	return x

curX = 0
curY = 0


pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

gameDisplay = pygame.display.set_mode((400, 300))
pygame.display.set_caption('Room')

counter = 0

drawings = []
drawing = [(10, 10), (20, 20)]
drawings.append(drawing)
drawings.append(((45,40),(50,50)))


gameExit = False

while not gameExit:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			gameExit = True

	print(drawings)
	gameDisplay.fill(white)
	pygame.draw.aalines(gameDisplay, black, True, drawings[0])	
	pygame.draw.aalines(gameDisplay, black, True, drawings[1])
	#if counter == 2:
		#deg120()
		#start.append(drawing)
	#pygame.draw.aalines(gameDisplay, black, True, start[1])
	#if counter == 3:
		#deg90()
		#start.append(drawing)
	#pygame.draw.aalines(gameDisplay, black, True, start[])
	pygame.display.update()

	
	




pygame.quit()
quit()
