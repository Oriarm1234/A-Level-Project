from InteractiveOverlays import *
import pygame
helpMenu = Overlay(("HelpMenu"),
                      (1060,600),
                      [0,0],
                      None,
                      [pygame.SRCALPHA],
                      [])

Background = StillImage("background", pygame.image.load("Background.png"), (0,0), helpMenu)
Background.crop_image(0,150, 1060, 600)
Background.move_backwards(100)

HelpLabel = Text(
    "Help", 
    "copperplategothic", 
    64, 
    (20,20,20), 
    (530,100), 
    "MainMenuLabel",
    helpMenu)

HelpLabel.align_to_center()
HelpLabel.set_underline(True)

HelpLabel = Text(
    ":,(", 
    "copperplategothic", 
    64, 
    (20,20,20), 
    (530,200), 
    "MainMenuLabel",
    helpMenu)

HelpLabel.align_to_center()