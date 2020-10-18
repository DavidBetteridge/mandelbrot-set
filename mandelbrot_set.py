import sys, pygame, colorsys
from math import e, log, log2, pi
import multiprocessing as mp
from multiprocessing import Pool

MAX_ITER = 50

black = 0, 0, 0

def inMandelbrot(c):
    z=0
    x=0
    while abs(z)<2 and x<MAX_ITER:
        x+=1
        z=z*z+c
   
    if x == MAX_ITER:
            return MAX_ITER
    
    return x + 1 - log(log2(abs(z)))

    
def colourForIteration(iterationNumber):
    hue = int(360 * iterationNumber / MAX_ITER)
    saturation = 100
    value = 100 if iterationNumber < MAX_ITER else 0

    c = pygame.Color(0,0,0)
    c.hsva = (hue, saturation, value, 0)

    return c

def plotrow(rowNumber, size, stepSize, zoomLevel, offset, rotation):
    (width, height) = size
    (xStep, yStep) = stepSize
    (xOffset, yOffset) = offset
    imaginaryNumber = ((1/height) * rowNumber * 2) -1
    imaginaryNumber = (imaginaryNumber + yOffset) * (1/zoomLevel)
    pixels = []
    for columnNumber in range(0,width,xStep):
        realNumber = (((1/width) * columnNumber *3.5)-2.5 + xOffset)* (1/zoomLevel)
        iterationNumber=inMandelbrot( rotation * complex(realNumber,imaginaryNumber))
        colour = colourForIteration(iterationNumber)
        pixels.append((colour,columnNumber,rowNumber))
        
    return pixels

def draw(screen, size, zoomLevel, stepSize, offset, rotation):
    (xStep, yStep) = stepSize
    (width, height) = size
    
    r = e ** (complex(0,rotation * (pi/180)))

    # screen.fill(black)

    # if xStep == 1:
    with Pool(processes=mp.cpu_count()) as pool:
        rows = pool.starmap(plotrow, [(rowNumber, size, stepSize, zoomLevel, offset, r) for rowNumber in range(0, height, yStep)])
        for row in rows:
            for (colour,columnNumber,rowNumber) in row:
                pygame.draw.rect(screen, colour, (columnNumber,rowNumber,xStep,yStep))        
    # else:
    #     for rowNumber in range(0, height, yStep):
    #         results = plotrow(rowNumber, size, stepSize, zoomLevel, offset, r)
    #         for (colour,columnNumber,rowNumber) in results:
    #             pygame.draw.rect(screen, colour, (columnNumber,rowNumber,xStep,yStep))

    pygame.display.flip()

def main():
    pygame.init()

    zoomLevel = 1
    size = width, height = 1500, 1000
    screen = pygame.display.set_mode(size)
    stepSize = xStep, yStep = 10,10
    offset = xOffset, yOffset = 0.0, 0.0
    rotation = 0

    draw(screen, size, zoomLevel, stepSize, offset, rotation)

    while (True):
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                if event.unicode == "+":
                    zoomLevel+=1
                    stepSize = xStep, yStep = 10, 10
                    draw(screen, size,zoomLevel, stepSize, offset, rotation)

                if event.unicode == "-":
                    if zoomLevel > 1:
                        zoomLevel-=1
                        stepSize = xStep, yStep = 10, 10
                        draw(screen, size,zoomLevel, stepSize, offset, rotation)

                if event.unicode == "h":
                    stepSize = xStep, yStep = 1, 1
                    draw(screen, size, zoomLevel, stepSize, offset, rotation)

                if event.key == pygame.K_LEFT: 
                    (xOffset, yOffset) = offset
                    offset = (xOffset - .1, yOffset)
                    draw(screen, size,zoomLevel, stepSize, offset, rotation)

                if event.key == pygame.K_RIGHT:  
                    (xOffset, yOffset) = offset
                    offset = (xOffset + .1, yOffset)
                    draw(screen, size,zoomLevel, stepSize, offset, rotation)

                if event.key == pygame.K_UP: 
                    (xOffset, yOffset) = offset
                    offset = (xOffset, yOffset - .1)
                    draw(screen, size,zoomLevel, stepSize, offset, rotation)

                if event.key == pygame.K_DOWN: 
                    (xOffset, yOffset) = offset
                    offset = (xOffset, yOffset + .1)
                    draw(screen, size,zoomLevel, stepSize, offset, rotation)

                if event.unicode == "c":
                    rotation -= 10 % 360    
                    draw(screen, size,zoomLevel, stepSize, offset, rotation)

                if event.unicode == "u":
                    rotation += 10 % 360    
                    draw(screen, size,zoomLevel, stepSize, offset, rotation)

            if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()

if __name__ == '__main__':
    main()