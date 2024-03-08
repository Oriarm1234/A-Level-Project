from ..InteractiveOverlays import (Text,
                                   Rectangle,
                                   Group,
                                   Overlay)

from ..ExtraElements import (DropdownList,
                             Slider,
                             Tickbox,
                             TextInputBox,
                             ExtraElementsInit)

extraElements = {"DropdownList":DropdownList, "Slider":Slider, "Tickbox":Tickbox,"TextInputBox":TextInputBox}

import json
import pygame

with open("Settings.json","r") as f:
    settings = json.load(f)
    print(settings)
images = {}

def init(imageObjects = {}):

    global images
    images = imageObjects
    
    ExtraElementsInit(images)
    
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
    
    settingsDisclaimer = Text("These settings are the default for each save. If you change the settings in a save it wont affect these.",
                              "copperplategothic", 16, (0,0,0), (530, 100), "SettingsDisclaimer", self)
    settingsDisclaimer.align_to_bottom_middle()
    settingsDisclaimer.set_underline(True)

    LIGHT_BLUE = (92, 225, 230)
    DARK_BLUE  = (82, 113, 255)

    settingsLabel.align_to_top_middle()
    settingsLabel.set_underline(True)

    spacingForTitleOptions = 8
    optionBoxesPadding = 8
    optionBoxY = settingsDisclaimer.y + settingsDisclaimer.hitbox.h + spacingForTitleOptions

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


    optionBoxes = []
    allNames = ["controls", "video", "audio"]
    
    
    
    
    optionBoxCollision = Group("optionBoxCollision", (530-boxWidth,optionBoxY), self, (optionBoxControlsRect,
                                                                                            optionBoxAudioRect,
                                                                                            optionBoxVideoRect,
                                                                                            optionBoxControlsText,
                                                                                            optionBoxAudioText,
                                                                                            optionBoxVideoText), True)
    optionBoxCollision.interactive = True
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
        
        amount = len(self.elements)//2 #Halfed because the group has 2 elements for every option
        
        index = min(amount-1,max(0,int(px*(amount))))
        
        
        elementNamePressed = allNames[index]
        
        for name in allNames:
            elementRectPressed:Rectangle = self._elements.get(f"optionBox-{name}-rect", None)
            elementTextPressed:Text      = self._elements.get(f"optionBox-{name}-text", None)
            
            if elementRectPressed != None and elementTextPressed is not None:
                elementRectPressed.colour = DARK_BLUE  if elementNamePressed != name else LIGHT_BLUE
                elementTextPressed.set_underline(elementNamePressed != name)
                
                
                if settingOptions[name].parent is not None:
                    settingOptions[name].visible = elementNamePressed == name
            

            
    optionBoxCollision.pressed = option_box_pressed    




    
    
    
    for settingType in settings:
        
        if settingType not in settingOptions:
            continue
        
        overlay = settingOptions[settingType]
        
        overlaySettings = settings[settingType]
        
        ix, iy = 0,0
        heightGap = 20
        
        
        for setting in overlaySettings:
            settingData = overlaySettings[setting]
            
            
            settingLabel = Text(setting, "copperplategothic", 32, (20,20,20), (100,optionBoxControlsRect.y+optionBoxControlsRect.hitbox.h+10+iy), setting+"-Label", self)
            settingInteractive = None
            
            if settingData["Type"] == "Slider":
                settingX = screenSize[1]-100
                settingY = optionBoxControlsRect.y+optionBoxControlsRect.hitbox.h+10+iy
                settingInteractive = Slider((settingX,settingY), setting+"-Interactive", self, settingData["MinValue"], settingData["MaxValue"], settingData["RoundDigits"])
                settingInteractive.set_value(settingInteractive,settingData["CurrentValue"])
                settingInteractive.align_to_bottom_left()
                
                overlay.append_element(settingInteractive)
                
            elif settingData["Type"] == "DropdownList":
                settingX = screenSize[1]-100
                settingY = optionBoxControlsRect.y+optionBoxControlsRect.hitbox.h+10+iy
                settingInteractive = DropdownList(setting+"-Interactive", (settingX,settingY), self, settingData["Options"], "copperplategothic", 24, (20,20,20),settingData["allowNothing"],(80,80,80),(140,140,140),3,2)
                settingInteractive.set_value(settingInteractive,settingData["CurrentValue"])
                settingInteractive.align_to_bottom_left()
                
                overlay.append_element(settingInteractive)
            
            overlay.append_element(settingLabel)
            iy += settingLabel.hitbox.h + heightGap
            
            

    
    
    
    
    return self