from InteractiveOverlays import *
import pygame
helpMenu = Overlay(("helpMenu"),
                      (1060,600),
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
    helpMenu)

helpLabel.align_to_center()
helpLabel.set_underline(True)

helpLabel = Text(
    ":,(", 
    "copperplategothic", 
    64, 
    (20,20,20), 
    (530,200), 
    "MainMenuLabel",
    helpMenu)

helpLabel.align_to_center()