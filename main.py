import pygame
from InteractiveOverlays import *
from OverlayDefinitions import *
import json

settings = json.load(open("Settings.json", "r"))

settings["brightness"] = brightness = settings.get("brightness", 100)

brightnessLayer = pygame.Surface((1060, 600), pygame.SRCALPHA)
brightnessLayer.fill((0, 0, 0, 200 - brightness * 2))

overlayManager = OverlayManager(
    "OverlayManager", (1060, 600), (0, 0), [pygame.SRCALPHA], []
)


def preDraw(self, *args, **kwargs):
    self._screen.fill((0, 0, 0, 0))


def preUpdate(overlayManager, *args, **kwargs):
    mousePressed = kwargs.get("mousePressed", [False, False, False, False, False])
    keysPressed = kwargs.get("keysPressed", [])

    if mousePressed[0] and not overlayManager.getStateEvent("mousePressed-0"):
        overlayManager.setStateEvent("mousePressed-0", True)
        mousePos = kwargs.get("mousePos", (0, 0))

        overlays = overlayManager.getVisibleOverlays()
        pressed=False
        for overlay in overlays:
            elements = overlay.GetElementsAtPos(*mousePos, onlyInteractive=True, onlyVisible=True)
            
            if elements != []:
                element = elements[-1]
                
                if not pressed:
                    overlay.Highlighted = element
                    
                if (not pressed) and element.pressed != None:
                    
                    element.pressed(element, mousePos)
                    pressed = True
                
        for overlay in overlays:
            elements = overlay.Elements
            
            for element in elements:
                if pressed and element.other_element_pressed is not None and element != overlay.Highlighted:
                    element.other_element_pressed(element, mousePos, overlay.Highlighted)
                    
                
                    
                
    elif mousePressed[0] and overlayManager.getStateEvent("mousePressed-0"):
        mousePos = kwargs.get("mousePos", (0, 0))

        overlays = overlayManager.getVisibleOverlays()

        for overlay in overlays:
            if overlay.Highlighted != None and overlay.Highlighted.held_down != None:
                overlay.Highlighted.held_down(overlay.Highlighted, mousePos)

    elif not mousePressed[0] and overlayManager.getStateEvent("mousePressed-0"):
        overlayManager.setStateEvent("mousePressed-0", False)
        mousePos = kwargs.get("mousePos", (0, 0))

        overlays = overlayManager.getVisibleOverlays()

        for overlay in overlays:
            if overlay.Highlighted != None:
                element = overlay.Highlighted
                overlay.Highlighted = None

                if element.released != None:
                    element.released(element, mousePos)
                    break

    if keysPressed != []:
        if keysPressed[pygame.K_ESCAPE] and not overlayManager.getStateEvent(
            "k_escape"
        ):
            overlayManager.setStateEvent("k_escape", True)
            visibleOverlays = overlayManager.getVisibleOverlays()
            mainMenu = overlayManager.getOverlayByName("MainMenu")
            if mainMenu in visibleOverlays:
                pygame.quit()
                quit()
            else:
                for overlay in visibleOverlays:
                    if overlay.Name in [
                        "HelpMenu",
                        "LoadGameMenu",
                        "SettingsMenu",
                        "NewGameMenu",
                    ]:
                        
                        overlayManager.SetOverlayVisible(overlay, False)
                overlayManager.SetOverlayVisible(mainMenu, True)

        elif not keysPressed[pygame.K_ESCAPE]:
            overlayManager.setStateEvent("k_escape", False)


overlayManager.preDraw = preDraw
overlayManager.preUpdate = preUpdate

overlayManager.appendOverlay(gameScreen)
overlayManager.appendOverlay(mainMenu)
overlayManager.appendOverlay(newGameMenu)
overlayManager.appendOverlay(settingsMenu)
overlayManager.appendOverlay(settingsControls)
overlayManager.appendOverlay(settingsVideo)
overlayManager.appendOverlay(settingsAudio)
overlayManager.appendOverlay(helpMenu)
overlayManager.appendOverlay(loadGameMenu)



screen = pygame.display.set_mode((1060, 600))
screen.fill((255, 255, 255))

overlayManager.SetOverlayVisible(mainMenu)
overlayManager.SetOverlayVisible(gameScreen)
while True:
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
    screen.blit(overlayManager.Screen, (0, 0))

    screen.blit(brightnessLayer, (0, 0))
    
    
    
    pygame.display.update() 