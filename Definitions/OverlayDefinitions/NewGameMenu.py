from ..InteractiveOverlays import (StillImage,
                                   Text,
                                   Overlay)
import pygame

images = {}

def init(imageObjects = {}):

    global images
    images = imageObjects

def newGameMenu(screenSize):

    self = Overlay(("newGameMenu"),
                        screenSize,
                        (0,0),
                        None,
                        [pygame.SRCALPHA],
                        [])



    newGameLabel = Text(
        "New Game", 
        "copperplategothic", 
        64, 
        (20,20,20), 
        (530,100), 
        "mainMenuLabel",
        self)

    newGameLabel.align_to_center()
    newGameLabel.set_underline(True)


    saveSlots = []

    for i in range(5):
        saveSlotButton = StillImage(
            f"saveSlotButton-{str(i + 1)}",
            images.get("button", None),
            (530, 200),
            self,
            imageName="button",
        )

        saveSlotLabel = Text(
            f"Save Slot {str(i + 1)}",
            "copperplategothic",
            32,
            (0, 0, 0),
            (530, 200),
            f"saveSlotLabel-{str(i + 1)}",
            self,
        )

        saveSlots.append((saveSlotButton, saveSlotLabel))

        saveSlotButton.align_to_center()
        saveSlotLabel.align_to_center()

        saveSlotButton.resize_image(*saveSlotLabel.hitbox.size)
        saveSlotButton.resize_image_by_amount(40,20)
        spacing = 16

        saveSlotButton.interactive = True

        if i>0:
            saveSlotButton.y = saveSlots[i-1][0].hitbox.h + saveSlots[i-1][0]._y + spacing
            saveSlotLabel.y = saveSlots[i-1][0].hitbox.h + saveSlots[i-1][0]._y + spacing
            
    return self