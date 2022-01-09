#!usr/bin/env python

import time
import math
import pygame
pygame.init()

windowHeight = 1000
windowWidth  = 1000

win = pygame.display.set_mode((windowHeight, windowHeight))
pygame.display.set_caption("Pathfinding / start by pressing 'spacebar'")

class Nodes:
    def __init__(self, x, y, previousNode):
        self.xpos = x
        self.ypos = y
        self.g = 0
        self.h = 0
        self.f = 0
        self.closed = False
        self.obsticle = False
        self.open = False
        self.neighbours = []
        self.previousNode = previousNode

    def drawSquare(self, color, thickness):
        pygame.draw.rect(win, color, (self.xpos * w, self.ypos * h, w, h), thickness)
        text_surface = font.render(str(round(self.f)), True, (255, 255, 255))
        win.blit(text_surface, dest = (self.xpos*w, self.ypos*h))
        pygame.display.update()

# Initializes surrounding blocks as neithgbours for the given block with x, y coords
def setNeighbours(x, y):
    for i in range(x - 1, x + 2):
        for z in range(y - 1, y + 2):

            if 40 > i >= 0 and 40 > z >= 0 :
                if i == x and z == y:
                    pass
                else:
                    grid[x][y].neighbours.append(grid[i][z])

    checkDiagonals(x, y)

# Remove diagonal neighbours blocked by two obsticles
def checkDiagonals(x, y):
    count = 0
    for i in grid[x][y].neighbours:
        if grid[x][y].xpos != i.xpos and grid[x][y].ypos != i.ypos:
            blocked = False
            for z in set(grid[x][y].neighbours) & set(i.neighbours):
                if z.obsticle == True:
                    if blocked == True:
                        del(grid[x][y].neighbours[int(count)])
                    blocked = True
        count = count + 1

def drawObsticles():
    while True:
        mx, my = pygame.mouse.get_pos()
        mousepos = grid[int(mx / w)][int(my / h)]

        # Add obsticles in 'block' if the nodes aren't the start or end ones and while the mouse button is down
        if mousepos.obsticle == False and mousepos != start and mousepos != end:
            mousepos.drawSquare(white, 0)
            grid[int(mx / w)][int(my / h)].obsticle = True

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                return
            if event.type == pygame.QUIT:
                run = False
                return

# Main solver
def solver():
    while len(openned) > 0:
        lowest = 0

        for i in range(len(openned)):
            if openned[i].f < openned[lowest].f:
                lowest = i
        #import pdb; pdb.set_trace()
        current = openned[lowest]
        openned[lowest].closed = True
        current.drawSquare((118, 255, 180), 0)
        generateNeighboursValues(current)

        if current == end:
            print("Finding path successful, the end point is {} blocks away from the start.".format(current.g / 10))
            while current != start:
                current.drawSquare(blue, 0)
                current = current.previousNode
            return

        del openned[lowest]
    print('No possible path.')

visited = []

font = pygame.font.Font(pygame.font.get_default_font(), 13)

# Set values g, h and f for neighbouring values
def generateNeighboursValues(parent):
    neighbour = parent.neighbours
    for i in range(len(neighbour)):
        if neighbour[i].closed == False and neighbour[i].obsticle == False:

            if neighbour[i].g != 0 or neighbour[i] == start:
                if neighbour[i].g > parent.g + 10:
                    neighbour[i].previousNode = parent
                    neighbour[i].g = parent.g + 10
            else:
                neighbour[i].previousNode = parent
                neighbour[i].openned = True
                neighbour[i].g = parent.g + 10
                openned.append(neighbour[i])

            neighbour[i].h = heuristics(neighbour[i], end)
            neighbour[i].f = neighbour[i].g + neighbour[i].h
            if neighbour[i] != end:
                neighbour[i].drawSquare(red, 0)

# Calcuate distance between a and b
def heuristics(a, b):
    try:
        h = (max(abs(a.xpos - b.xpos), abs(a.ypos - b.ypos)))*10
    except ValueError:
        h = 0
    return h

rows = 40
cols = 40

w = windowWidth / rows
h = windowHeight / cols

openned = []
block  = []

red = (255, 0, 0)
black = (0, 0, 0)
blue = (0, 0, 255)
green = (118, 255, 0)
white = (255, 255, 255)

# Build the grid
grid = [['' for i in range(rows)] for i in range(cols)]

# Initialize nodes, draw squares
for i in range(rows):
    for z in range(cols):
        grid[i][z] = Nodes(i, z, 0)
        grid[i][z].drawSquare(red, 1)

locked = '1'

run = True
while run:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN and locked == '3':
            if event.key == pygame.K_SPACE:
                 # Set neighbouring notes for each node in the grid and run the solver
                [[[setNeighbours(i, z)] for z in range(cols)] for i in range(rows)]
                solver()

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            if locked == '1':
                grid[int(x / w)][int(y / h)].drawSquare(green, 0)
                start = grid[int(x / w)][int(y / h)]
                openned.append(start)
                locked = '2'

            elif locked == '2':
                end = grid[int(x / w)][int(y / h)].drawSquare(blue, 0)
                end = grid[int(x / w)][int(y / h)]
                locked = '3'

            elif locked == '3':
                drawObsticles()


        pygame.display.update()
pygame.quit()

# if __name__ == '__main__':
#     main()
