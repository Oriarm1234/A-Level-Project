from InteractiveOverlays import *
import pygame
mainMenu = Overlay("MainMenu",
                     (1060,600),
                     [0,0],
                     None,
                     [pygame.SRCALPHA],
                     [])


NewGameButton = StillImage(
    "NewGameButton",
    pygame.image.load("button.png"),
    (530,200),
    mainMenu,
    image_name="button.png")

NewGameLabel = Text(
    "New Run", 
    "copperplategothic", 
    32, 
    (0,0,0), 
    (530,200), 
    "NewGameLabel",
    mainMenu)

LoadGameButton = StillImage(
    "LoadGameButton",
    pygame.image.load("button.png"),
    (530,200),
    mainMenu,
    image_name="button.png")

LoadGameLabel = Text(
    "Load Run", 
    "copperplategothic", 
    32, 
    (0,0,0), 
    (530,200), 
    "LoadGameLabel",
    mainMenu)

SettingsButton = StillImage(
    "SettingsButton",
    pygame.image.load("button.png"),
    (530,200),
    mainMenu,
    image_name="button.png")

SettingsLabel = Text(
    "Settings", 
    "copperplategothic", 
    32, 
    (0,0,0), 
    (530,200), 
    "SettingsLabel",
    mainMenu)

HelpButton = StillImage(
    "HelpButton",
    pygame.image.load("button.png"),
    (530,200),
    mainMenu,
    image_name="button.png")

HelpLabel = Text(
    "Help", 
    "copperplategothic", 
    32, 
    (0,0,0), 
    (530,200), 
    "HelpLabel",
    mainMenu)

QuitButton = StillImage(
    "QuitButton",
    pygame.image.load("button.png"),
    (530,200),
    mainMenu,
    image_name="button.png")

QuitLabel = Text(
    "Quit", 
    "copperplategothic", 
    32, 
    (0,0,0), 
    (530,200), 
    "QuitLabel",
    mainMenu)

NewGameButton.align_to_center()
NewGameLabel.align_to_center()
LoadGameButton.align_to_center()
LoadGameLabel.align_to_center()
SettingsButton.align_to_center()
SettingsLabel.align_to_center()
HelpButton.align_to_center()
HelpLabel.align_to_center()
QuitButton.align_to_center()
QuitLabel.align_to_center()


LoadGameButton.resize_image(*LoadGameLabel.Hitbox.size)
LoadGameButton.resize_image_by_amount(40,20)


NewGameButton.resize_image(*LoadGameLabel.Hitbox.size)
SettingsButton.resize_image(*LoadGameLabel.Hitbox.size)
HelpButton.resize_image(*LoadGameLabel.Hitbox.size)
QuitButton.resize_image(*LoadGameLabel.Hitbox.size)
NewGameButton.resize_image_by_amount(40,20)
SettingsButton.resize_image_by_amount(40,20)
HelpButton.resize_image_by_amount(40,20)
QuitButton.resize_image_by_amount(40,20)

Spacing = 16

LoadGameLabel.y = NewGameButton.Hitbox.h + NewGameButton.y + Spacing
LoadGameButton.y = NewGameButton.Hitbox.h + NewGameButton.y + Spacing
SettingsLabel.y = LoadGameButton.Hitbox.h + LoadGameButton.y + Spacing
SettingsButton.y = LoadGameButton.Hitbox.h + LoadGameButton.y + Spacing
HelpLabel.y =  SettingsButton.Hitbox.h + SettingsButton.y + Spacing
HelpButton.y = SettingsButton.Hitbox.h + SettingsButton.y + Spacing
QuitLabel.y =  HelpButton.Hitbox.h + HelpButton.y + Spacing
QuitButton.y = HelpButton.Hitbox.h + HelpButton.y + Spacing

MainMenuLabel = Text(
    "Main Menu", 
    "copperplategothic", 
    64, 
    (20,20,20), 
    (530,100), 
    "MainMenuLabel",
    mainMenu)

MainMenuLabel.align_to_center()
MainMenuLabel.set_underline(True)

Background = StillImage("background", pygame.image.load("Background.png"), (0,0), mainMenu)
Background.crop_image(0,150, 1060, 600)
Background.move_backwards(100)

BestDungeonRunsFrame = StillImage("BestDungeonRunsFrame", pygame.image.load("button.png"), (20,20), mainMenu, image_name="button.png")
BestDungeonRunsFrame.resize_image(180,60)

BestDungeonRunsLabel = Text(
    "Best Dungeon Runs", 
    "copperplategothic", 
    16, 
    (20,20,20), 
    (110,50), 
    "BestDungeonRunsLabel",
    mainMenu)
BestDungeonRunsLabel.align_to_center()
BestDungeonRunsLabel.set_underline(True)

AchievementsFrame = StillImage("AchievementsFrame", pygame.image.load("button.png"), (1040,20), mainMenu, image_name="button.png")
AchievementsFrame.resize_image(180,60)
AchievementsFrame.align_to_bottom_left()

AchievementsLabel = Text(
    "Achievements",  
    "copperplategothic", 
    16, 
    (20,20,20), 
    (950,50), 
    "AchievementsLabel",
    mainMenu)
AchievementsLabel.align_to_center()
AchievementsLabel.set_underline(True)


def NewGameButtonPressed(self, *args, **kwargs):
   
    NewGameMenu = mainMenu._parent.getOverlayByName("NewGameMenu")
    
    if NewGameMenu != None:
        
        mainMenu._parent.SetOverlayVisible(mainMenu, False)
        mainMenu._parent.SetOverlayVisible(NewGameMenu, True)

def LoadGameButtonPressed(self, *args, **kwargs):
   
    LoadGameMenu = mainMenu._parent.getOverlayByName("LoadGameMenu")
    
    if LoadGameMenu != None:
        
        mainMenu._parent.SetOverlayVisible(mainMenu, False)
        mainMenu._parent.SetOverlayVisible(LoadGameMenu, True)

def SettingsButtonPressed(self, *args, **kwargs):
   
    SettingsMenu = mainMenu._parent.getOverlayByName("SettingsMenu")
    
    if SettingsMenu != None:
        
        mainMenu._parent.SetOverlayVisible(mainMenu, False)
        mainMenu._parent.SetOverlayVisible(SettingsMenu, True)

def HelpButtonPressed(self, *args, **kwargs):
   
    HelpMenu = mainMenu._parent.getOverlayByName("HelpMenu")
    
    if HelpMenu != None:
        
        mainMenu._parent.SetOverlayVisible(mainMenu, False)
        mainMenu._parent.SetOverlayVisible(HelpMenu, True)

def QuitButtonPressed(self, *args, **kwargs):
    pygame.quit()
    quit()

NewGameButton.pressed = NewGameButtonPressed
LoadGameButton.pressed = LoadGameButtonPressed
SettingsButton.pressed = SettingsButtonPressed
HelpButton.pressed = HelpButtonPressed
QuitButton.pressed = QuitButtonPressed

NewGameButton.Interactive = True
LoadGameButton.Interactive = True
SettingsButton.Interactive = True
HelpButton.Interactive = True
QuitButton.Interactive = True

BestDungeonRunsFrame.Interactive = True
AchievementsFrame.Interactive = True