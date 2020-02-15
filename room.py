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

gameExit = False

while not gameExit:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			gameExit = True
	counter += 1
	drawing = ((x1, y1), (x2, y2))
	if counter == 10:
		deg90()
		drawings.append(drawing)
	gameDisplay.fill(white)
	if counter >= 10:
		pygame.draw.aalines(gameDisplay, black, True, drawings[0])
	if counter == 20:
		deg120()
		drawings.append(drawing)
	if counter >= 20:	
		pygame.draw.aalines(gameDisplay, black, True, drawings[1])
	if counter == 30:
		deg180()
		drawings.append(drawing)
	if counter >= 40:
		pygame.draw.aalines(gameDisplay, black, True, drawings[2])
	if counter == 50:
		deg90()
		drawings.append(drawing)
	if counter >= 50:
		pygame.draw.aalines(gameDisplay, black, True, drawings[3])
	print(drawings)
	pygame.display.update()

	
	




pygame.quit()
quit()
