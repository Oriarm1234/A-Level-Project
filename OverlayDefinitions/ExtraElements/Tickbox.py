from InteractiveOverlays import *

def pressed(self, *args, **kwargs):
    self.tick.Visible = not self.tick.Visible
    self.Value = self.tick.Visible

def Tickbox(Pos, Size, Name, CircleRadius, Parent, BorderSize, BorderColour, BGColour, CircleColour, CircleBorderSize, tickImage, default):
    bg = Rectangle(Name+"-background#Tickbox", Pos, Size, Parent, BGColour)
    border = Rectangle(Name+"-border#Tickbox", Pos, Size, Parent, BorderColour, BorderSize)
    circle = Circle(Name+"-circle#Tickbox", (Pos[0]+Size[0]/2, Pos[1]+Size[1]/2), Parent, CircleColour, CircleBorderSize, CircleRadius)
    circle.align_to_center()
    tick = StillImage(Name+"-tickImage#Tickbox", tickImage, (Pos[0]+Size[0]/2, Pos[1]+Size[1]/2), Parent)
    tick.align_to_center()
    
    tick.Visible = default
    
    NewTickbox = Group(Name, Pos, Parent, (bg,border,circle,tick))
    NewTickbox.Value = default
    NewTickbox.tick = tick
    NewTickbox.pressed = pressed
    NewTickbox.Interactive = True
    return NewTickbox
    