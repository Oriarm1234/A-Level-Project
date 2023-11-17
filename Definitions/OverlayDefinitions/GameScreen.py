from ..InteractiveOverlays import (Element, 
                                   ElementDict, 
                                   ElementList, 
                                   StillImage,
                                   Text,
                                   Rectangle,
                                   Circle,
                                   Line,
                                   Group,
                                   Overlay,
                                   OverlayManager)
import pygame

images = {}

def init(imageObjects = {}):

    global images
    images = imageObjects

def gameScreen(screenSize):

    gameScreen = Overlay("gameScreen",
                        screenSize,
                        [0,0],
                        None,
                        [pygame.SRCALPHA],
                        [])


    background = StillImage("background", images.get("Background", None), (0,0), gameScreen)
    background.crop_image(0,150, 1060, 600)
    background.move_backwards(100)
    
    return gameScreen