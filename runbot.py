import cv2
import time
import numpy as np
import math
from PIL import ImageGrab
from matplotlib import pyplot as plt
from pymouse import PyMouse

clickDelay = 1/4

board = [
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
]

m = PyMouse()

blue = cv2.imread('templates/blue.PNG',0)
green = cv2.imread('templates/green.PNG',0)
orange = cv2.imread('templates/orange.PNG',0)
purple = cv2.imread('templates/purple.PNG',0)
red = cv2.imread('templates/red.PNG',0)
white = cv2.imread('templates/white.PNG',0)
yellow = cv2.imread('templates/yellow.PNG',0)

gems = [
["b",blue],
["g",green],
["o",orange],
["p",purple],
["r",red],
["w",white],
["y",yellow]
]

def gridToClick(row,col):
    top = 668
    left = 194
    clickX = top + (col*73)
    clickY = left + (row*73)
    m.click(clickX+36,clickY+36)
    time.sleep(clickDelay)



def multiFind(template):
    w, h = template[1].shape[::-1]
    capture = ImageGrab.grab()
    capture = np.array(capture)
    cv_capture = capture.astype(np.uint8)
    cv_capture_grey = cv2.cvtColor(cv_capture, cv2.COLOR_RGB2GRAY)

    res = cv2.matchTemplate(cv_capture_grey,template[1],cv2.TM_CCOEFF_NORMED)
    threshold = .90
    loc = np.where( res >= threshold)
    matches = len(zip(*loc[::-1]))
    for pt in zip(*loc[::-1]):
        gridX = int(math.floor((pt[0]+(w/2)-668)/73))
        gridY = int(math.floor((pt[1]+(h/2)-194)/73))
        board[gridY][gridX] = template[0]
        # m.move(pt[0]+(w/2), pt[1]+(h/2))
        # m.click( pt[0]+(w/2), pt[1]+(h/2))
    # plt.imshow(board, cmap = 'magma')
    # plt.show()

def matchNeighbors(row,col):
    current = board[row][col]
    top = board[row-1][col] if row > 0 else None
    topLeft = board[row-1][col-1] if row > 0 and col > 0 else None
    left = board[row][col-1] if col > 0 else None
    bottomLeft = board[row+1][col-1] if row < 7 and col > 0 else None
    bottom = board[row+1][col] if row < 7 else None
    bottomRight = board[row+1][col+1] if row < 7 and col < 7 else None
    right = board[row][col+1] if col < 7 else None
    topRight = board[row-1][col+1] if row > 0 and col < 7 else None

    farRight = board[row][col+2] if col < 6 else None
    farLeft = board[row][col-2] if col > 1 else None
    farTop = board[row-2][col] if row > 1 else None
    farBottom = board[row+2][col] if row < 6 else None

    if(top == left == bottom):
        gridToClick(row,col)
        gridToClick(row,col-1)

    if(top == right == bottom):
        gridToClick(row,col)
        gridToClick(row,col+1)

    if(right == left == top):
        gridToClick(row,col)
        gridToClick(row-1,col)

    if(right == left == bottom):
        gridToClick(row,col)
        gridToClick(row+1,col)

    if(current == top == bottomRight):
        gridToClick(row+1,col)
        gridToClick(row+1,col+1)

    if(current == top == bottomLeft):
        gridToClick(row+1,col)
        gridToClick(row+1,col-1)

    if(current == bottom == topRight):
        gridToClick(row-1,col)
        gridToClick(row-1,col+1)

    if(current == bottom == topLeft):
        gridToClick(row-1,col)
        gridToClick(row-1,col-1)

    if(current == left == topRight):
        gridToClick(row,col+1)
        gridToClick(row-1,col+1)

    if(current == left == bottomRight):
        gridToClick(row,col+1)
        gridToClick(row+1,col+1)

    if(current == right == topLeft):
        gridToClick(row,col-1)
        gridToClick(row-1,col-1)

    if(current == right == bottomLeft):
        gridToClick(row,col-1)
        gridToClick(row+1,col-1)

    if(current == left == farRight):
        gridToClick(row,col+1)
        gridToClick(row,col+2)

    if(current == right == farLeft):
        gridToClick(row,col-1)
        gridToClick(row,col-2)

    if(current == bottom == farTop):
        gridToClick(row-1,col)
        gridToClick(row-2,col)

    if(current == top == farBottom):
        gridToClick(row+1,col)
        gridToClick(row+2,col)

# MAIN LOOP
while True:
    # BUILD THE BOARD
    for g in gems:
        print(g[0])
        multiFind(g)
    # PRINT THE BOARD
    for rows in board:
        print(rows)
    # ACT!
    for row in range(0,8):
        for col in range(0,8):
            matchNeighbors(row,col)

    # WAIT!
    time.sleep(.5)
