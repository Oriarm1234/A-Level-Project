import pygame
from .ElementBaseClass import (Element, ElementDict, ElementList)

pygame.init()


class Text(Element):
    __ClassName__ = "Text"
    def __init__(
        self,
        text="",
        font="",
        size=8,
        colour=(0, 0, 0),
        pos=(1, 1),
        name="TextBox",
        parent=None,
    ):
        self._text = text
        self._font = font
        self.fontObject = pygame.font.SysFont(font, size)
        self.renderedText = self.fontObject.render(text, True, colour)
        self._color = colour
        self._size = size
        self.get_bold = self.fontObject.get_bold
        self.set_bold = self._update_wrapper(self.fontObject.set_bold)
        self.get_italic = self.fontObject.get_italic
        self.set_italic = self._update_wrapper(self.fontObject.set_italic)
        self.get_underline = self.fontObject.get_underline
        self.set_underline = self._update_wrapper(self.fontObject.set_underline)
        self.get_strikethrough = self.fontObject.get_strikethrough
        self.set_strikethrough = self._update_wrapper(self.fontObject.set_strikethrough)

        super().__init__(name, self.renderedText, pos, parent=parent)

    def _update_wrapper(self, function):
        def new_function(*args):
            function(*args)
            self.update_text()

        return new_function
    
    def renderer(self, text):
        return self.fontObject.render(text, True, self._color)

    @property
    def colour(self):
        return self._color

    @colour.setter
    def colour(self, colour):
        if colour != self.colour:
            self._color = colour
            self.update_text()

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if value != self._text:
            self._text = value
            self.update_text()

    @property
    def font(self):
        return self._font

    @font.setter
    def font(self, value):
        if value != self._font:
            self._font = value
            self.fontObject = pygame.font.SysFont(self._font, self._size)
            self.update_text()

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        if value != self._size:
            self._size = value
            self.fontObject = pygame.font.SysFont(self._font, int(self._size))
            self.update_text()

    def update_text(self):
        self.renderedText = self.fontObject.render(self._text, True, self._color)
        self.hitbox = self.renderedText.get_rect()
        self.hitbox.x, self.hitbox.y = self.x, self.y

    def draw(self, screen=None, *args, **kwargs):
        if screen != None and self.visible:
            screen.blit(self.renderedText, (self.x, self.y))


class StillImage(Element):
    __ClassName__ = "StillImage"
    def __init__(self, name, image, pos, parent=None, imageName=""):
        super().__init__(name, image, pos, parent, imageName=imageName)

    def draw(self, screen=None, *args, **kwargs):
        if screen != None and self.visible:
            screen.blit(self.image, (self.x, self.y))


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
        hitbox = pygame.Rect(*pos, *size)

        super().__init__(name, None, pos, parent, hitbox=hitbox)

        self.colour = colour

        self.borderThickness = borderThickness
        self.borderRadius = borderRadius
        self.borderTopLeftRadius = borderTopLeftRadius
        self.borderTopRightRadius = borderTopRightRadius
        self.borderBottomLeftRadius = borderBottomLeftRadius
        self.borderBottomRightRadius = borderBottomRightRadius

    def draw(self, screen=None, *args, **kwargs):
        if screen is not None and self.visible:
            pygame.draw.rect(
                screen,
                self.colour,
                self.hitbox,
                self.borderThickness,
                self.borderRadius,
                self.borderTopLeftRadius,
                self.borderTopRightRadius,
                self.borderBottomLeftRadius,
                self.borderBottomRightRadius,
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
        hitbox = pygame.Rect(*pos, radius * 2, radius * 2)
        self.radius = radius

        super().__init__(name, None, pos, parent, hitbox=hitbox)

        self.colour = colour

        self.borderThickness = borderThickness

    def update_hitbox(self):
        if self.hitbox is not None:
            self.hitbox.x = self.x
            self.hitbox.y = self.y

    def draw(self, screen=None, *args, **kwargs):
        if screen is not None and self.visible:
            pygame.draw.circle(
                screen,
                self.colour,
                (self.x + self.radius, self.y + self.radius),
                self.radius,
                self.borderThickness,
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

        self.hitbox = pygame.Rect(*pos, end_pos[0] - pos[0], end_pos[1] - pos[1])
        self.colour = colour

        self.thickness = thickness
        self.radius = radius
        self._endX, self._endY = end_pos
        
        self.update_hitbox()
        
    def update_hitbox(self):
        self.hitbox.x = self.x
        self.hitbox.y = self.y
        self.hitbox.w = self._endX - self._x
        self.hitbox.h = self._endY - self._y
        
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
        if type(self.hitbox) == pygame.Rect:
            self.update_hitbox()
        return value

    @startY.setter
    def startY(self, value):
        self._y = value
        if type(self.hitbox) == pygame.Rect:
            self.update_hitbox()
        return value

    @x.setter
    def x(self, value):
        width = self._endX - self._x
        self._x = value
        self._endX = value + width
        if type(self.hitbox) == pygame.Rect:
            self.update_hitbox()
        return value

    @y.setter
    def y(self, value):
        height = self._endY - self._y
        self._y = value
        self._endY = value + height
        if type(self.hitbox) == pygame.Rect:
            self.update_hitbox()
        return value
    
    @endX.setter
    def endX(self, value):
        self._endX = value
        if type(self.hitbox) == pygame.Rect:
            self.update_hitbox()
        return value
    
    @endY.setter
    def endY(self, value):
        self._endY = value
        if type(self.hitbox) == pygame.Rect:
            self.update_hitbox()
        return value

    def draw(self, screen=None, *args, **kwargs):
        if screen is not None and self.visible:
            pygame.draw.line(screen, self.colour, (self._x, self._y), (self._endX, self._endY), self.thickness)


class Group(Element):
    __ClassName__ = "Group"
    def __init__(self, name, pos, parent=None, elements=[], visible=True):
        self._elements = ElementDict()
        super().__init__(name, None, pos, parent)

        self._visible = visible
        
        for element in elements:
            self.append_element(element)
            
    @property
    def visible(self):
        return self._visible
    
    @visible.setter
    def visible(self, value):
        self._visible = value
        for element in self.elements:
            element.visible = value
            self.parent.set_element_interactive(element, value)
        return value
    
    @property
    def parent(self):
        return self._parent
    
    @parent.setter
    def parent(self, newParent):
        for element in [self, *self.elements]:
            if element._parent is not None:
                element._parent.remove_element(element)
            if newParent is not None:
                newParent.append_element(element)
            element._parent = newParent

    @property
    def elements(self):
        return ElementList(self._elements.values())

    def append_element(self, element):
        if (
            element not in [None, *list(self._elements.values())]
            and element.name not in self._elements
        ):
            self._elements[element.name] = element
            self._x = min(element._x, self._x)
            self._y = min(element._y, self._y)
        element._parent = self.parent
        element.visible = self.visible
        element.interactive = self.visible

    def remove_element(self, element):
        if element.name in self._elements:
            del self._elements[element.name]
        elif element in list(self._elements.values()):
            index = list(self._elements.values()).index(element)
            name = list(self._elements.keys())[index]
            del self._elements[name]
            
    def remove_element_by_name(self, name):
        if name in self._elements:
            del self._elements[name]
              

    def is_element_at_pos(self, x, y, onlyInteractive=False):
        sortedElements = sorted(
            filter(
                lambda element: (not onlyInteractive) + element._interactive,
                self.elements,
            ),
            key=lambda element: element.hitbox.collidepoint(x, y),
        )

        if sortedElements != [] and sortedElements[0].hitbox.collidepoint(x, y):
            return True
        return False

    def get_element_at_pos(self, x, y, onlyInteractive=False):
        sortedElements = sorted(
            filter(
                lambda element: (not onlyInteractive) + element._interactive,
                self.elements,
            ),
            key=lambda element: element.hitbox.collidepoint(x, y),
        )

        if sortedElements != [] and sortedElements[0].hitbox.collidepoint(x, y):
            return sortedElements[0]
        return None

    def get_elements_at_pos(self, x, y, onlyInteractive=False):
        return list(
            filter(
                lambda element: element.hitbox.collidepoint(x, y),
                filter(
                    lambda element: (not onlyInteractive) + element._interactive,
                    self.elements,
                ),
            )
        )

    
    @property
    def x(self):
        elements = self.elements
        if elements != []:
            self._x = min(self.elements, key = lambda element: element.x).x
            return self._x
        else:
            return None  
    
    @property
    def y(self):
        elements = self.elements
        if elements != []:
            self._y= min(self.elements, key = lambda element: element.y).y
            return self._y
        else:
            return None
    
    @x.setter
    def x(self, value):
        xPos = self.x
        if xPos is not None:
            xPos = int(xPos)
            for element in self.elements:
                element.x = element._x - xPos + value
            
            self._x = value
        return value 
    
    @y.setter
    def y(self, value):
        yPos = self.y
        if yPos is not None:
            yPos = int(yPos)
            for element in self.elements:
                element.y = element._y - yPos + value
            
            self._y = value
        return value 
    
    @property
    def width(self):
        elements = self.elements
        xPos = self.x
        if elements != []:
            biggestRight=max(self.elements, key = lambda element: element.x + element.hitbox.w)
            return biggestRight.x + biggestRight.hitbox.w - xPos
        else:
            return 0

    @property
    def height(self):
        elements = self.elements
        yPos = self.y
        if elements != []:
            biggestDown = max(self.elements, key = lambda element: element.y + element.hitbox.h)
            return biggestDown.y + biggestDown.hitbox.h - yPos
        else:
            return 0
