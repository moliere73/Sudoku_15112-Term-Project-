from cmu_graphics import *
from playScreen import *
from PIL import Image

# image cited from:
# https://www.sbs-zipper.com/blog/morandi-colors-the-most-comfortable-color/
def colorScreen_onAppStart(app):
    app.morandi = Image.open('morandi.jpg')
    app.morandi = CMUImage(app.morandi)

def colorScreen_onScreenActivate(app):
    print('In helpScreen_onScreenActivate')

def colorScreen_onKeyPress(app, key):
    if key == 'p': 
        setActiveScreen('playScreen')
    elif key == 's': 
        setActiveScreen('splashScreen')

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


def colorScreen_redrawAll(app):
    drawImage(app.morandi, app.width/2, app.height/2, height = 1100, width = 1000, align='center')

'''
bg color
rgb = (212, 186, 176)
rgb = (127, 134, 123)
rgb = (193, 171, 173)
rgb = (199, 199, 187)
rgb = (239, 237, 231)
selected color
rgb = (156, 93, 65)
rgb = (202, 155, 128)
rgb = (151, 146, 138)
rgb = (209, 212, 208)
'''