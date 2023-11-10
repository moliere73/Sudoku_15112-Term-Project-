from cmu_graphics import *
import math
import copy
from copy import deepcopy
import random
import os
import itertools
from itertools import combinations
from PIL import Image
from colorScreen import *


#UI inspired from: 
# https://www.youtube.com/watch?v=Jw8aE9QQmE4
# https://www.youtube.com/watch?v=QgkVz9sdHEs

#https://www.cs.cmu.edu/afs/cs.cmu.edu/academic/class/15112-3-s23/www/notes/term-project.html
#https://www.cs.cmu.edu/afs/cs.cmu.edu/academic/class/15112-3-s23/www/notes/tp-sudoku-hints.html
def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)

##################################
#Board loading
##################################
def loadBoardPaths(filters):
    boardPaths = [ ]
    for filename in os.listdir(f'boards/'):
        if filename.endswith('.txt'):
            if hasFilters(filename, filters):
                boardPaths.append(f'boards/{filename}')
    return boardPaths

def hasFilters(filename, filters=None):
    if filters == None: return True
    for filter in filters:
        if filter not in filename:
            return False
    return True

def loadRandomBoard(filters=None):
    boardPaths = loadBoardPaths(filters)
    boardPath = random.choice(boardPaths)
    board = [[] for _ in range(9)]
    with open(boardPath, 'r') as file:
        lines = file.read().splitlines()
    for row in range(9):
        for char in lines[row]:
            if char.isdigit():
                board[row].append(int(char))
    return board

##################################
# App
#https://cs3-112-f22.academy.cs.cmu.edu/notes/4187
##################################
def playScreen_onAppStart(app, filters=None):
    ##################################
    #draw board
    ##################################
    app.rows = 9
    app.cols = 9
    app.boardLeft = 75
    app.boardTop = 75
    app.boardWidth = 810
    app.boardHeight = 810
    app.cellBorderWidth = 0.5

    # Load the PIL image
    app.keypad = Image.open('keypad.jpg')
    
    app.easy = Image.open('easy.jpg')
    app.medium = Image.open('medium.jpg')
    app.hard = Image.open('hard.jpg')
    app.expert = Image.open('expert.jpg')
    app.evil = Image.open('evil.jpg')
    app.random = Image.open('random.jpg')
    app.machine = Image.open('machine.jpg')
    app.hint1 = Image.open('hint1.jpg')
    app.hint2 = Image.open('hint2.jpg')
    app.singleton = Image.open('singleton.jpg')
    app.manual = Image.open('manual.jpg')
    app.notes = Image.open('notes.jpg')
    
    # Convert each PIL image to a CMUImage for drawing
    app.keypad = CMUImage(app.keypad)
    app.easy = CMUImage(app.easy)
    app.medium = CMUImage(app.medium)
    app.hard = CMUImage(app.hard)
    app.expert = CMUImage(app.expert)
    app.evil = CMUImage(app.evil)
    app.machine = CMUImage(app.machine)
    app.random = CMUImage(app.random)
    app.hint1 = CMUImage(app.hint1)
    app.hint2 = CMUImage(app.hint2)
    app.singleton = CMUImage(app.singleton)
    app.manual = CMUImage(app.manual)
    app.notes = CMUImage(app.notes)

    ##################################
    # Controllers
    ##################################
    app.selection = None
    app.showLegals = False
    
    ##################################
    #game over
    app.gameOver = False
    #################################
    
    board = loadRandomBoard(filters=None)
    app.board = board
    app.legals = getLegals(app)
    initialize(app)
    app.solved = solveSudoku(board)
    app.levelSelected = str(filters)
    app.movesMade = []
    app.movesToRedo = []
    app.singletons = True
    app.mistakes = 0

    legalColor = rgb(101, 101, 101)
    app.legalColor = legalColor
    selectedColor = rgb(253, 249, 238)
    app.selectedColor = selectedColor
    bgColor = rgb(205, 223, 210)#light green
    app.bgColor = bgColor

def initialize(app):
    app.rows, app.cols = len(app.board), len(app.board[0])
    app.initialValue = [[app.board[row][col] != 0 for col in range(app.cols)] for row in range(app.rows)]
    # False if 0; True if not 0

#set discard method: https://www.w3schools.com/python/ref_set_discard.asp
def getLegals(app):
    legals = [[set(range(1, 10)) for _ in range(9)] for _ in range(9)]
    for row in range(app.rows):
        for col in range(app.cols):
            value = app.board[row][col]
            if value != 0:
                for c in range(app.cols):
                    legals[row][c].discard(value)
                for r in range(app.rows):
                    legals[r][col].discard(value)
                blockRow, blockCol = row // 3, col // 3
                for r in range(blockRow * 3, (blockRow + 1) * 3):
                    for c in range(blockCol * 3, (blockCol + 1) * 3):
                        legals[r][c].discard(value)
    return legals

def drawLegals(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    legalRows = app.rows//3
    legalCols = app.cols//3
    legalWidth = cellWidth//3
    legalHeight = cellHeight//3
    legalMoves = sorted(list(app.legals[row][col]))
    # step by step place the legals
    for i in range(len(legalMoves)):
        legalValue = legalMoves[i]
        cellX = (i % legalCols) * legalWidth
        cellY = (i // legalRows) * legalHeight
        legalX = cellLeft + cellX + legalWidth/2
        legalY = cellTop + cellY + legalHeight/2
        fill = app.legalColor
        drawLabel(legalValue, legalX, legalY, size=20, fill=fill)

#Region function downloaded from:
#https://www.cs.cmu.edu/afs/cs.cmu.edu/academic/class/15112-3-s23/www/notes/tp-sudoku-hints.html
def getCellRegions(app, row, col):
    rows = len(app.board)
    blockSize = int(rows**0.5)
    regions = []
    for i in range(rows):
        if i != col:
            regions.append((row, i))
        if i != row:
            regions.append((i, col))
    blockRow = (row // blockSize) * blockSize
    blockCol = (col // blockSize) * blockSize
    for i in range(blockRow, blockRow + blockSize):
        for j in range(blockCol, blockCol + blockSize):
            if i != row or j != col:
                regions.append((i, j))
    return regions

def setVal(app, row, col, value):
    prevVal = app.board[row][col]
    app.board[row][col] = value
    for banR, banC in getCellRegions(app, row, col):
        ban(app, banR, banC, {value})
    newVal = app.board[row][col]
    if prevVal != newVal:
        for unbanR, unbanC in getCellRegions(app, row, col):
            unban(app, unbanR, unbanC, {prevVal})
    
#set discard method: https://www.w3schools.com/python/ref_set_discard.asp
def ban(app, row, col, values):
    for value in values:
        if value != 0:
            app.legals[row][col].discard(value)

def unban(app, row, col, values):
    for value in values:
        if value != 0:
            app.legals[row][col].add(value)
    
def drawGameOver(app):
    drawRect(0, 0, 1500, 1000, fill='beige')
    drawLabel('GAME OVER!', app.width/2, app.height/2, size = 200, bold=True, font='monospace')
    drawLabel('Press v to restart!', 700, 700, size = 100, font='monospace')   

def checkSudoku(app):
    rows, cols = len(app.board), len(app.board[0])
    for row in range(rows):
        if set([app.board[row][col] for col in range(cols)]) != set(range(1, 10)):
            app.gameOver = True
    for col in range(cols):
        if set([app.board[row][col] for row in range(cols)]) != set(range(1, 10)):
            app.gameOver = True
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            block = [app.board[x][y] for x in range(i, i+3) for y in range(j, j+3)]
            if set(block) != set(range(1, 10)):
                app.gameOver = True

def playScreen_redrawAll(app):
    if app.gameOver == True:
            drawGameOver(app)
            return
    drawBoard(app)
    drawBoardBorder(app)
    drawBlockBorder(app)
    drawBoardLevel(app)
    drawLabel('The * on phone is undo move (or press u)!', 320, 900, size=25, bold=True, font='monospace')
    #the asterisk
    drawLabel('The # on phone is redo move (or press r)!', 320, 940, size=25, bold=True, font='monospace')
    #the pound key
    drawImage(app.keypad, 1100, 580, height=800, width=350, align='center')
    #https://www.pngegg.com/en/search?q=game+Icon
    drawLabel('easy', 1000, 30, size=25, font='monospace')
    drawImage(app.easy, 1000, 80, height=80, width=90, align='center')
    drawLabel("('a')", 1000, 130, size=25, font='monospace', bold=True)
    drawLabel("help('h')", 1015, 180, size=25, font='monospace', bold=True)
    drawImage(app.random, 1000, 240, height=80, width=90, align='center')
    drawLabel('medium', 1110, 30, size=25, font='monospace')
    drawLabel("('b')", 1100, 130, size=25, font='monospace', bold=True)
    drawImage(app.medium, 1110, 80, height=80, width=90, align='center')
    drawLabel('hard', 1220, 30, size=25, font='monospace')
    drawImage(app.hard, 1220, 80, height=80, width=90, align='center')
    drawLabel("('c')", 1220, 130, size=25, font='monospace', bold=True)
    drawLabel('expert', 1330, 30, size=25, font='monospace')
    drawImage(app.expert, 1330, 80, height=80, width=90, align='center')
    drawLabel("('d')", 1330, 130, size=25, font='monospace', bold=True)
    drawLabel('evil', 1440, 30, size=25, font='monospace')
    drawImage(app.evil, 1440, 80, height=80, width=90, align='center')
    drawLabel("('e')", 1440, 130, size=25, font='monospace', bold=True)
    drawLabel("choose colors!", 1380, 820, size=25, font='monospace')
    drawImage(app.machine, 1440, 900, height=120, width=110, align='center')
    drawLabel("('m')", 1380, 850, size=25, font='monospace')
    drawLabel("hint1('x')", 1330, 170, size=18, font='monospace', bold=True)
    drawImage(app.hint1, 1330, 230, height=80, width=90, align='center')
    drawLabel("hint2('y')", 1440, 170, size=18, font='monospace', bold=True)
    drawImage(app.hint2, 1440, 230, height=80, width=90, align='center')
    drawImage(app.notes, 1360, 730, height=100, width=90, align='center')
    drawLabel('check', 1450, 700, size=20, font='monospace', bold=True)
    drawLabel("board", 1450, 730, size=20, font='monospace', bold=True)
    drawLabel("('z')", 1450, 760, size=20, font='monospace', bold=True)
    #https://www.flaticon.com/free-icon/mobile-game_1792276
    drawLabel("('s')Singleton", 1365, 300, size=20, font='monospace', bold=True)
    drawImage(app.singleton, 1360, 390, height=140, width=160, align='center')
    drawLabel("('l')Legals on/off", 1368, 620, size=19, font='monospace', bold=True)
    drawImage(app.manual, 1365, 530, height=140, width=160, align='center')
    drawLabel(f'Mistakes: {app.mistakes}/3', 140, 30, size=30, font='monospace', bold=True)
   
def playScreen_onKeyPress(app, key):
    if key == 'v':
        playScreen_onAppStart(app, filters=None)

    if not app.gameOver:
        if key == 'm':
            setActiveScreen('colorScreen')
        if key == 'h':
            setActiveScreen('helpScreen')
            
        elif key == 'a':
            playScreen_onAppStart(app, 'easy')
        elif key == 'b':
            playScreen_onAppStart(app, 'medium')
        elif key == 'c':
            playScreen_onAppStart(app, 'hard')
        elif key == 'd':
            playScreen_onAppStart(app, 'expert')
        elif key == 'e':
            playScreen_onAppStart(app, 'evil')

        elif key == 'l':
            app.showLegals = not app.showLegals

        elif key == 's': 
            singletons(app)
            
        elif key == 'u':
            undo(app)

        elif key == 'r': 
            redo(app)
        
        elif key == 'x':
            hint1(app)

        elif key == 'y':
            hint2(app)

        elif key == 'z':
            checkSudoku(app)
            if app.levelSelected == 'easy':
                playScreen_onAppStart(app, 'medium')
            elif app.levelSelected == 'medium':
                playScreen_onAppStart(app, 'hard')
            elif app.levelSelected == 'hard':
                playScreen_onAppStart(app, 'expert')
            elif app.levelSelected == 'expert':
                playScreen_onAppStart(app, 'evil')
            elif app.levelSelected == 'evil':
                playScreen_onAppStart(app, 'evil')

        #bg
        elif key == 'f':
            rgb1 = rgb(212, 186, 176) 
            app.bgColor = rgb1

        elif key == 'g':
            rgb2 = rgb(127, 134, 123)
            app.bgColor = rgb2
        
        elif key == 'j':
            rgb3 = rgb(193, 171, 173)
            app.bgColor = rgb3

        elif key == 'k':
            rgb4 = rgb(199, 199, 187)
            app.bgColor = rgb4

        elif key == 'n':
            rgb5 = rgb(239, 237, 231)
            app.bgColor = rgb5

        #selected
        elif key == 'o':
            rgb6 = rgb(156, 93, 65)
            app.selectedColor = rgb6
        
        elif key == 'q':
            rgb7 = rgb(202, 155, 128)
            app.selectedColor = rgb7

        elif key == 'p':
            rgb8 = rgb(151, 146, 138)
            app.selectedColor = rgb8

        elif key == 't':
            rgb9 = rgb(209, 212, 208)
            app.selectedColor = rgb9

        elif key == 'left':  moveSelection(app, 0, -1)
        elif key == 'right': moveSelection(app, 0, +1)
        elif key == 'up':    moveSelection(app ,-1, 0)
        elif key == 'down':  moveSelection(app, +1, 0)

        elif app.selection is not None and key.isdigit() and int(key) != 0:
            row, col = app.selection
            setVal(app, row, col, int(key))
            app.movesMade.append((row, col))
            num = str(app.board[row][col])
            if int(num) != app.solved[row][col]:
                app.mistakes += 1
                if app.mistakes > 3:
                    app.gameOver = True

#Selecting with Keys
#https://cs3-112-f22.academy.cs.cmu.edu/notes/4189
def moveSelection(app, drow, dcol):
  if app.selection != None:
    selectedRow, selectedCol = app.selection
    newSelectedRow = (selectedRow + drow) % app.rows
    newSelectedCol = (selectedCol + dcol) % app.cols
    app.selection = (newSelectedRow, newSelectedCol)
    app.selectionList = []

def playScreen_onMousePress(app, mouseX, mouseY):
    #print(mouseX, mouseY)
    if app.gameOver == False:
        if app.selection is not None:
            row, col = app.selection
            #print(app.selection)
            if (960 <= mouseX <= 1035) and (687 <= mouseY <= 724):
                setVal(app, row, col, int(1))
                if int(1) != app.solved[row][col]:
                    app.mistakes += 1
                    if app.mistakes > 3:
                        app.gameOver = True
            elif (1057 <= mouseX <= 1134) and (687 <= mouseY <= 724):
                setVal(app, row, col, int(2))
                if int(2) != app.solved[row][col]:
                    app.mistakes += 1
                    if app.mistakes > 3:
                        app.gameOver = True
            elif (1157 <= mouseX <= 1232) and (687 <= mouseY <= 724):
                setVal(app, row, col, int(3))
                if int(3) != app.solved[row][col]:
                    app.mistakes += 1
                    if app.mistakes > 3:
                        app.gameOver = True
            elif (960 <= mouseX <= 1035) and (758 <= mouseY <= 802):
                setVal(app, row, col, int(4))
                if int(4) != app.solved[row][col]:
                    app.mistakes += 1
                    if app.mistakes > 3:
                        app.gameOver = True
            elif (1063 <= mouseX <= 1133) and (758 <= mouseY <= 802):
                setVal(app, row, col, int(5))
                if int(5) != app.solved[row][col]:
                    app.mistakes += 1
                    if app.mistakes > 3:
                        app.gameOver = True
            elif (1160 <= mouseX <= 1233) and (758 <= mouseY <= 802):
                setVal(app, row, col, int(6))
                if int(6) != app.solved[row][col]:
                    app.mistakes += 1
                    if app.mistakes > 3:
                        app.gameOver = True
            elif (960 <= mouseX <= 1035) and (834 <= mouseY <= 874):
                setVal(app, row, col, int(7))
                if int(7) != app.solved[row][col]:
                    app.mistakes += 1
                    if app.mistakes > 3:
                        app.gameOver = True
            elif (1060 <= mouseX <= 1136) and (834 <= mouseY <= 874):
                setVal(app, row, col, int(8))
                if int(8) != app.solved[row][col]:
                    app.mistakes += 1
                    if app.mistakes > 3:
                        app.gameOver = True
            elif (1157 <= mouseX <= 1234) and (834 <= mouseY <= 874):
                setVal(app, row, col, int(9))
                if int(9) != app.solved[row][col]:
                    app.mistakes += 1
                    if app.mistakes > 3:
                        app.gameOver = True

        if 1000 <= mouseX <= 1090 and 80 <= mouseY <= 170:
            playScreen_onAppStart(app, 'easy')
        elif 1110 <= mouseX <= 1200 and 80 <= mouseY <= 170:
            playScreen_onAppStart(app, 'medium')
        elif 1220 <= mouseX <= 1310 and 80 <= mouseY <= 170:
            playScreen_onAppStart(app, 'hard')
        elif 1330 <= mouseX <= 1420 and 80 <= mouseY <= 170:
            playScreen_onAppStart(app, 'expert')
        elif 1440 <= mouseX <= 1530 and 80 <= mouseY <= 170:
            playScreen_onAppStart(app, 'evil')
        elif 942 <= mouseX <= 1080 and 160 <= mouseY <= 273:
            setActiveScreen('helpScreen')
        elif 960 <= mouseX <= 1035 and 901 <= mouseY <= 952:
            undo(app)
        elif 1150 <= mouseX <= 1236 and 901 <= mouseY <= 952:
            redo(app)
        elif 1304 <= mouseX <= 1488 and 660 <= mouseY <= 756:
            checkSudoku(app)
        elif 1280 <= mouseX <= 1488 and 790 <= mouseY <= 925:
            setActiveScreen('colorScreen')
            
        if app.levelSelected != 'easy' and 1330 <= mouseX <= 1420 and 230 <= mouseY <= 310:
            hint1(app)

        if 1280 <= mouseX <= 1440 and 290 <= mouseY <= 441:
            singletons(app)
        
        selectedCell = getCell(app, mouseX, mouseY)
        app.selection = selectedCell

##################################
# draw board functions
#Reference: https://cs3-112-f22.academy.cs.cmu.edu/notes/4187
#Reference: https://cs3-112-f22.academy.cs.cmu.edu/notes/4189
##################################

def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col)

def drawBoardBorder(app):
  # draw the board outline (with double-thickness):
  drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
           fill=None, border='black',
           borderWidth=4)

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)

def drawCell(app, row, col):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
#Color Reference: https://blog.csdn.net/weixin_36670529/article/details/121744863
    #selectedColor = rgb(253, 249, 238)
    color = app.selectedColor if (row, col) == app.selection else None
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color, border='black',
             borderWidth=app.cellBorderWidth)

    #bgColor = rgb(205, 223, 210)#light green
    setNum = app.initialValue[row][col]
    if setNum:
        fill = app.bgColor 
    elif setNum == 0: 
        fill=None
    else:
        fill=None
    drawRect(cellLeft, cellTop, cellWidth, cellHeight, fill=fill, 
                 border='black', borderWidth=app.cellBorderWidth)

    cx = cellLeft + cellWidth/2
    cy = cellTop + cellHeight/2
    num = str(app.board[row][col])
    if num != '0':
        drawLabel(num, cx, cy, size=65, fill='black', font='monospace')
        if int(num) != app.solved[row][col]:
            drawCircle(cx+35, cy+35, 5, fill='red')       
    else: 
        if app.showLegals == True:
            drawLegals(app, row, col)

def getCell(app, x, y):
    dx = x - app.boardLeft
    dy = y - app.boardTop
    cellWidth, cellHeight = getCellSize(app)
    row = math.floor(dy / cellHeight)
    col = math.floor(dx / cellWidth)
    if (0 <= row < app.rows) and (0 <= col < app.cols):
        return (row, col)
    else:
        return None

def drawBlockBorder(app):
    numRows = app.rows
    boardWidth = app.boardWidth
    blockSize = boardWidth / (3)
    boardLeft = app.boardLeft
    boardTop = app.boardTop

    for i in range(numRows):
        col = i % 3
        row = i // 3
        rectLeft = boardLeft + col * blockSize
        rectTop = boardTop + row * blockSize
        drawRect(rectLeft, rectTop, blockSize, blockSize, 
                    fill=None, border='black')

def drawBoardLevel(app):
    if app.levelSelected == 'easy':
        drawLabel('EASY', 500, 40, size=55, font='monospace', bold=True)
    elif app.levelSelected == 'medium':
        drawLabel('MEDIUM', 500, 40, size=55, font='monospace', bold=True)
    elif app.levelSelected == 'hard':
        drawLabel('HARD', 500, 40, size=55, font='monospace', bold=True)
    elif app.levelSelected == 'expert':
        drawLabel('EXPERT', 500, 40, size=55, font='monospace', bold=True)
    elif app.levelSelected == 'evil':
        drawLabel('EVIL', 500, 40, size=55, font='monospace', bold=True)

#Backtracking Solver
# Basic backtracker: expand first empty cell
#Reference: solution for solveMiniSudoku
# https://cs3-112-f22.academy.cs.cmu.edu/exercise/4823
# Faster backtracker: expand cell with fewest legals (modfied solve mini sudoku)

def solveSudoku(board):
    return isSolved(copy.deepcopy(board))

def getCells(board):
    rows, cols = len(board), len(board[0])
    cells = [] # empty cells
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == 0:
                legalValues = getLegalValues(board, row, col)
                # number of legals
                cells.append((row, col, len(legalValues)))
    # first empty cell in the sorted list has the fewest legals
    cells.sort()
    return cells

def isSolved(board):
    cells = getCells(board)
    if cells == []:
        return board
    else:
        #get the least legal
        row, col, num = cells[0]
        for val in getLegalValues(board, row, col):
            board[row][col] = val
            solution = isSolved(board)
            if solution != None:
                return solution
            board[row][col] = 0
        return None

def getLegalValues(board, row, col):
    rows = len(board)
    blockSize = int(rows**0.5)
    values = set(range(1, rows+1))
    for i in range(rows):
        if board[i][col] in values:
            values.remove(board[i][col])
        if board[row][i] in values:
            values.remove(board[row][i])
    blockRow = (row // blockSize) * blockSize
    blockCol = (col // blockSize) * blockSize
    for i in range(blockRow, blockRow+blockSize):
        for j in range(blockCol, blockCol+blockSize):
            if board[i][j] in values:
                values.remove(board[i][j])
    return list(values)

#Undo and Redo
def undo(app):
  if len(app.movesMade) > 0:
    #next move
    row, col = app.movesMade.pop()
    value = app.board[row][col]
    app.movesToRedo.append((row, col, value))
    setVal(app, row, col, 0)
    
def redo(app):
  if len(app.movesToRedo) > 0:
    row, col, value = app.movesToRedo.pop()
    setVal(app, row, col, value)
    app.movesMade.append((row, col))

#Autoplayed Singletons
def singletons(app):
    for row in range(app.rows):
        for col in range(app.cols):
            if app.board[row][col] == 0:
                if len(app.legals[row][col]) == 1:
                    value = list(app.legals[row][col])[0]
                    setVal(app, row, col, value)
                    app.movesMade.append((row, col))

#Hint #1: Obvious (or "Naked") Singles
def hint1(app):
    for row in range(app.rows):
        for col in range(app.cols):
            if app.board[row][col] == 0 and len(app.legals[row][col]) == 1:
                app.selection = row, col
                value = list(app.legals[row][col])[0]  # extract single value from set
                setVal(app, row, col, value)
                app.movesMade.append((row, col))
                return True
    return False

#hint2 functions downloaded from:
#https://www.cs.cmu.edu/afs/cs.cmu.edu/academic/class/15112-3-s23/www/notes/tp-sudoku-hints.html
#Reference for solving sudoku using hint2:
#https://www.conceptispuzzles.com/index.aspx?uri=puzzle/sudoku/techniques#:~:text=The%20easiest%20way%20starting%20a,the%20way%20to%20the%20end.

def hint2(app):
    hint = getHint2(app)
    if hint is None:
        return
    cell, legalVals = hint
    regions = getAllRegionsWithTargets(app, cell)
    bannedCells = []
    for region in regions:
        for r, c in region:
            if (r, c) not in cell:
                bannedCells.append((r, c))
    for r, c in bannedCells:
        banValuesInCells(app, bannedCells,legalVals)

def getHint2(app):
    for N in range(2, 6):
        for region in getAllRegions(app):
            result = applyRule2(app, region, N)
            if result is not None:
                return result
    return None

def applyRule2(app, region, N):
    emptyCells = [(row, col) for row, col in region if app.board[row][col] == 0]
    for combination in itertools.combinations(emptyCells, N):
        legalVals = set()
        for row, col in combination:
            legalVals = legalVals.union(app.legals[row][col])
            if len(legalVals) == N:
                bannedCells = getBannedCellsForRegions(app, combination, legalVals)
                if bannedCells is not None:
                    hint = set(combination).difference(bannedCells)
                    if hint:
                        return hint, legalVals
    return None

def getBannedCellsForRegions(app, values, targets):
    # The values (to be banned) can stay in the targets, but they must be
    # banned from all other cells in all regions that contain all
    # the targets
    cellsInRegions = []
    for region in getAllRegionsWithTargets(app, targets):
        cellsInRegions.extend(region)
    bannedCells = set(cellsInRegions).difference(targets)
    return bannedCells

def getAllRegionsWithTargets(app, targets):
    regions = []
    for region in getAllRegions(app):
        if set(region).intersection(targets) == set(targets):
            regions.append(region)
    return regions

def banValuesInCells(app, cells, values):
    for r, c in cells:
        ban(app, r, c, values)

def getRowRegion(app, row):
    region = [(row, col) for col in range(app.cols)]
    return region

def getColRegion(app, col):
    region = [(row, col) for row in range(app.rows)]
    return region

def getBlockRegion(app, block):
    region = []
    blockSize = int(app.rows**0.5)
    startRow = (block // blockSize) * blockSize
    startCol = (block % blockSize) * blockSize
    for i in range(startRow, startRow + blockSize):
        for j in range(startCol, startCol + blockSize):
            region.append((i, j))
    return region

def getAllRegions(app):
    regions = []
    regions.extend([getRowRegion(app, row) for row in range(app.rows)])
    regions.extend([getColRegion(app, col) for col in range(app.cols)])
    regions.extend([getBlockRegion(app, block) for block in range(app.rows)])
    return regions