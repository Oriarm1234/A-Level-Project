from InteractiveOverlays import *
import pygame



def OptionPressed(self, optionElements):
    
    currentText = self.CurrentOptionText.Text
    self.CurrentOptionText.Text = optionElements[1].Text
    optionElements[1].Text = currentText
    
    self.CurrentOptionText.update_text()
    optionElements[1].update_text()






def SetOpen(self, value):
        if self._open != value:
            arrow = self._elements.get(self.Name + "-DropdownArrow", None)
            if arrow:
                arrow.BaseImage = pygame.transform.rotate(arrow.BaseImage, 180) if arrow.BaseImage else None
                arrow.Image = arrow.BaseImage
            self._open = value
        
        for optionName in self.Options:
            optionElements = self.Options[optionName]
            for optionElement in optionElements:
                optionElement.Visible = value
                optionElement.Interactive = value



def DropdownList(name, ArrowImage:pygame.Surface, pos, Parent, ArrowImageName, options, textFont, textSize, TextColor, allowNothing, borderColor, backgroundColor, padding, borderSize):
    x,y = pos
    options = list(options)
        
    currentOption = max(options) if len(options) > 0 else ""
    currentOptionText = Text(currentOption, textFont, textSize, TextColor, (x,y),name+"-DropdownCurrentOptionText", Parent)
    currentOptionText.set_bold(True)
    ArrowImage = pygame.transform.scale(ArrowImage, (
        ArrowImage.get_width() * (currentOptionText.Hitbox.h/ArrowImage.get_height()), 
        currentOptionText.Hitbox.h
    ))
    
    DropdownArrow = StillImage(name+"-DropdownArrow", ArrowImage, (x,y), Parent, ArrowImageName)
    
    width = currentOptionText.Hitbox.width + DropdownArrow.Hitbox.width
    height = max(currentOptionText.Hitbox.height, DropdownArrow.Hitbox.height)
    

    border = Rectangle(name + "-Border", (x,y), (width + borderSize * 2+padding*2,height + borderSize*2 + padding*2), Parent, borderColor, borderSize)
    BackgroundDropdown = Rectangle(name+"-Background", (x+borderSize,y+borderSize), (width + padding*2,height + padding*2), Parent, backgroundColor)
    
    currentOptionText.move_forwards(3) 
    DropdownArrow.move_forwards(2)
    currentOptionText._x = x+borderSize+padding
    currentOptionText._y = y+borderSize+padding
    
    
    DropdownArrow.x = x+borderSize+padding+currentOptionText.Hitbox.width
    DropdownArrow.y = y+borderSize+padding
    
    Dropdown = Group(name, pos, Parent, (border,BackgroundDropdown, DropdownArrow, currentOptionText))
    Dropdown.Interactive = True
    Dropdown.CurrentOptionText = currentOptionText
    Dropdown._open = False
    Dropdown.Options = {}
    textOY = y + border.Hitbox.h + padding
    backgroundOY = y + border.Hitbox.h
    
    for option in options:
        text = option
        if currentOption == option:
            if allowNothing:
                text = "     "
            else:
                continue
        
        print(backgroundOY, height)
        
        optionBackground = Rectangle(name+"-optionBackground{}".format(option), (x+borderSize, backgroundOY), (width + padding*2, height+padding*2), Parent, backgroundColor)
        optionText = Text(text, textFont, textSize, TextColor, (x+padding+borderSize, textOY), name+"-option{}".format(option), Parent)
        Dropdown.Options[option] = [optionBackground, optionText]
        
        pressed = lambda self, *args, **kwargs: OptionPressed(Dropdown, Dropdown.Options[option])
        released = lambda self, *args, **kwargs: SetOpen(Dropdown, False)
        optionText.pressed = pressed
        optionBackground.pressed = pressed
        
        optionText.released = released
        optionBackground.released = released
        
        optionBackground.Visible = False
        optionBackground.Interactive = False
        optionText.Visible = False
        optionText.Interactive = False
        
        
        
        
        textOY+=height+padding*2
        backgroundOY+=height+padding*2
        
    
    Dropdown.GetOpen = lambda self : self._open
    
            
    
    
    Dropdown.SetOpen = SetOpen
    
    Dropdown.pressed = lambda self, *args, **kwargs: SetOpen(self, not self._open)
    
    return Dropdown