from InteractiveOverlays import *
from OverlayDefinitions.ExtraElements import *
import pygame

settingsMenu = Overlay(
    ("SettingsMenu"), (1060, 600), (0, 0), None, [pygame.SRCALPHA], []
)

settingsControls = Overlay(
    ("SettingsControls"), (1060, 300), (0, 300), None, [pygame.SRCALPHA], [],
)

settingsVideo = Overlay(
    ("SettingsVideo"), (1060, 300), (0, 300), None, [pygame.SRCALPHA], []
)

settingsAudio = Overlay(
    ("SettingsAudio"), (1060, 300), (0, 300), None, [pygame.SRCALPHA], []
)

SettingOptions = {"Controls":settingsControls, "Video":settingsVideo, "Audio":settingsAudio}

# ---------------------------------------------------------------------------- #
#                                 Settings Menu                                #
# ---------------------------------------------------------------------------- #
SettingsLabel = Text(
    "Settings",
    "copperplategothic",
    64,
    (20, 20, 20),
    (530, 100),
    "MainMenuLabel",
    settingsMenu,
)

LIGHT_BLUE = (92, 225, 230)
DARK_BLUE  = (82, 113, 255)

SettingsLabel.align_to_center()
SettingsLabel.set_underline(True)

spacingForTitleOptions = 8
OptionBoxesPadding = 8
OptionBoxY = SettingsLabel.y+SettingsLabel.Hitbox.h+spacingForTitleOptions

OptionBoxControlsText = Text("Controls", "copperplategothic", 32, (20,20,20), (530, OptionBoxY+OptionBoxesPadding/2), "OptionBox-Controls-Text", settingsMenu)
OptionBoxAudioText = Text("Audio", "copperplategothic", 32, (20,20,20), (530, OptionBoxY+OptionBoxesPadding/2), "OptionBox-Audio-Text", settingsMenu)
OptionBoxVideoText = Text("Video", "copperplategothic", 32, (20,20,20), (530, OptionBoxY+OptionBoxesPadding/2), "OptionBox-Video-Text", settingsMenu)

boxWidth = max(max(OptionBoxAudioText.Hitbox.w, OptionBoxControlsText.Hitbox.w), OptionBoxVideoText.Hitbox.w) + OptionBoxesPadding

OptionBoxControlsRect = Rectangle("OptionBox-Controls-Rect", 
                                  (530-boxWidth,OptionBoxY), 
                                  (boxWidth, 32+OptionBoxesPadding), 
                                  settingsMenu, 
                                  (92, 225, 230))


OptionBoxAudioRect = Rectangle("OptionBox-Audio-Rect", 
                                  (530+boxWidth,OptionBoxY), 
                                  (boxWidth, 32+OptionBoxesPadding), 
                                  settingsMenu, 
                                  (92, 225, 230))


OptionBoxVideoRect = Rectangle("OptionBox-Video-Rect", 
                                  (530,OptionBoxY), 
                                  (boxWidth, 32+OptionBoxesPadding), 
                                  settingsMenu, 
                                  (92, 225, 230))


OptionBoxControlsRect.align_to_bottom_middle()
OptionBoxAudioRect.align_to_bottom_middle()
OptionBoxVideoRect.align_to_bottom_middle()

OptionBoxControlsText.align_to_bottom_middle()
OptionBoxAudioText.align_to_bottom_middle()
OptionBoxVideoText.align_to_bottom_middle()

OptionBoxControlsText.bring_to_front()
OptionBoxAudioText.bring_to_front()
OptionBoxVideoText.bring_to_front()

OptionBoxControlsText._x -= boxWidth
OptionBoxAudioText._x += boxWidth


OptionBoxCollision = Group("OptionBoxCollision", (530-boxWidth,OptionBoxY), settingsMenu, (OptionBoxControlsRect,
                                                                                           OptionBoxAudioRect,
                                                                                           OptionBoxVideoRect,
                                                                                           OptionBoxControlsText,
                                                                                           OptionBoxAudioText,
                                                                                           OptionBoxVideoText), True)

OptionBoxCollision.Interactive = True

AllNames = ["Controls", "Video", "Audio"]


#Setting Default Colours

for name in AllNames:
    elementRectPressed:Rectangle = OptionBoxCollision._elements.get(f"OptionBox-{name}-Rect", None)
    elementTextPressed:Text      = OptionBoxCollision._elements.get(f"OptionBox-{name}-Text", None)
    
    if elementRectPressed != None and elementTextPressed is not None:
        elementRectPressed.Colour = DARK_BLUE  if "Controls" != name else LIGHT_BLUE
        elementTextPressed.set_underline("Controls" != name)
        
        
#-----------------------------------------------------------------
        

def OptionBoxPressed(self:Group, *args, **kwargs):
    mx,my = args[0]
    rx    = mx - self.x #relative X position to object
    px    = rx / self.width #percent x relative to object
    
    elementNamePressed = None
    
    
    
    if 1/3 > px > 0:
        elementNamePressed = AllNames[0]
    elif 2/3 > px > 1/3:
        elementNamePressed = AllNames[1]
    elif 1 > px > 2/3:
        elementNamePressed = AllNames[2]
    
    for name in AllNames:
        elementRectPressed:Rectangle = self._elements.get(f"OptionBox-{name}-Rect", None)
        elementTextPressed:Text      = self._elements.get(f"OptionBox-{name}-Text", None)
        
        if elementRectPressed != None and elementTextPressed is not None:
            elementRectPressed.Colour = DARK_BLUE  if elementNamePressed != name else LIGHT_BLUE
            elementTextPressed.set_underline(elementNamePressed != name)
            
            
            if SettingOptions[name].Parent is not None:
                SettingOptions[name].Parent.SetOverlayVisible(
                    SettingOptions[name], 
                    elementNamePressed == name)
        

        
OptionBoxCollision.pressed = OptionBoxPressed    



OptionBoxAudioRect = Rectangle("OptionBox-Audio-Rect", 
                                  (0,0), 
                                  (boxWidth, 32+OptionBoxesPadding), 
                                  settingsControls, 
                                  (92, 225, 230))

OptionBoxAudioRect = Rectangle("OptionBox-Audio-Rect", 
                                  (530+boxWidth,0), 
                                  (boxWidth, 32+OptionBoxesPadding), 
                                  settingsVideo, 
                                  (92, 225, 10))