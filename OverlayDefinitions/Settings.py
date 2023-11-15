from InteractiveOverlays import *
from OverlayDefinitions.ExtraElements import *
import pygame

settingsMenu = Overlay(
    ("SettingsMenu"), (1060, 600), (0, 0), None, [pygame.SRCALPHA], []
)


SettingsLabel = Text(
    "Settings",
    "copperplategothic",
    64,
    (20, 20, 20),
    (530, 100),
    "MainMenuLabel",
    settingsMenu,
)

SettingsLabel.align_to_center()
SettingsLabel.set_underline(True)

arrow = pygame.image.load("Images\\dropdownarrow.png")

s1 = Slider((300, 300), "sliderC", settingsMenu, MaxVal=255, roundNDigits = 0)
s2 = Slider((300, 400), "sliderD", settingsMenu)
d1 = DropdownList(
    "Dropper",
    pygame.transform.rotate(arrow, 180),
    (300, 450),
    settingsMenu,
    "Images\\dropdownarrow.png",
    ["Fullscreen", "1920x1080"][::-1],
    "calibri",
    14,
    (20, 20, 20),
    True,
    (150, 150, 150),
    (180, 180, 180),
    2,
    2,
)

tb1 = Tickbox((400, 450), (24,24), "tb1", 10, settingsMenu, 2, (80,80,80), (140,140,140), (80,80,80), 2, pygame.image.load("Images\\tick.png"), False)

t1 = TextInputBox((250,500), (300, 20), 4, 16, "calibri", "t1", settingsMenu, 2, (100,100,100), (140,140,140), (180,180,180), (40,40,40) ,DefaultText="a",HoloText="Enter Text Here", maxVisibleCharacterLimit=40, maxCharacterLimit=40)
t1.pointerForcedInvisible = False