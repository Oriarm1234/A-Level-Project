import Definitions
from Definitions.OverlayDefinitions import GameUI
from Game.Definitions import game_info
from StartMenu import MenuLoader
import pygame
import glob
import json
import time

screenSize = (1060, 600)                     # SCREEN SIZE
screen = pygame.display.set_mode(screenSize) # MAIN SCREEN SURFACE
imageFileNames = glob.glob("Images\\*.png")  # ALL GUI IMAGES
images = dict(                               # LOADED GUI IMAGES
    [fileName.split("\\")[-1].split(".")[0], pygame.image.load(fileName)] for fileName in imageFileNames
)
print(images)
Definitions.GameScreen.init(images)             
gameScreen = Definitions.GameScreen.gameScreen((1060, 600))

GameUI.init(images)
MenuLoader.init(images, gameScreen, screenSize)


MenuLoader.StartMenu(screen, screenSize)
