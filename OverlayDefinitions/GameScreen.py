from InteractiveOverlays import *
import pygame

gameScreen = Overlay("gameScreen",
                     (1060,600),
                     [0,0],
                     None,
                     [pygame.SRCALPHA],
                     [])


background = StillImage("background", pygame.image.load("Background.png"), (0,0), gameScreen)
background.crop_image(0,150, 1060, 600)
background.move_backwards(100)