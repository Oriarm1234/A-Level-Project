import Definitions
from StartMenu import MenuLoader
import pygame
import glob

imageFileNames = glob.glob("Images\\*.png")
images = dict(
    [fileName.split("\\")[-1].split(".")[0], pygame.image.load(fileName)] for fileName in imageFileNames
)

screenSize = (1060, 600)
screen = pygame.display.set_mode(screenSize)


Definitions.GameScreen.init(images)
gameScreen = Definitions.GameScreen.gameScreen((1060, 600))



MenuLoader.init(images, gameScreen, screenSize)

MenuLoader.StartMenu(screen, screenSize, images)
