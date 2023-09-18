from InteractiveOverlays import *
import pygame
settingsMenu = Overlay(("SettingsMenu"),
                      (1060,600),
                      [0,0],
                      None,
                      [pygame.SRCALPHA],
                      [])

Background = StillImage("background", pygame.image.load("Background.png"), (0,0), settingsMenu)
Background.crop_image(0,150, 1060, 600)
Background.move_backwards(100)

SettingsLabel = Text(
    "Settings", 
    "copperplategothic", 
    64, 
    (20,20,20), 
    (530,100), 
    "MainMenuLabel",
    settingsMenu)

SettingsLabel.align_to_center()
SettingsLabel.set_underline(True)