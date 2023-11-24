from ..InteractiveOverlays import (Element, 
                                   ElementDict, 
                                   ElementList, 
                                   StillImage,
                                   Text,
                                   Rectangle,
                                   Circle,
                                   Line,
                                   Group,
                                   Overlay,
                                   OverlayManager)
import pygame

images = {}

def init(imageObjects = {}):

    global images
    images = imageObjects
    

def option_pressed(self, optionElements):
    
    currentText = self.currentOptionText.text
    self.value = optionElements[1].text
    self.currentOptionText.text = optionElements[1].text
    optionElements[1].text = currentText
    
    self.currentOptionText.update_text()
    optionElements[1].update_text()
    
    




def set_open(self, value):
    if self.open != value:
        arrow = self._elements.get(self.name + "-dropdownArrow", None)
        if arrow:
            arrow.baseImage = pygame.transform.rotate(arrow.baseImage, 180) if arrow.baseImage else None
            arrow.image = arrow.baseImage
        self.open = value
    
    for optionName in self.options:
        optionElements = self.options[optionName]
        optionElements.sort(key = lambda element: type(element) == Text)
        
        for optionElement in optionElements:
            optionElement.visible = value
            optionElement.interactive = value
            optionElement.bring_to_front()
                    



def DropdownList(name, pos, parent, options, textFont, textSize, textColor, allowNothing, borderColor, backgroundColor, padding, borderSize):
    x,y = pos
    options = list(options)
        
    currentOption = max(options, key=lambda string: len(string)) if len(options) > 0 else ""
    currentOptionText = Text(currentOption, textFont, textSize, textColor, (x,y),name+"-dropdownCurrentOptionText", parent)
    
    currentOptionText.set_bold(True)
    
    arrowImage = images.get("dropdownarrow",None)
    
    if arrowImage:
    
        arrowImage = pygame.transform.scale(arrowImage, (
            arrowImage.get_width() * (currentOptionText.hitbox.h/arrowImage.get_height()), 
            currentOptionText.hitbox.h
        ))
    
    dropdownArrow = StillImage(name+"-dropdownArrow", arrowImage, (x,y), parent, "dropdownarrow")
    
    width = currentOptionText.hitbox.width + dropdownArrow.hitbox.width
    height = max(currentOptionText.hitbox.height, dropdownArrow.hitbox.height)
    

    border = Rectangle(name + "-border", (x,y), (width + borderSize * 2+padding*2,height + borderSize*2 + padding*2), parent, borderColor, borderSize)
    backgroundDropdown = Rectangle(name+"-background", (x+borderSize,y+borderSize), (width + padding*2,height + padding*2), parent, backgroundColor)
    
    currentOptionText.move_forwards(3) 
    dropdownArrow.move_forwards(2)
    currentOptionText._x = x+borderSize+padding
    currentOptionText._y = y+borderSize+padding
    
    
    dropdownArrow.x = x+borderSize+padding+currentOptionText.hitbox.width
    dropdownArrow.y = y+borderSize+padding
    
    self = Group(name, pos, parent, (border,backgroundDropdown, dropdownArrow, currentOptionText))
    self.interactive = True
    self.currentOptionText = currentOptionText
    self.value = currentOptionText.text
    self.open = False
    self.options = {}
    textOY = y + border.hitbox.h + padding
    backgroundOY = y + border.hitbox.h
    i = 0
    for option in options:
        text = option
        if currentOption == option:
            if allowNothing:
                text = "     "
            else:
                continue
        
        
        optionBackground = Rectangle(name+"-optionBackground{}".format(option), (x, backgroundOY), (width + padding*2+borderSize*2 , height+padding*2), parent, backgroundColor)
        optionText = Text(text, textFont, textSize, textColor, (x+padding+borderSize, textOY), name+"-option{}".format(option), parent)
        self.options["option"+str(i)] = [optionBackground, optionText]
        
        pressedMaker = lambda index: (lambda self, *args, **kwargs: option_pressed(self, self.options["option"+str(index)]))
        released = lambda self, *args, **kwargs: set_open(self, False)
        optionText.pressed =  pressedMaker(i)
        optionBackground.pressed = pressedMaker(i)
        
        optionText.released = released
        optionBackground.released = released
        
        optionBackground.visible = False
        optionBackground.interactive = False
        optionText.visible = False
        optionText.interactive = False
        
        
        
        
        textOY+=height+padding*2
        backgroundOY+=height+padding*2
        i+=1
        
    
    #Resize box to fit all elements - width
    largestTextBox = currentOptionText
    for option in self.options:
        textBox = self.options[option][1]

        if textBox.hitbox.w > largestTextBox.hitbox.w:
            largestTextBox = textBox
    
    newWidth = largestTextBox.hitbox.w
    
    if newWidth > currentOptionText.hitbox.w:
        for option in self.options:
            bg, txt = self.options[option]
            bg.hitbox.w = newWidth + dropdownArrow.hitbox.w+ padding*2 + borderSize*2 
            
        backgroundDropdown.hitbox.w = newWidth + padding*2 + dropdownArrow.hitbox.w
        border.hitbox.w = newWidth + borderSize*2 + padding*2 + dropdownArrow.hitbox.w
        dropdownArrow.x = x+borderSize+padding*2+newWidth

    
    
    
    
    
    self.get_open = lambda self : self.open
    
            
    
    
    self.set_open = set_open
    self.other_element_pressed = lambda self, *args, **kwargs: set_open(self, False)
    
    self.pressed = lambda self, *args, **kwargs: set_open(self, not self.open)
    
    self.value = currentOptionText.text
    
    return self