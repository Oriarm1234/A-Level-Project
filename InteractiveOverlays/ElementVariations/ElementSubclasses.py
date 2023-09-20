import pygame
from .ElementBaseClass import Element

pygame.init()

class Text(Element):

    def __init__(self, text="", font="", size=8, color=(0,0,0), pos=(1,1), name="TextBox", parent=None):
        
        self._text=text
        self._font = font
        self.FontObject = pygame.font.SysFont(font, size)
        self.RenderedText = self.FontObject.render(text, True, color)
        self._color = color
        self._size = size
        self.get_bold = self.FontObject.get_bold
        self.set_bold = self._update_wrapper(self.FontObject.set_bold)
        self.get_italic = self.FontObject.get_italic
        self.set_italic = self._update_wrapper(self.FontObject.set_italic)
        self.get_underline = self.FontObject.get_underline
        self.set_underline = self._update_wrapper(self.FontObject.set_underline)
        self.get_strikethrough = self.FontObject.get_strikethrough
        self.set_strikethrough = self._update_wrapper(self.FontObject.set_strikethrough)

        super().__init__(name, self.RenderedText, pos, parent=parent)
        
    def _update_wrapper(self, function):
        def new_function(*args):
            function(*args)
            self.update_text()
        return new_function


    @property
    def Color(self):
        return self._color
    
    @Color.setter
    def Color(self, color):
        if color != self.Color:
            self._color = color
            self.update_text()

    @property
    def Text(self):
        return self._text
    
    @Text.setter
    def Text(self, value):
        if value != self._text:
            self._text = value
            self.update_text()
    
    @property
    def Font(self):
        return self._font
    
    @Font.setter
    def Font(self, value):
        if value != self._font:
            self._font = value
            self.FontObject = pygame.font.SysFont(self._font, self._size)
            self.update_text()
    
    
    @property
    def Size(self):
        return self._size
    
    @Size.setter
    def Size(self, value):
        if value != self._size:
            self._size = value
            self.FontObject = pygame.font.SysFont(self._font, int(self._size))
            self.update_text()

    def update_text(self):
        
        self.RenderedText = self.FontObject.render(self._text, True, self._color)
        self.Hitbox = self.RenderedText.get_rect()
        self.Hitbox.x, self.Hitbox.y = self.x + self.get_offset_x(), self.y + self.get_offset_y()
    

    def draw(self, screen=None, *args, **kwargs):
        if screen != None:

            screen.blit(self.RenderedText, (self.x + self.get_offset_x(), self.y + self.get_offset_y()))


class StillImage(Element):

    def __init__(self, name, image, pos, parent=None, image_name=""):
        super().__init__(name, image, pos, parent, image_name=image_name)
    
    def draw(self, screen=None, *args, **kwargs):
        if screen != None:
            screen.blit(self.Image, (self.x + self.get_offset_x(), self.y + self.get_offset_y()))







class Group(Element):
    def __init__(self, name, pos, parent=None):
        super().__init__(name, None, pos, parent)

        self._elements = {}

    @property
    def Elements(self):
        return list(self._elements.values())

    def append_element(self, element):
        if element not in [None, *self._elements]:
            self._elements[element.Name] = element
        
    def remove_element(self, element):
        if element in self._elements:
            del self._elements[element.Name]

    def IsElementAtPos(self, x, y, onlyInteractive=False):

        SortedElements = sorted(self._elements[["allElements", "interactive"][onlyInteractive]], key=lambda Element:Element.Hitbox.collidepoint(x,y))

        if SortedElements != [] and SortedElements[0].Hitbox.collidepoint(x,y):
            return True
        return False
    
    def GetElementAtPos(self, x, y, onlyInteractive=False):
        SortedElements = sorted(self._elements[["allElements", "interactive"][onlyInteractive]], key=lambda Element:Element.Hitbox.collidepoint(x,y))

        if SortedElements != [] and SortedElements[0].Hitbox.collidepoint(x,y):
            return SortedElements[0]
        return None
    
    def GetElementsAtPos(self, x, y, onlyInteractive=False):

        return list(filter(lambda Element: Element.Hitbox.collidepoint(x,y), self._elements[["allElements", "interactive"][onlyInteractive]]))

            
    def intereacted_at_pos(self, pos):
        pass

    def draw(self):
        pass

    def update(self):
        pass
