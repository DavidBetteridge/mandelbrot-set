import sys, pygame, colorsys
from math import e, log, log2, pi
import multiprocessing as mp
from multiprocessing import Pool
from dataclasses import dataclass

@dataclass
class Parameters:
    width: int
    height: int
    zoomLevel: int
    rotation: int
    xStep: int
    yStep: int
    xOffset: int
    yOffset: int

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

def plotrow(rowNumber, parameters, rotation):
    imaginaryNumber = ((1/parameters.height) * rowNumber * 2) -1
    imaginaryNumber = (imaginaryNumber + parameters.yOffset) * (1/parameters.zoomLevel)
    pixels = []
    for columnNumber in range(0,parameters.width,parameters.xStep):
        realNumber = (((1/parameters.width) * columnNumber *3.5)-2.5 + parameters.xOffset)* (1/parameters.zoomLevel)
        iterationNumber=inMandelbrot( rotation * complex(realNumber,imaginaryNumber))
        colour = colourForIteration(iterationNumber)
        pixels.append((colour,columnNumber,rowNumber))
        
    return pixels

def draw(screen, parameters):
   
    r = e ** (complex(0,parameters.rotation * (pi/180)))

    with Pool(processes=mp.cpu_count()) as pool:
        rows = pool.starmap(plotrow, [(rowNumber, parameters, r) for rowNumber in range(0, parameters.height, parameters.yStep)])
        for row in rows:
            for (colour,columnNumber,rowNumber) in row:
                pygame.draw.rect(screen, colour, (columnNumber,rowNumber,parameters.xStep,parameters.yStep))        

    pygame.display.flip()

def useLowQuality(parameters):
    parameters.xStep = 10
    parameters.yStep = 10
    return parameters

def useHighQuality(parameters):
    parameters.xStep = 1
    parameters.yStep = 1
    return parameters

def main():
    pygame.init()

    size = width, height = 1500, 1000
    screen = pygame.display.set_mode(size)

    parameters = Parameters(width = width, height = height, zoomLevel = 1, rotation = 0, xStep=10, yStep=10, xOffset=0, yOffset=0)
    parameters = useLowQuality(parameters)

    draw(screen, parameters)

    while (True):
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                if event.unicode == "+":
                    parameters.zoomLevel+=1
                    parameters = useLowQuality(parameters)
                    draw(screen, parameters)

                if event.unicode == "-":
                    if parameters.zoomLevel > 1:
                        parameters.zoomLevel-=1
                        parameters = useLowQuality(parameters)
                        draw(screen, parameters)

                if event.unicode == "h":
                    parameters = useHighQuality(parameters)
                    draw(screen, parameters)

                if event.key == pygame.K_LEFT: 
                    parameters.xOffset -= .1
                    draw(screen, parameters)

                if event.key == pygame.K_RIGHT:  
                    parameters.xOffset += .1
                    draw(screen, parameters)

                if event.key == pygame.K_UP: 
                    parameters.yOffset -= .1
                    draw(screen, parameters)

                if event.key == pygame.K_DOWN: 
                    parameters.yOffset += .1
                    draw(screen, parameters)

                if event.unicode == "c":
                    parameters.rotation -= 10 % 360    
                    draw(screen, parameters)

                if event.unicode == "u":
                    parameters.rotation += 10 % 360    
                    draw(screen, parameters)

            if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()

if __name__ == '__main__':
    main()