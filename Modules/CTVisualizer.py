## Import Statements
import pygame
import random
from tkinter import *
from enum import Enum
from ct_algorithms import BubbleSort
from ct_algorithms import QuickSort

pygame.init()

## Class Definitions

# SwFsm class
class SwFsm(Enum):
        BASE = 1
        MENU = 2
        SORT = 3

# Bin class
class Bin:

    def __init__(self, val, color):
        self.val = val
        self.color = color

# DrawInfo class
class DrawInfo:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    BLUE = 0, 0, 255
    BG_COLOR = WHITE
    PADDING = 100           # Number of pixels to pad on each side of the visualizer
    HEIGHT_PAD = 50         # Number of pixels to pad from the top to make room for title and other menu items
    GRADIENT = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)
    ]

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height
        self.setLst(lst.copy())

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualizer")

    def setLst(self, lst):
        self.lst = []
        for i in range(len(lst)):
            self.lst.append(Bin(lst[i], self.GRADIENT[i%3]))
        self.maxVal = max(lst)
        self.minVal = min(lst)

        self.blockWidth = round((self.width - self.PADDING)/len(lst))
        self.blockHeight = round((self.height - self.HEIGHT_PAD)/(self.maxVal - self.minVal))

        self.startX = self.PADDING / 2

    def draw(self):
        self.window.fill(self.BG_COLOR)

        # Draw List in it's current state
        for i, val in enumerate(self.lst):
            x = self.startX + i*self.blockWidth
            y = self.height - (val.val-self.minVal)*self.blockHeight
            pygame.draw.rect(self.window, val.color, (x, y, self.blockWidth, (val.val - self.minVal)*self.blockHeight))

        # Update window
        pygame.display.update()

def generateStartingSeq(n = 10, minVal = 1, maxVal = 10) -> list:
    lst = []

    for i in range(n):
        lst.append(round(random.random()*(maxVal - minVal) + minVal))

    return lst

def main():
    # Setting default values
    n = 20
    mn = 1
    mx = 30
    run = True
    clock = pygame.time.Clock()

    drawInfo = DrawInfo(800, 600, lst = generateStartingSeq(n, mn, mx))

    visState = SwFsm.BASE
    visNextState = SwFSM.BASE

    while run:
        clock.tick(60)

        # This is where the drawing functions will go
        drawInfo.draw()

        if visState == SwFsm.BASE:
            # Waiting for inputs. Nothing to do. Maybe throw in an idle animation if I have the time.
            pass

        elif visState == SwFsm.MENU:
            ## Do Menu things
            # Create Menu and wait for it to exit

            # Modify drawInfo parameters when it is done
            pass

        elif visState == SwFsm.SORT:
            # Sort
            # Update cosmetics to show the compared item and the pivot item

            # Check if the sort is complete; set flag if it is
        else:
            # FSM is broken
            run = False

        pygame.display.update()

        # Event Handler / Next State\
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                # State machine
                if visState == SwFsm.BASE:
                    if event.key == pygame.locals.K_ESCAPE:
                        # Quit State
                        run = False
                    elif event.key == pygame.locals.K_r:
                        ## Reset state
                        # Set a new list variable
                        drawInfo.setLst(generateStartingSeq(n,mn,mx))
                        visNextState = SwFsm.BASE
                    elif event.key == pygame.locals.K_m:
                        # Menu State
                        visNextState = SwFsm.MENU
                    elif event.key == pygame.locals.K_s:
                        # Sort State

                elif visState == SwFsm.MENU:
                    # Do Menu things
                    visNextState = SwFsm.SwFsm.BASE

                elif visState == SwFsm.SORT:
                    if event.key == pygame.locals.K_ESCAPE:
                        # Quit State
                        run = False
                    elif event.key == pygame.locals.K_r:
                        ## Reset state
                        # Set a new list variable
                        drawInfo.setLst(generateStartingSeq(n,mn,mx))
                        visNextState = SwFsm.BASE
                else:
                    # FSM is broken
                    run = False
        visState = visNextState
    pygame.quit()

if __name__ == '__main__':
    main()
