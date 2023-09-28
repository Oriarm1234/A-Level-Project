from InteractiveOverlays import *
import pygame
settingsMenu = Overlay(("SettingsMenu"),
                      (1060,600),
                      (0,0),
                      None,
                      [pygame.SRCALPHA],
                      [])

Background = StillImage("background", pygame.image.load("Background.png"), (0,0), settingsMenu)
Background.crop_image(0,150, 1060, 600)
Background.move_backwards(100)

SettingsLabel = Text(
    "Settings", 
    "copperplategothic", 
    64, 
    (20,20,20), 
    (530,100), 
    "MainMenuLabel",
    settingsMenu)

SettingsLabel.align_to_center()
SettingsLabel.set_underline(True)

print(SettingsLabel.__dict__ == SettingsLabel.copy().__dict__)

r = Rectangle("background", (530,300), (420,21), settingsMenu, (100,100,100))
l = Line("line", (330, 299), (730, 299), settingsMenu, (0,0,0), 4)
c = Circle("circle", (330,300), settingsMenu, (80,80,80),4, 8)
r.align_to_center()
c.align_to_center()

slider = Group("Slider", (0,0), settingsMenu, (r,l,c))


def slider_pressed(self, *args, **kwargs):
    mousePos = args[0]
    element = self._elements.get("circle", None)
    if element is not None:
        element.x = max(min(mousePos[0], self.x + self.width - element.Hitbox.w/2), self.x + element.Hitbox.w/2)
    
    for element in (element for element in settingsMenu._elements["allElements"] if element.Name == "sliderBox"):
        settingsMenu.removeElement(element)
        self.remove_element_by_name("sliderBox")
    self._elements["sliderBox"] = Rectangle("sliderBox", (self.x, self.y),( self.width, self.height), settingsMenu, (255,0,0), 4)
    

    
slider.pressed = slider_pressed
slider.held_down = slider_pressed
slider.Interactive = True

def Slider(
    ):
        newSlider = slider.copy()
        for name in newSlider._elements:
            newSlider._elements[name] = newSlider._elements[name].copy()
        return newSlider
    