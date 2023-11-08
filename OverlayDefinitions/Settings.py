from InteractiveOverlays import *
from OverlayDefinitions.ExtraElements import *
import pygame
settingsMenu = Overlay(("SettingsMenu"),
                      (1060,600),
                      (0,0),
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

arrow = pygame.image.load("Images\\dropdownarrow.png")

s1 = Slider((300,300), "sliderC", settingsMenu)
s2 = Slider((300,400), "sliderD", settingsMenu)
d1 = DropdownList("Dropper", pygame.transform.rotate(arrow, 180), (300,500), settingsMenu, "Images\\dropdownarrow.png", ["Hamburber", "chesburger","balls"], "calibri", 14, (20,20,20), True, (150,150,150), (180,180,180), 2, 2)