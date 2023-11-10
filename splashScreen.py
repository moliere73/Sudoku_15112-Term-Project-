from cmu_graphics import *
from PIL import Image

##################################
# Screen1
##################################
#Images cited from:
#https://www.istockphoto.com/vector/retro-telephone-ringing-vintage-pop-art-comic-book-vector-illustration-gm693774356-128181289
#https://www.istockphoto.com/vector/pop-art-woman-on-phone-gm517501441-49236670

def splashScreen_onAppStart(app):
    # Load the PIL image
    app.dring = Image.open('dring.jpg')
    app.play = Image.open('play.jpg')
    
    app.dring = CMUImage(app.dring)
    app.play = CMUImage(app.play)
   
    #print('In splashScreen_onAppStart')

def splashScreen_onScreenActivate(app):
    print('In splashScreen_onScreenActivate')

def splashScreen_onKeyPress(app, key):
    if key == 'p': 
        setActiveScreen('playScreen')
    elif key == 'h':
        setActiveScreen('helpScreen')

def splashScreen_redrawAll(app):
    drawImage(app.dring, 250, 700, align='center')
    drawImage(app.play, 900, 320, align='center')
    #drawLabel('SUDOKU')
    drawLabel('Press p to play', 1200, 800, size=60, bold=True, font='monospace')
    drawLabel('Press h to get help', 1000, 900, size=60, font='monospace')




