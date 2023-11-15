from InteractiveOverlays import *
import pygame
helpMenu = Overlay(("HelpMenu"),
                      (1060,600),
                      [0,0],
                      None,
                      [pygame.SRCALPHA],
                      [])

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