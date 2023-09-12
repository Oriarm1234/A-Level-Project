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
    

    def draw(self, screen=None):
        if screen != None:

            screen.blit(self.RenderedText, (self.x + self.get_offset_x(), self.y + self.get_offset_y()))


class StillImage(Element):

    def __init__(self, name, image, pos, parent=None):
        super().__init__(name, image, pos, parent)
    
    def draw(self, screen=None):
        if screen != None:
            screen.blit(self.Image, (self.x + self.get_offset_x(), self.y + self.get_offset_y()))

class Animation(Element):

    def __init__(self, name, pos, parent=None):
        super().__init__(name, None, pos, parent)

        self.Images = []
        self.FPS = 0
        self.CurrentFrame = None
        self.CurrentFrameIndex = 0
        self.LastFrameChange = None
        self.paused = False

    def addImage(self, image:(pygame.Surface), index:(None|int)=None):
        """
        Add an image to the animation.

        if index is None, then the image will be added to the end of the animation.
        
        Else, the image will be inserted into the animation at the given index
        """

        if image is not pygame.Surface:
            raise ValueError("Image must be of type pygame.Surface")
        
        if index is not None and type(index) != int:
            raise ValueError("Index must be an integer value or of type None")


        if index is not None:
            self.Images.append(image)
        else:
            self.Images.insert(index, image)

    def removeImage(self, image:(None|pygame.Surface)=None, index:(None|int)=None):
        """
        Remove an image from the animation.
        
        If an image is not passed, but an index is provided, the image will be removed by deleting the index.
        If an index is not provided, then the image will be removed through the list.remove method.
        
        if neither are provided, nothing will be removed."""


        if image is None and type(index) == int:
            del self.Images[index]

        elif index is None and type(image) == pygame.Surface:
            self.Images.remove(image)
        
    
    def update(self, currentTime, screen=None):
        if len(self.Images) != 0:
            if currentTime - self.LastFrameChanged > 1/self.FPS:
                self.CurrentFrameIndex = (self.CurrentFrameIndex + 1) % len(self.Images)-1
            if not self.paused:
                self.CurrentFrame = self.Images[self.CurrentFrameIndex]

        self.draw(screen)
            

    def draw(self, screen=None):
        if screen != None and self.CurrentFrame != None:
            screen.blit(self.CurrentFrame, (self.x + self.get_offset_x(), self.y + self.get_offset_y()))