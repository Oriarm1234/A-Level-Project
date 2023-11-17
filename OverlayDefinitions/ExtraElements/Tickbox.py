from InteractiveOverlays import *

def pressed(self, *args, **kwargs):
    self.tick.visible = not self.tick.visible
    self.value = self.tick.visible

def Tickbox(pos, size, name, circleRadius, parent, borderSize, borderColour, bgColour, circleColour, circleBorderSize, tickImage, default):
    bg = Rectangle(name+"-tickbox-background", pos, size, parent, bgColour)
    border = Rectangle(name+"-tickbox-border", pos, size, parent, borderColour, borderSize)
    circle = Circle(name+"-tickbox-circle", (pos[0]+size[0]/2, pos[1]+size[1]/2), parent, circleColour, circleBorderSize, circleRadius)
    circle.align_to_center()
    tick = StillImage(name+"-tickbox-tickImage", tickImage, (pos[0]+size[0]/2, pos[1]+size[1]/2), parent)
    tick.align_to_center()
    
    tick.visible = default
    
    newTickbox = Group(name, pos, parent, (bg,border,circle,tick))
    newTickbox.value = default
    newTickbox.tick = tick
    newTickbox.pressed = pressed
    newTickbox.interactive = True
    return newTickbox
    