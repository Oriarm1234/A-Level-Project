from MainMenu.MenuLoader import StartMenu, overlayManager, gameScreen
import pygame
import glob

imageFileNames = glob.glob("Images\\*.png")
images = dict(
    [fileName.split("\\")[-1].split(".")[0], pygame.image.load(fileName)] for fileName in imageFileNames
)

screenSize = (1060,600)

currentState = "startScreen"
screen = pygame.display.set_mode(screenSize)
screen.fill((255, 255, 255))

StartMenu(screen, screenSize, images)