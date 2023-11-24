from ..InteractiveOverlays import (
                                   StillImage,
                                   Overlay)
import pygame

images = {}

def init(imageObjects = {}):

    global images
    images = imageObjects

def gameScreen(screenSize):

    self = Overlay("gameScreen",
                        screenSize,
                        [0,0],
                        None,
                        [pygame.SRCALPHA],
                        [])

    background = StillImage("background", images.get("Background", None), (0,0), self)
    background.crop_image(0,150, screenSize[0], screenSize[1])
    background.move_backwards(100)
    
    return self