from ..InteractiveOverlays import (
                                    Text,
                                    StillImage,
                                    Overlay)

import pygame


def level_text_update(self, screen, *args, **kwargs):
    self.text = "Level: " + str(self.parent.game_info["Level"])


images = {}

def init(imageObjects = {}):

    global images
    images = imageObjects

def gameUI(screenSize, game_info):

    self = Overlay("GameUI",
                        screenSize,
                        [0,0],
                        None,
                        [pygame.SRCALPHA],
                        [])
    self.game_info = game_info

    levelText = Text("Level: " + str(game_info["Level"]),  "copperplategothic", 32, (80,80,80), (screenSize[0],0), "levelTextbox", self)
    
    levelText.update_function = level_text_update
    levelText.align_to_bottom_left()
    
    
    return self