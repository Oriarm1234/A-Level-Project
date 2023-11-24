import pygame
from Definitions import *
import json

overlayManager = None

def init(images, gameScreen, screenSize):
    global  overlayManager  ,\
            mainMenu        ,\
            newGameMenu     ,\
            settingsMenu    ,\
            helpMenu        ,\
            loadGameMenu    

    

    overlayManager = OverlayManager(
        "overlayManager", (1060,600), (0, 0), [pygame.SRCALPHA], []
    )


    def pre_draw(self, *args, **kwargs):
        self._screen.fill((0, 0, 0, 0))


    def pre_update(overlayManager, *args, **kwargs):
        mousePressed = kwargs.get("mousePressed", [False, False, False, False, False])
        keysPressed = kwargs.get("keysPressed", [])

        if mousePressed[0] and not overlayManager.get_state_event("mousePressed-0"):
            overlayManager.set_state_event("mousePressed-0", True)
            mousePos = kwargs.get("mousePos", (0, 0))

            overlays = overlayManager.get_visible_overlays()
            pressed=False
            for overlay in overlays:
                elements = overlay.get_elements_at_pos(*mousePos, onlyInteractive=True, onlyVisible=True)
                
                if elements != []:
                    element = elements[-1]
                    
                    if not pressed:
                        overlay.highlighted = element
                        
                    if (not pressed) and element.pressed != None:
                        
                        element.pressed(element, mousePos)
                        pressed = True
                    
            for overlay in overlays:
                elements = overlay.elements
                
                for element in elements:
                    if pressed and element.other_element_pressed is not None and element != overlay.highlighted:
                        element.other_element_pressed(element, mousePos, overlay.highlighted)
                        
                    
                        
                    
        elif mousePressed[0] and overlayManager.get_state_event("mousePressed-0"):
            mousePos = kwargs.get("mousePos", (0, 0))

            overlays = overlayManager.get_visible_overlays()

            for overlay in overlays:
                if overlay.highlighted != None and overlay.highlighted.held_down != None:
                    overlay.highlighted.held_down(overlay.highlighted, mousePos)

        elif not mousePressed[0] and overlayManager.get_state_event("mousePressed-0"):
            overlayManager.set_state_event("mousePressed-0", False)
            mousePos = kwargs.get("mousePos", (0, 0))

            overlays = overlayManager.get_visible_overlays()

            for overlay in overlays:
                if overlay.highlighted != None:
                    element = overlay.highlighted
                    overlay.highlighted = None

                    if element.released != None:
                        element.released(element, mousePos)
                        break

        if keysPressed != []:
            if keysPressed[pygame.K_ESCAPE] and not overlayManager.get_state_event(
                "k_escape"
            ):
                overlayManager.set_state_event("k_escape", True)
                visibleOverlays = overlayManager.get_visible_overlays()
                mainMenu = overlayManager.get_overlay_by_name("mainMenu")
                if mainMenu in visibleOverlays:
                    pygame.quit()
                    quit()
                else:
                    for overlay in visibleOverlays:
                        if overlay.name in [
                            "helpMenu",
                            "loadGameMenu",
                            "settingsMenu",
                            "newGameMenu",
                        ]:
                            
                            overlayManager.set_overlay_visible(overlay, False)
                    overlayManager.set_overlay_visible(mainMenu, True)

            elif not keysPressed[pygame.K_ESCAPE]:
                overlayManager.set_state_event("k_escape", False)


    overlayManager.pre_draw = pre_draw
    overlayManager.pre_update = pre_update
    
    MainMenu.init(images)
    NewGameMenu.init(images)
    LoadGameMenu.init(images)
    Settings.init(images)
    Help.init(images)
    

    mainMenu = MainMenu.mainMenu(screenSize)
    newGameMenu = NewGameMenu.newGameMenu(screenSize)
    settingsMenu = Settings.settingsMenu(screenSize)
    helpMenu = Help.helpMenu(screenSize)
    loadGameMenu = LoadGameMenu.loadGameMenu(screenSize)
    
    overlayManager.set_overlay_visible(gameScreen)
    overlayManager.append_overlay(gameScreen)
    overlayManager.append_overlay(mainMenu)
    overlayManager.append_overlay(newGameMenu)
    overlayManager.append_overlay(settingsMenu)
    overlayManager.append_overlay(helpMenu)
    overlayManager.append_overlay(loadGameMenu)
    
    



def StartMenu(screen, screenSize = (1060, 600), settings={}):
    
    assert overlayManager, "OverlayManager doesn't exist, have you initialised the menu? (MenuLoader.init(*))"
    
    overlayManager.size = screenSize
    
    brightness = settings.get("brightness", 100)

    checkBrightness = brightness

    brightnessLayer = pygame.Surface(screenSize, pygame.SRCALPHA)
    brightnessLayer.fill((0, 0, 0, 200 - brightness * 2))
    
    
    visibleOverlays = overlayManager.get_visible_overlays()
    mainMenu = overlayManager.get_overlay_by_name("mainMenu")

    for overlay in visibleOverlays:
                        if overlay.name not in [
                            "mainMenu",
                            "gameScreen"
                        ]:
                            
                            overlayManager.set_overlay_visible(overlay, False)

    overlayManager.set_overlay_visible(mainMenu)
    
    
    
    
    while True:
        
        if brightness != checkBrightness:
            checkBrightness = brightness
            brightnessLayer = pygame.Surface(screenSize, pygame.SRCALPHA)
            brightnessLayer.fill((0, 0, 0, 200 - brightness * 2))
        
        
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        overlayManager.update(
            keysPressed=pygame.key.get_pressed(),
            keysFocused=pygame.key.get_focused(),
            mousePressed=pygame.mouse.get_pressed(),
            mouseFocused=pygame.mouse.get_focused(),
            mousePos=pygame.mouse.get_pos(),
            mouseRel=pygame.mouse.get_rel(),
            events = events
        )

        screen.fill((255, 255, 255))
        screen.blit(overlayManager.screen, (0, 0))

        screen.blit(brightnessLayer, (0, 0))
        
        
        
        pygame.display.update() 