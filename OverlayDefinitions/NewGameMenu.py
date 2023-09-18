from InteractiveOverlays import *
import pygame
newGameMenu = Overlay(("NewGameMenu"),
                      (1060,600),
                      [0,0],
                      None,
                      [pygame.SRCALPHA],
                      [])

Background = StillImage("background", pygame.image.load("Background.png"), (0,0), newGameMenu)
Background.crop_image(0,150, 1060, 600)
Background.move_backwards(100)

NewGameLabel = Text(
    "New Game", 
    "copperplategothic", 
    64, 
    (20,20,20), 
    (530,100), 
    "MainMenuLabel",
    newGameMenu)

NewGameLabel.align_to_center()
NewGameLabel.set_underline(True)


SaveSlots = []

for i in range(5):
    SaveSlotButton = StillImage(
        "SaveSlotButton-"+str(i+1),
        pygame.image.load("button.png"),
        (530,200),
        newGameMenu,
        image_name="button.png")

    SaveSlotLabel = Text(
        "Save Slot "+str(i+1), 
        "copperplategothic", 
        32, 
        (0,0,0), 
        (530,200), 
        "SaveSlotLabel-"+str(i+1),
        newGameMenu)
    
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