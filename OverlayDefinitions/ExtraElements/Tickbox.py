from InteractiveOverlays import *

def pressed(self, *args, **kwargs):
    self.tick.visible = not self.tick.visible
    self.value = self.tick.visible

def Tickbox(Pos, Size, name, CircleRadius, parent, BorderSize, BorderColour, BGColour, CircleColour, CircleBorderSize, tickImage, default):
    bg = Rectangle(name+"-background#Tickbox", Pos, Size, parent, BGColour)
    border = Rectangle(name+"-border#Tickbox", Pos, Size, parent, BorderColour, BorderSize)
    circle = Circle(name+"-circle#Tickbox", (Pos[0]+Size[0]/2, Pos[1]+Size[1]/2), parent, CircleColour, CircleBorderSize, CircleRadius)
    circle.align_to_center()
    tick = StillImage(name+"-tickImage#Tickbox", tickImage, (Pos[0]+Size[0]/2, Pos[1]+Size[1]/2), parent)
    tick.align_to_center()
    
    tick.visible = default
    
    NewTickbox = Group(name, Pos, parent, (bg,border,circle,tick))
    NewTickbox.value = default
    NewTickbox.tick = tick
    NewTickbox.pressed = pressed
    NewTickbox.interactive = True
    return NewTickbox
    