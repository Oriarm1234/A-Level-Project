import Definitions
from Definitions.OverlayDefinitions import GameUI
from Game.Definitions import game_info
import pygame
import glob

import time

screenSize = (1060, 600)
imageFileNames = glob.glob("Images\\*.png")
images = dict(
    [fileName.split("\\")[-1].split(".")[0], pygame.image.load(fileName)] for fileName in imageFileNames
)

GameUI.init(images)



manager = Definitions.InteractiveOverlays.OverlayManager("PlayerUI", screenSize, (0,0),[],[GameUI.gameUI(screenSize, game_info)])


manager.set_overlay_visible(manager.get_overlay_by_name("GameUI"))

screen = pygame.display.set_mode(screenSize)
s = time.time()
while True:
    manager.update()
    
    if time.time()-s > 1:
        s = time.time()
        game_info["Level"] += 1
    
    screen.fill((0,0,0,0))
    screen.blit(manager.screen,(0,0))
    pygame.display.update()
    
