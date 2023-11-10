from cmu_graphics import *
from splashScreen import *
from helpScreen import *
from playScreen import *
from colorScreen import *


#https://www.cs.cmu.edu/afs/cs.cmu.edu/academic/class/15112-3-s23/www/notes/runAppWithScreensDemo1.py
##################################

# main
##################################

def main():
    runAppWithScreens(initialScreen='splashScreen', width=1500, height=1000)

main()  