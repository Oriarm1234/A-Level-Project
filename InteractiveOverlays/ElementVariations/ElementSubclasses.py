import pygame
from .ElementBaseClass import *

pygame.init()


class Text(Element):
    __ClassName__ = "Text"
    def __init__(
        self,
        text="",
        font="",
        size=8,
        color=(0, 0, 0),
        pos=(1, 1),
        name="TextBox",
        parent=None,
    ):
        self._text = text
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
    
    def renderer(self, text):
        return self.FontObject.render(text, True, self._color)

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
        self.Hitbox.x, self.Hitbox.y = self.x, self.y

    def draw(self, screen=None, *args, **kwargs):
        if screen != None and self.Visible:
            screen.blit(self.RenderedText, (self.x, self.y))


class StillImage(Element):
    __ClassName__ = "StillImage"
    def __init__(self, name, image, pos, parent=None, image_name=""):
        super().__init__(name, image, pos, parent, image_name=image_name)

    def draw(self, screen=None, *args, **kwargs):
        if screen != None and self.Visible:
            screen.blit(self.Image, (self.x, self.y))


class Rectangle(Element):
    __ClassName__ = "Rectangle"
    def __init__(
        self,
        name,
        pos,
        size,
        parent=None,
        colour=(0, 0, 0),
        borderThickness=0,
        borderRadius=-1,
        borderTopLeftRadius=-1,
        borderTopRightRadius=-1,
        borderBottomLeftRadius=-1,
        borderBottomRightRadius=-1,
    ):
        Hitbox = pygame.Rect(*pos, *size)

        super().__init__(name, None, pos, parent, Hitbox=Hitbox)

        self.Colour = colour

        self.BorderThickness = borderThickness
        self.BorderRadius = borderRadius
        self.BorderTopLeftRadius = borderTopLeftRadius
        self.BorderTopRightRadius = borderTopRightRadius
        self.BorderBottomLeftRadius = borderBottomLeftRadius
        self.BorderBottomRightRadius = borderBottomRightRadius

    def draw(self, screen=None, *args, **kwargs):
        if screen is not None and self.Visible:
            pygame.draw.rect(
                screen,
                self.Colour,
                self.Hitbox,
                self.BorderThickness,
                self.BorderRadius,
                self.BorderTopLeftRadius,
                self.BorderTopRightRadius,
                self.BorderBottomLeftRadius,
                self.BorderBottomRightRadius,
            )


class Circle(Element):
    __ClassName__ = "Circle"
    def __init__(
        self,
        name: str,
        pos: tuple[int, int],
        parent=None,
        colour: tuple[int, int, int] = (0, 0, 0),
        borderThickness: int = 0,
        radius: int = 5,
    ):
        Hitbox = pygame.Rect(*pos, radius * 2, radius * 2)
        self.Radius = radius

        super().__init__(name, None, pos, parent, Hitbox=Hitbox)

        self.Colour = colour

        self.BorderThickness = borderThickness

    def update_hitbox(self):
        if self.Hitbox is not None:
            self.Hitbox.x = self.x
            self.Hitbox.y = self.y

    def draw(self, screen=None, *args, **kwargs):
        if screen is not None and self.Visible:
            pygame.draw.circle(
                screen,
                self.Colour,
                (self.x + self.Radius, self.y + self.Radius),
                self.Radius,
                self.BorderThickness,
            )


# TODO: All these basic shapes should be implemented!


class Line(Element):
    __ClassName__ = "Line"
    def __init__(
        self,
        name,
        pos:tuple[int, int],
        end_pos:tuple[int, int],
        parent=None,
        colour=(0, 0, 0),
        thickness=1,
        radius=5,
    ):
        self._endX, self._endY = (0,0)
        super().__init__(name, None, pos, parent)

        self.Hitbox = pygame.Rect(*pos, end_pos[0] - pos[0], end_pos[1] - pos[1])
        self.Colour = colour

        self.Thickness = thickness
        self.Radius = radius
        self._endX, self._endY = end_pos
        
        self.update_hitbox()
        
    def update_hitbox(self):
        self.Hitbox.x = self.x
        self.Hitbox.y = self.y
        self.Hitbox.w = self._endX - self._x
        self.Hitbox.h = self._endY - self._y
        
    @property
    def startX(self):
        return self._x

    @property
    def startY(self):
        return self._y 
        
    @property
    def endX(self):
        return self._endX
    
    @property
    def endY(self):
        return self._endY 
    
    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y 
    
    @startX.setter
    def startX(self, value):
        self._x = value
        if type(self.Hitbox) == pygame.Rect:
            self.update_hitbox()
        return value

    @startY.setter
    def startY(self, value):
        self._y = value
        if type(self.Hitbox) == pygame.Rect:
            self.update_hitbox()
        return value

    @x.setter
    def x(self, value):
        width = self._endX - self._x
        self._x = value
        self._endX = value + width
        if type(self.Hitbox) == pygame.Rect:
            self.update_hitbox()
        return value

    @y.setter
    def y(self, value):
        height = self._endY - self._y
        self._y = value
        self._endY = value + height
        if type(self.Hitbox) == pygame.Rect:
            self.update_hitbox()
        return value
    
    @endX.setter
    def endX(self, value):
        self._endX = value
        if type(self.Hitbox) == pygame.Rect:
            self.update_hitbox()
        return value
    
    @endY.setter
    def endY(self, value):
        self._endY = value
        if type(self.Hitbox) == pygame.Rect:
            self.update_hitbox()
        return value

    def draw(self, screen=None, *args, **kwargs):
        if screen is not None and self.Visible:
            pygame.draw.line(screen, self.Colour, (self._x, self._y), (self._endX, self._endY), self.Thickness)


class Group(Element):
    __ClassName__ = "Group"
    def __init__(self, name, pos, parent=None, elements=[], Visible=True):
        self._elements = elementDict()
        super().__init__(name, None, pos, parent)

        self._visible = Visible
        
        for element in elements:
            self.append_element(element)
            
    @property
    def Visible(self):
        return self._visible
    
    @Visible.setter
    def Visible(self, value):
        self._visible = value
        for element in self.Elements:
            element.Visible = value
        return value
    
    @property
    def Parent(self):
        return self._parent
    
    @Parent.setter
    def Parent(self, newParent):
        for element in [self, *self.Elements]:
            if element._parent is not None:
                element._parent.removeElement(element)
            if newParent is not None:
                newParent.appendElement(element)
            element._parent = newParent

    @property
    def Elements(self):
        return elementList(self._elements.values())

    def append_element(self, element):
        if (
            element not in [None, *list(self._elements.values())]
            and element.Name not in self._elements
        ):
            self._elements[element.Name] = element
            self._x = min(element._x, self._x)
            self._y = min(element._y, self._y)
        element._parent = self.Parent

    def remove_element(self, element):
        if element.Name in self._elements:
            del self._elements[element.Name]
        elif element in list(self._elements.values()):
            index = list(self._elements.values()).index(element)
            name = list(self._elements.keys())[index]
            del self._elements[name]
            
    def remove_element_by_name(self, name):
        if name in self._elements:
            del self._elements[name]
              

    def IsElementAtPos(self, x, y, onlyInteractive=False):
        SortedElements = sorted(
            filter(
                lambda Element: (not onlyInteractive) + Element._interactive,
                self.Elements,
            ),
            key=lambda Element: Element.Hitbox.collidepoint(x, y),
        )

        if SortedElements != [] and SortedElements[0].Hitbox.collidepoint(x, y):
            return True
        return False

    def GetElementAtPos(self, x, y, onlyInteractive=False):
        SortedElements = sorted(
            filter(
                lambda Element: (not onlyInteractive) + Element._interactive,
                self.Elements,
            ),
            key=lambda Element: Element.Hitbox.collidepoint(x, y),
        )

        if SortedElements != [] and SortedElements[0].Hitbox.collidepoint(x, y):
            return SortedElements[0]
        return None

    def GetElementsAtPos(self, x, y, onlyInteractive=False):
        return list(
            filter(
                lambda Element: Element.Hitbox.collidepoint(x, y),
                filter(
                    lambda Element: (not onlyInteractive) + Element._interactive,
                    self.Elements,
                ),
            )
        )

    
    @property
    def x(self):
        elements = self.Elements
        if elements != []:
            self._x = min(self.Elements, key = lambda element: element.x).x
            return self._x
        else:
            return None  
    
    @property
    def y(self):
        elements = self.Elements
        if elements != []:
            self._y= min(self.Elements, key = lambda element: element.y).y
            return self._y
        else:
            return None
    
    @x.setter
    def x(self, value):
        xPos = self.x
        if xPos is not None:
            xPos = int(xPos)
            for element in self.Elements:
                element.x = element._x - xPos + value
            
            self._x = value
        return value 
    
    @y.setter
    def y(self, value):
        yPos = self.y
        if yPos is not None:
            yPos = int(yPos)
            for element in self.Elements:
                element.y = element._y - yPos + value
            
            self._y = value
        return value 
    
    @property
    def width(self):
        elements = self.Elements
        xPos = self.x
        if elements != []:
            biggestRight=max(self.Elements, key = lambda element: element.x + element.Hitbox.w)
            return biggestRight.x + biggestRight.Hitbox.w - xPos
        else:
            return 0

    @property
    def height(self):
        elements = self.Elements
        yPos = self.y
        if elements != []:
            biggestDown = max(self.Elements, key = lambda element: element.y + element.Hitbox.h)
            return biggestDown.y + biggestDown.Hitbox.h - yPos
        else:
            return 0
