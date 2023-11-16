from InteractiveOverlays import *
import pygame
loadGameMenu = Overlay(("LoadGameMenu"),
                      (1060,600),
                      (0,0),
                      None,
                      [pygame.SRCALPHA],
                      [])

LoadGameLabel = Text(
    "Load Game", 
    "copperplategothic", 
    64, 
    (20,20,20), 
    (530,100), 
    "MainMenuLabel",
    loadGameMenu)

LoadGameLabel.align_to_center()
LoadGameLabel.set_underline(True)


SaveSlots = []

for i in range(5):
    SaveSlotButton = StillImage(
        f"SaveSlotButton-{str(i + 1)}",
        pygame.image.load("button.png"),
        (530, 200),
        loadGameMenu,
        image_name="button.png",
    )

    SaveSlotLabel = Text(
        f"Save Slot {str(i + 1)}",
        "copperplategothic",
        32,
        (0, 0, 0),
        (530, 200),
        f"SaveSlotLabel-{str(i + 1)}",
        loadGameMenu,
    )

    SaveSlots.append((SaveSlotButton, SaveSlotLabel))

    SaveSlotButton.align_to_center()
    SaveSlotLabel.align_to_center()

    SaveSlotButton.resize_image(*SaveSlotLabel.hitbox.size)
    SaveSlotButton.resize_image_by_amount(40,20)
    Spacing = 16

    SaveSlotButton.interactive = True

    if i>0:
        SaveSlotButton.y = SaveSlots[i-1][0].hitbox.h + SaveSlots[i-1][0]._y + Spacing
        SaveSlotLabel.y = SaveSlots[i-1][0].hitbox.h + SaveSlots[i-1][0]._y + Spacing