## Import Statements
import pygame
import random
from tkinter import *
from enum import Enum
from Vis_Sort import BubbleSort, QuickSort

pygame.init()

MAX_SIZE = 500
SORTS = ['Bubble Sort', 'Quick Sort']
SIZE = 20
SORT = 'Quick Sort'
ASC = True

## Function Definitions
def getMenuVals():
    global SIZE, SORT, ASC
    menu = Tk()
    menuAsc = IntVar()
    menuSize = IntVar()
    menuSort = StringVar()

    def setVals():
        global SIZE, ASC, SORT
        SIZE = menuSize.get()
        ASC = (menuAsc.get() == 1)
        SORT = menuSort.get()
        menu.destroy()

    def resetVals():
        menuSort.set(SORT)
        menuAsc.set(1 if ASC else 0)
        scSize.set(SIZE)

    ## Create widgets
    menu.geometry("400x200")
    frame1 = Frame(menu, height=100, width=400)
    frame1.pack(side=TOP)

    menuSortR1 = Radiobutton(frame1, text='Bubble Sort', variable=menuSort, value='Bubble Sort')
    menuSortR2 = Radiobutton(frame1, text='Quick Sort', variable=menuSort, value='Quick Sort')
    menuSortR1.grid(row=1, column=1)
    menuSortR2.grid(row=1, column=2)
    menuSort.set(SORT)

    menuAscR1 = Radiobutton(frame1, text='Ascending', variable=menuAsc, value=1)
    menuAscR2 = Radiobutton(frame1, text='Descending', variable=menuAsc, value=0)
    menuAscR1.grid(row=2, column=1)
    menuAscR2.grid(row=2, column=2)

    frame3 = Frame(menu, height=50, width=400)
    frame3.pack(side=BOTTOM)

    btnSubmit = Button(frame3, text='Submit', width=10, command=setVals)
    btnSubmit.grid(row=2, column=1)

    btnCancel = Button(frame3, text='Quit', width=10, command=menu.destroy)
    btnCancel.grid(row=2, column=2)

    btnReset  = Button(frame3, text='Reset', width=10, command=resetVals)
    btnReset.grid(row=2, column=3)

    frame2 = Frame(menu, height=50, width=400)
    frame2.pack(side=BOTTOM)

    scSize = Scale(frame2, variable=menuSize, from_=6, to=MAX_SIZE, length=300, orient=HORIZONTAL)
    scSize.pack(anchor=W)

    menu.mainloop()

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
        self.lst = lst.copy()
        #for i in range(len(lst)):
            #self.lst.append(Bin(lst[i], self.GRADIENT[i%3]))
        self.maxVal = max(lst)
        self.minVal = min(lst)

        #self.blockWidth = round((self.width - self.PADDING)/len(lst))
        self.blockWidth = (self.width - self.PADDING)/len(lst)
        self.blockHeight = round((self.height - self.HEIGHT_PAD)/(self.maxVal - self.minVal + 1))

        self.startX = self.PADDING / 2

    def draw(self):
        self.window.fill(self.BG_COLOR)

        # Draw List in it's current state
        for i, val in enumerate(self.lst):
            x = self.startX + i*self.blockWidth
            y = self.height - (val-self.minVal + 1)*self.blockHeight
            pygame.draw.rect(self.window, self.GRADIENT[i%3], (x, y, self.blockWidth, (val - self.minVal + 1)*self.blockHeight))

        # Update window
        pygame.display.update()

def generateStartingSeq(n = 10, minVal = 1, maxVal = 10) -> list:
    lst = []

    for i in range(n):
        lst.append(round(random.random()*(maxVal - minVal) + minVal))

    return lst

def main():
    global SORT, SIZE, ASC
    # Setting default values
    mn = 1
    mx = 30
    run = True
    clock = pygame.time.Clock()

    drawInfo = DrawInfo(800, 600, lst = generateStartingSeq(SIZE, mn, mx))

    visState = SwFsm.BASE
    visNextState = SwFsm.BASE

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
            getMenuVals()

            # Modify drawInfo parameters when it is done
            drawInfo.setLst(generateStartingSeq(SIZE, mn, mx))
            visNextState = SwFsm.BASE

        elif visState == SwFsm.SORT:
            # Sort
            # Update cosmetics to show the compared item and the pivot item
            pass
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
                    if event.key == pygame.K_ESCAPE:
                        # Quit State
                        run = False
                    elif event.key == pygame.K_r:
                        ## Reset state
                        # Set a new list variable
                        drawInfo.setLst(generateStartingSeq(SIZE,mn,mx))
                        visNextState = SwFsm.BASE
                    elif event.key == pygame.K_m:
                        # Menu State
                        visNextState = SwFsm.MENU
                    elif event.key == pygame.K_s:
                        # Sort State
                        pass
                elif visState == SwFsm.MENU:
                    # Do Menu things
                    visNextState = SwFsm.BASE

                elif visState == SwFsm.SORT:
                    if event.key == pygame.K_ESCAPE:
                        # Quit State
                        run = False
                    elif event.key == pygame.K_r:
                        ## Reset state
                        # Set a new list variable
                        drawInfo.setLst(generateStartingSeq(SIZE,mn,mx))
                        visNextState = SwFsm.BASE
                else:
                    # FSM is broken
                    run = False
        visState = visNextState
    pygame.quit()

if __name__ == '__main__':
    main()
