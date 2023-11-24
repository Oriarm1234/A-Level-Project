from ..InteractiveOverlays import (StillImage,
                                   Text,
                                   Overlay)
import pygame

images = {}

def init(imageObjects = {}):

    global images
    images = imageObjects

def mainMenu(screenSize):
    
    self = Overlay("mainMenu",
                        screenSize,
                        [0,0],
                        None,
                        [pygame.SRCALPHA],
                        [])


    newGameButton = StillImage(
        "newGameButton",
        images.get("button",None),
        (530,200),
        self,
        imageName="button")

    newGameLabel = Text(
        "New Run", 
        "copperplategothic", 
        32, 
        (0,0,0), 
        (530,200), 
        "NewGameLabel",
        self)

    loadGameButton = StillImage(
        "loadGameButton",
        images.get("button",None),
        (530,200),
        self,
        imageName="button")

    loadGameLabel = Text(
        "Load Run", 
        "copperplategothic", 
        32, 
        (0,0,0), 
        (530,200), 
        "loadGameLabel",
        self)

    settingsButton = StillImage(
        "settingsButton",
        images.get("button",None),
        (530,200),
        self,
        imageName="button")

    settingsLabel = Text(
        "Settings", 
        "copperplategothic", 
        32, 
        (0,0,0), 
        (530,200), 
        "settingsLabel",
        self)

    helpButton = StillImage(
        "helpButton",
        images.get("button",None),
        (530,200),
        self,
        imageName="button")

    helpLabel = Text(
        "Help", 
        "copperplategothic", 
        32, 
        (0,0,0), 
        (530,200), 
        "helpLabel",
        self)

    quitButton = StillImage(
        "quitButton",
        images.get("button",None),
        (530,200),
        self,
        imageName="button")

    quitLabel = Text(
        "Quit", 
        "copperplategothic", 
        32, 
        (0,0,0), 
        (530,200), 
        "quitLabel",
        self)

    newGameButton.align_to_center()
    newGameLabel.align_to_center()
    loadGameButton.align_to_center()
    loadGameLabel.align_to_center()
    settingsButton.align_to_center()
    settingsLabel.align_to_center()
    helpButton.align_to_center()
    helpLabel.align_to_center()
    quitButton.align_to_center()
    quitLabel.align_to_center()


    loadGameButton.resize_image(*loadGameLabel.hitbox.size)
    loadGameButton.resize_image_by_amount(40,20)


    newGameButton.resize_image(*loadGameLabel.hitbox.size)
    settingsButton.resize_image(*loadGameLabel.hitbox.size)
    helpButton.resize_image(*loadGameLabel.hitbox.size)
    quitButton.resize_image(*loadGameLabel.hitbox.size)
    newGameButton.resize_image_by_amount(40,20)
    settingsButton.resize_image_by_amount(40,20)
    helpButton.resize_image_by_amount(40,20)
    quitButton.resize_image_by_amount(40,20)

    spacing = 16

    loadGameLabel.y = newGameButton.hitbox.h + newGameButton._y + spacing
    loadGameButton.y = newGameButton.hitbox.h + newGameButton._y + spacing
    settingsLabel.y = loadGameButton.hitbox.h + loadGameButton._y + spacing
    settingsButton.y = loadGameButton.hitbox.h + loadGameButton._y + spacing
    helpLabel.y =  settingsButton.hitbox.h + settingsButton._y + spacing
    helpButton.y = settingsButton.hitbox.h + settingsButton._y + spacing
    quitLabel.y =  helpButton.hitbox.h + helpButton._y + spacing
    quitButton.y = helpButton.hitbox.h + helpButton._y + spacing

    selfLabel = Text(
        "Main Menu", 
        "copperplategothic", 
        64, 
        (20,20,20), 
        (530,100), 
        "selfLabel",
        self)

    selfLabel.align_to_center()
    selfLabel.set_underline(True)



    bestDungeonRunsFrame = StillImage("bestDungeonRunsFrame", images.get("button",None), (20,20), self, imageName="button")
    bestDungeonRunsFrame.resize_image(180,60)

    bestDungeonRunsLabel = Text(
        "Best Dungeon Runs", 
        "copperplategothic", 
        16, 
        (20,20,20), 
        (110,50), 
        "bestDungeonRunsLabel",
        self)
    bestDungeonRunsLabel.align_to_center()
    bestDungeonRunsLabel.set_underline(True)

    achievementsFrame = StillImage("achievementsFrame", images.get("button",None), (1040,20), self, imageName="button")
    achievementsFrame.resize_image(180,60)
    achievementsFrame.align_to_bottom_left()

    achievementsLabel = Text(
        "achievements",  
        "copperplategothic", 
        16, 
        (20,20,20), 
        (950,50), 
        "achievementsLabel",
        self)
    achievementsLabel.align_to_center()
    achievementsLabel.set_underline(True)


    def button_pressed_wrapper(function):
        def button_pressed(self, *args, **kwargs):
            result = function(self, *args, **kwargs)
            self.tempIm = self.image
            self.baseImage = pressedButtonImage
            self.resize_image(*self.tempIm.get_size())
            return result
        return button_pressed

    def button_released_wrapper(function):
        def button_released(self, *args, **kwargs):
            result = function(self, *args, **kwargs)
            self.baseImage = self.tempIm
            self.resize_image(*self.tempIm.get_size())
            return result
        return button_released



    @button_released_wrapper
    def new_game_button_released(self, *args, **kwargs):
    
        overlayManager = self._parent._parent
        newGameMenu = overlayManager.get_overlay_by_name("newGameMenu")
        
        if newGameMenu != None:
            
            overlayManager.set_overlay_visible(self._parent, False)
            overlayManager.set_overlay_visible(newGameMenu, True)

    @button_released_wrapper
    def load_game_button_released(self, *args, **kwargs):
    
        overlayManager = self._parent._parent
        loadGameMenu = overlayManager.get_overlay_by_name("loadGameMenu")
        
        if loadGameMenu != None:
            
            overlayManager.set_overlay_visible(self._parent, False)
            overlayManager.set_overlay_visible(loadGameMenu, True)

    @button_released_wrapper
    def settings_button_released(self, *args, **kwargs):
        
        overlayManager = self._parent._parent
        settingsMenu = overlayManager.get_overlay_by_name("settingsMenu")
        
        if settingsMenu != None:
            
            overlayManager.set_overlay_visible(self._parent, False)
            overlayManager.set_overlay_visible(settingsMenu, True) 

    @button_released_wrapper
    def help_button_released(self, *args, **kwargs):
    
        overlayManager = self._parent._parent
        helpMenu = overlayManager.get_overlay_by_name("helpMenu")
        
        if helpMenu != None:
            
            overlayManager.set_overlay_visible(self._parent, False)
            overlayManager.set_overlay_visible(helpMenu, True)

    @button_released_wrapper
    def quit_button_released(self, *args, **kwargs):
        pygame.quit()
        quit()

    pressedButtonImage = images.get("pressed_button",None)



    newGameButton.released = new_game_button_released
    loadGameButton.released = load_game_button_released
    settingsButton.released = settings_button_released
    helpButton.released = help_button_released
    quitButton.released = quit_button_released

    newGameButton.pressed = button_pressed_wrapper(lambda self,*args,**kwargs:None)
    loadGameButton.pressed = button_pressed_wrapper(lambda self,*args,**kwargs:None)
    helpButton.pressed = button_pressed_wrapper(lambda self,*args,**kwargs:None)
    quitButton.pressed = button_pressed_wrapper(lambda self,*args,**kwargs:None)
    settingsButton.pressed = button_pressed_wrapper(lambda self,*args,**kwargs:None)

    newGameButton.interactive = True
    loadGameButton.interactive = True
    settingsButton.interactive = True
    helpButton.interactive = True
    quitButton.interactive = True

    bestDungeonRunsFrame.interactive = True
    achievementsFrame.interactive = True
    
    return self