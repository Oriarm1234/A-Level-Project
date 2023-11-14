from InteractiveOverlays import *
import pygame



def OptionPressed(self, optionElements):
    
    currentText = self.CurrentOptionText.Text
    self.Value = optionElements[1].Text
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
            optionElements.sort(key = lambda element: type(element) == Text)
            
            for optionElement in optionElements:
                optionElement.Visible = value
                optionElement.Interactive = value
                optionElement.bring_to_front()
                



def DropdownList(name, ArrowImage:pygame.Surface, pos, Parent, ArrowImageName, options, textFont, textSize, TextColor, allowNothing, borderColor, backgroundColor, padding, borderSize):
    x,y = pos
    options = list(options)
        
    currentOption = max(options, key=lambda string: len(string)) if len(options) > 0 else ""
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
    Dropdown.Value = currentOptionText.Text
    Dropdown._open = False
    Dropdown.Options = {}
    textOY = y + border.Hitbox.h + padding
    backgroundOY = y + border.Hitbox.h
    i = 0
    for option in options:
        text = option
        if currentOption == option:
            if allowNothing:
                text = "     "
            else:
                continue
        
        
        optionBackground = Rectangle(name+"-optionBackground{}".format(option), (x, backgroundOY), (width + padding*2+borderSize*2 , height+padding*2), Parent, backgroundColor)
        optionText = Text(text, textFont, textSize, TextColor, (x+padding+borderSize, textOY), name+"-option{}".format(option), Parent)
        Dropdown.Options["option"+str(i)] = [optionBackground, optionText]
         
        pressedMaker = lambda index: (lambda self, *args, **kwargs: OptionPressed(Dropdown, Dropdown.Options["option"+str(index)]))
        released = lambda self, *args, **kwargs: SetOpen(Dropdown, False)
        optionText.pressed =  pressedMaker(i)
        optionBackground.pressed = pressedMaker(i)
        
        optionText.released = released
        optionBackground.released = released
        
        optionBackground.Visible = False
        optionBackground.Interactive = False
        optionText.Visible = False
        optionText.Interactive = False
        
        
        
        
        textOY+=height+padding*2
        backgroundOY+=height+padding*2
        i+=1
        
    
    #Resize box to fit all elements - width
    largestTextBox = currentOptionText
    for option in Dropdown.Options:
        TextBox = Dropdown.Options[option][1]

        if TextBox.Hitbox.w > largestTextBox.Hitbox.w:
            largestTextBox = TextBox
    
    newWidth = largestTextBox.Hitbox.w
    
    if newWidth > currentOptionText.Hitbox.w:
        for option in Dropdown.Options:
            bg, txt = Dropdown.Options[option]
            bg.Hitbox.w = newWidth + DropdownArrow.Hitbox.w+ padding*2 + borderSize*2 
            
        BackgroundDropdown.Hitbox.w = newWidth + padding*2 + DropdownArrow.Hitbox.w
        border.Hitbox.w = newWidth + borderSize*2 + padding*2 + DropdownArrow.Hitbox.w
        DropdownArrow.x = x+borderSize+padding*2+newWidth

    
    
    
    
    
    Dropdown.GetOpen = lambda self : self._open
    
            
    
    
    Dropdown.SetOpen = SetOpen
    Dropdown.other_element_pressed = lambda self, *args, **kwargs: SetOpen(self, False)
    
    Dropdown.pressed = lambda self, *args, **kwargs: SetOpen(self, not self._open)
    
    Dropdown.Value = currentOptionText.Text
    
    return Dropdown