from ..InteractiveOverlays import (Text,
                                   Rectangle,
                                   Group,
                                   Overlay)

from ..ExtraElements import (DropdownList,
                             Slider,
                             Tickbox,
                             TextInputBox)

import pygame

images = {}

def init(imageObjects = {}):

    global images
    images = imageObjects
    
def settingsMenu(screenSize):

    self = Overlay(
        ("settingsMenu"), screenSize, (0, 0), None, [pygame.SRCALPHA], []
    )

    settingsControls = Group("settingsControl", (0,300), self, [], True)

    settingsVideo =  Group("settingsVideo", (0,300), self, [], False)

    settingsAudio =  Group("settingsAudio", (0,300), self, [], False)

    settingOptions = {"controls":settingsControls, "video":settingsVideo, "audio":settingsAudio}

    # ---------------------------------------------------------------------------- #
    #                                 settings Menu                                #
    # ---------------------------------------------------------------------------- #
    settingsLabel = Text(
        "settings",
        "copperplategothic",
        64,
        (20, 20, 20),
        (530, 100),
        "mainMenuLabel",
        self,
    )

    LIGHT_BLUE = (92, 225, 230)
    DARK_BLUE  = (82, 113, 255)

    settingsLabel.align_to_center()
    settingsLabel.set_underline(True)

    spacingForTitleOptions = 8
    optionBoxesPadding = 8
    optionBoxY = settingsLabel.y+settingsLabel.hitbox.h+spacingForTitleOptions

    optionBoxControlsText = Text("controls", "copperplategothic", 32, (20,20,20), (530, optionBoxY+optionBoxesPadding/2), "optionBox-controls-text", self)
    optionBoxAudioText = Text("audio", "copperplategothic", 32, (20,20,20), (530, optionBoxY+optionBoxesPadding/2), "optionBox-audio-text", self)
    optionBoxVideoText = Text("video", "copperplategothic", 32, (20,20,20), (530, optionBoxY+optionBoxesPadding/2), "optionBox-video-text", self)

    boxWidth = max(max(optionBoxAudioText.hitbox.w, optionBoxControlsText.hitbox.w), optionBoxVideoText.hitbox.w) + optionBoxesPadding

    optionBoxControlsRect = Rectangle("optionBox-controls-rect", 
                                    (530-boxWidth,optionBoxY), 
                                    (boxWidth, 32+optionBoxesPadding), 
                                    self, 
                                    (92, 225, 230))


    optionBoxAudioRect = Rectangle("optionBox-audio-rect", 
                                    (530+boxWidth,optionBoxY), 
                                    (boxWidth, 32+optionBoxesPadding), 
                                    self, 
                                    (92, 225, 230))


    optionBoxVideoRect = Rectangle("optionBox-video-rect", 
                                    (530,optionBoxY), 
                                    (boxWidth, 32+optionBoxesPadding), 
                                    self, 
                                    (92, 225, 230))


    optionBoxControlsRect.align_to_bottom_middle()
    optionBoxAudioRect.align_to_bottom_middle()
    optionBoxVideoRect.align_to_bottom_middle()

    optionBoxControlsText.align_to_bottom_middle()
    optionBoxAudioText.align_to_bottom_middle()
    optionBoxVideoText.align_to_bottom_middle()

    optionBoxControlsText.bring_to_front()
    optionBoxAudioText.bring_to_front()
    optionBoxVideoText.bring_to_front()

    optionBoxControlsText._x -= boxWidth
    optionBoxAudioText._x += boxWidth


    optionBoxCollision = Group("optionBoxCollision", (530-boxWidth,optionBoxY), self, (optionBoxControlsRect,
                                                                                            optionBoxAudioRect,
                                                                                            optionBoxVideoRect,
                                                                                            optionBoxControlsText,
                                                                                            optionBoxAudioText,
                                                                                            optionBoxVideoText), True)

    optionBoxCollision.interactive = True

    allNames = ["controls", "video", "audio"]


    #Setting Default Colours

    for name in allNames:
        elementRectPressed:Rectangle = optionBoxCollision._elements.get(f"optionBox-{name}-rect", None)
        elementTextPressed:Text      = optionBoxCollision._elements.get(f"optionBox-{name}-text", None)
        
        if elementRectPressed != None and elementTextPressed is not None:
            elementRectPressed.colour = DARK_BLUE  if "controls" != name else LIGHT_BLUE
            elementTextPressed.set_underline("controls" != name)
            
            
    #-----------------------------------------------------------------
            

    def option_box_pressed(self:Group, *args, **kwargs):
        mx,my = args[0]
        rx    = mx - self.x #relative X position to object
        px    = rx / self.width #percent x relative to object
        
        elementNamePressed = None
        
        
        
        if 1/3 > px > 0:
            elementNamePressed = allNames[0]
        elif 2/3 > px > 1/3:
            elementNamePressed = allNames[1]
        elif 1 > px > 2/3:
            elementNamePressed = allNames[2]
        
        for name in allNames:
            elementRectPressed:Rectangle = self._elements.get(f"optionBox-{name}-rect", None)
            elementTextPressed:Text      = self._elements.get(f"optionBox-{name}-text", None)
            
            if elementRectPressed != None and elementTextPressed is not None:
                elementRectPressed.colour = DARK_BLUE  if elementNamePressed != name else LIGHT_BLUE
                elementTextPressed.set_underline(elementNamePressed != name)
                
                
                if settingOptions[name].parent is not None:
                    settingOptions[name].visible = elementNamePressed == name
            

            
    optionBoxCollision.pressed = option_box_pressed    



    optionBoxAudioRect = Rectangle("optionBox-audio-rect", 
                                    (0,0), 
                                    (boxWidth, 32+optionBoxesPadding), 
                                    settingsControls, 
                                    (92, 225, 230))

    optionBoxAudioRect = Rectangle("optionBox-audio-rect", 
                                    (530+boxWidth,0), 
                                    (boxWidth, 32+optionBoxesPadding), 
                                    settingsVideo, 
                                    (92, 225, 10))
    
    return self