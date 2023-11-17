from InteractiveOverlays import *
import pygame

def init(images):
    
    global mainMenu
    
    mainMenu = Overlay("MainMenu",
                        (1060,600),
                        [0,0],
                        None,
                        [pygame.SRCALPHA],
                        [])


    newGameButton = StillImage(
        "newGameButton",
        images.get("button",None),
        (530,200),
        mainMenu,
        imageName="button")

    newGameLabel = Text(
        "New Run", 
        "copperplategothic", 
        32, 
        (0,0,0), 
        (530,200), 
        "NewGameLabel",
        mainMenu)

    loadGameButton = StillImage(
        "loadGameButton",
        images.get("button",None),
        (530,200),
        mainMenu,
        imageName="button")

    loadGameLabel = Text(
        "Load Run", 
        "copperplategothic", 
        32, 
        (0,0,0), 
        (530,200), 
        "loadGameLabel",
        mainMenu)

    settingsButton = StillImage(
        "settingsButton",
        images.get("button",None),
        (530,200),
        mainMenu,
        imageName="button")

    settingsLabel = Text(
        "Settings", 
        "copperplategothic", 
        32, 
        (0,0,0), 
        (530,200), 
        "settingsLabel",
        mainMenu)

    helpButton = StillImage(
        "helpButton",
        images.get("button",None),
        (530,200),
        mainMenu,
        imageName="button")

    helpLabel = Text(
        "Help", 
        "copperplategothic", 
        32, 
        (0,0,0), 
        (530,200), 
        "helpLabel",
        mainMenu)

    quitButton = StillImage(
        "quitButton",
        images.get("button",None),
        (530,200),
        mainMenu,
        imageName="button")

    quitLabel = Text(
        "Quit", 
        "copperplategothic", 
        32, 
        (0,0,0), 
        (530,200), 
        "quitLabel",
        mainMenu)

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

    mainMenuLabel = Text(
        "Main Menu", 
        "copperplategothic", 
        64, 
        (20,20,20), 
        (530,100), 
        "mainMenuLabel",
        mainMenu)

    mainMenuLabel.align_to_center()
    mainMenuLabel.set_underline(True)



    bestDungeonRunsFrame = StillImage("bestDungeonRunsFrame", images.get("button",None), (20,20), mainMenu, imageName="button")
    bestDungeonRunsFrame.resize_image(180,60)

    bestDungeonRunsLabel = Text(
        "Best Dungeon Runs", 
        "copperplategothic", 
        16, 
        (20,20,20), 
        (110,50), 
        "bestDungeonRunsLabel",
        mainMenu)
    bestDungeonRunsLabel.align_to_center()
    bestDungeonRunsLabel.set_underline(True)

    achievementsFrame = StillImage("achievementsFrame", images.get("button",None), (1040,20), mainMenu, imageName="button")
    achievementsFrame.resize_image(180,60)
    achievementsFrame.align_to_bottom_left()

    achievementsLabel = Text(
        "achievements",  
        "copperplategothic", 
        16, 
        (20,20,20), 
        (950,50), 
        "achievementsLabel",
        mainMenu)
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
    
        newGameMenu = mainMenu._parent.get_overlay_by_name("newGameMenu")
        
        if newGameMenu != None:
            
            mainMenu._parent.set_overlay_visible(mainMenu, False)
            mainMenu._parent.set_overlay_visible(newGameMenu, True)

    @button_released_wrapper
    def load_game_button_released(self, *args, **kwargs):
    
        loadGameMenu = mainMenu._parent.get_overlay_by_name("loadGameMenu")
        
        if loadGameMenu != None:
            
            mainMenu._parent.set_overlay_visible(mainMenu, False)
            mainMenu._parent.set_overlay_visible(loadGameMenu, True)

    @button_released_wrapper
    def settings_button_released(self, *args, **kwargs):
    
        settingsMenu = mainMenu._parent.get_overlay_by_name("settingsMenu")
        
        if settingsMenu != None:
            
            mainMenu._parent.set_overlay_visible(mainMenu, False)
            mainMenu._parent.set_overlay_visible(settingsMenu, True) 

    @button_released_wrapper
    def help_button_released(self, *args, **kwargs):
    
        helpMenu = mainMenu._parent.get_overlay_by_name("helpMenu")
        
        if helpMenu != None:
            
            mainMenu._parent.set_overlay_visible(mainMenu, False)
            mainMenu._parent.set_overlay_visible(helpMenu, True)

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