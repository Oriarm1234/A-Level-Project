from InteractiveOverlays import *
import pygame
loadGameMenu = Overlay(("LoadGameMenu"),
                      (1060,600),
                      [0,0],
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

Background = StillImage("background", pygame.image.load("Background.png"), (0,0), loadGameMenu)
Background.crop_image(0,150, 1060, 600)
Background.move_backwards(100)

SaveSlots = []

for i in range(5):
    SaveSlotButton = StillImage(
        "SaveSlotButton-"+str(i+1),
        pygame.image.load("button.png"),
        (530,200),
        loadGameMenu,
        image_name="button.png")

    SaveSlotLabel = Text(
        "Save Slot "+str(i+1), 
        "copperplategothic", 
        32, 
        (0,0,0), 
        (530,200), 
        "SaveSlotLabel-"+str(i+1),
        loadGameMenu)
    
    SaveSlots.append((SaveSlotButton, SaveSlotLabel))
    
    SaveSlotButton.align_to_center()
    SaveSlotLabel.align_to_center()

    SaveSlotButton.resize_image(*SaveSlotLabel.Hitbox.size)
    SaveSlotButton.resize_image_by_amount(40,20)
    Spacing = 16

    SaveSlotButton.Interactive = True

    if i>0:
        SaveSlotButton.y = SaveSlots[i-1][0].Hitbox.h + SaveSlots[i-1][0].y + Spacing
        SaveSlotLabel.y = SaveSlots[i-1][0].Hitbox.h + SaveSlots[i-1][0].y + Spacing