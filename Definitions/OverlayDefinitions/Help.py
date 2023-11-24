from ..InteractiveOverlays import (
                                   Text,
                                   Overlay)
import pygame

images = {}

def init(imageObjects = {}):

    global images
    images = imageObjects
    
def helpMenu(screenSize):

    self = Overlay(("helpMenu"),
                        screenSize,
                        [0,0],
                        None,
                        [pygame.SRCALPHA],
                        [])

    helpLabel = Text(
        "Help", 
        "copperplategothic", 
        64, 
        (20,20,20), 
        (530,100), 
        "MainMenuLabel",
        self)

    helpLabel.align_to_center()
    helpLabel.set_underline(True)

    helpLabel = Text(
        ":,(", 
        "copperplategothic", 
        64, 
        (20,20,20), 
        (530,200), 
        "MainMenuLabel",
        self)

    helpLabel.align_to_center()
    
    return self