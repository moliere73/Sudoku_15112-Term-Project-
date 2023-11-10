from cmu_graphics import *
from PIL import Image

##################################
# Screen2
##################################

# image cited from:
# https://www.istockphoto.com/vector/pop-art-vintage-comics-style-woman-texting-or-using-app-on-smartphone-simple-user-gm1214866727-353623408

def helpScreen_onAppStart(app):
    app.click = Image.open('click.jpg')

    app.click = CMUImage(app.click)

def helpScreen_onScreenActivate(app):
    print('In helpScreen_onScreenActivate')

def helpScreen_onKeyPress(app, key):
    if key == 'p': 
        setActiveScreen('playScreen')
    elif key == 's': 
        setActiveScreen('splashScreen')

#def helpScreen_onStep(app):
#    app.cx = (app.cx + app.dx) % app.width

##################################
#Reference: sudoku instructions from:
#https://sudoku.com/how-to-play/sudoku-rules-for-complete-beginners/
###################################
def helpScreen_redrawAll(app):
    drawImage(app.click, 1300, 800, align='center')
    drawLabel('help screen', app.width/2, 50, size=80, bold=True, font='monospace')
    drawLabel('Your mission now:', app.width/2, 150, size=40, font='cursive')
    drawLabel('1. Use number 1-9 to fill out every row, column, and square', app.width/2, 200, size=35, font='serif')
    drawLabel('2. press every key in () can achieve different effects', app.width/2, 250, size=35, font='serif')
    drawLabel('3. If you are using a mouse', app.width/2, 290, size=35, font='serif')
    drawLabel('click on the game icon or near ()', app.width/2, 330, size=35, font='serif')
    drawLabel('4. click the cell and click the number on the phone to add that value', app.width/2, 370, size=34, font='serif')
    drawLabel('5. Press x to get basic hints(get one each time)', app.width/2, 410, size=32, font='serif', bold=True)
    drawLabel('6. Press y to get advanced hints(fewer legals)', app.width/2, 450, size=32, font='serif', bold=True)
    drawLabel('7. Press s to display all singletons!', app.width/2, 490, size=32, font='serif', bold=True)
    drawLabel('[get many single values at one time!]', app.width/2, 530, size=32, font='serif')
    drawLabel('Remember you can use 5,6,7 multiple times', app.width/2, 570, size=32, font='serif')
    drawLabel('wrong value entered will be marked by a red dot', 700, 610, size=32, bold=True, font='serif')
    drawLabel('When you finish, click z to check board!', app.width/2, 650, size=32, font='serif')
    drawLabel('when you finish one level, it will swtich to next level', app.width/2, 690, size=30, font='serif')
    drawLabel('You can only make 3 mistakes', app.width/2, 730, size=34, font='serif')
    drawLabel('Otherwise, the game will end automatically', app.width/2, 770, size=34, font='serif')
    drawLabel('Press p to play', app.width/3, 850, size=40, bold=True, font='monospace')
    drawLabel('Press s to the Home Page', app.width/3, 900, size=40, bold=True, font='monospace')




