import pygame
from .ElementBaseClass import Element

pygame.init()


class Text(Element):
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
    
    def copy(self,
            text=None,
            font=None,
            size=None,
            color=None,
            pos=None,
            name=None,
            parent=None):
        
        return Text(text or self._text,
                    font or self._font,
                    size or self._size,
                    color or self._color,
                    pos or (self._x, self._y),
                    name or self.Name,
                    parent or self._parent)

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
        if screen != None:
            screen.blit(self.RenderedText, (self.x, self.y))


class StillImage(Element):
    def __init__(self, name, image, pos, parent=None, image_name=""):
        super().__init__(name, image, pos, parent, image_name=image_name)

    def draw(self, screen=None, *args, **kwargs):
        if screen != None:
            screen.blit(self.Image, (self.x, self.y))
    
    def copy(self, 
             name = None, 
             image = None, 
             pos = None, 
             parent=None, 
             image_name=None):
        
        return StillImage(
            name or self.Name,
            image or self.BaseImage,
            pos or (self._x, self._y),
            parent or self._parent,
            image_name or self.image_name
        )


class Rectangle(Element):
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
        if screen is not None:
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
            
    def copy(
        self,
        name=None,
        pos=None,
        size=None,
        parent=None,
        colour=None,
        borderThickness=None,
        borderRadius=None,
        borderTopLeftRadius=None,
        borderTopRightRadius=None,
        borderBottomLeftRadius=None,
        borderBottomRightRadius=None,
    ):
        
        return Rectangle(
            name or self.Name,
            pos or (self._x, self._y),
            size or self.Hitbox[2:],
            parent or self._parent,
            colour or self.Colour,
            borderThickness or self.BorderThickness,
            borderRadius or self.BorderRadius,
            borderTopLeftRadius or self.BorderTopLeftRadius,
            borderTopRightRadius or self.BorderTopRightRadius,
            borderBottomLeftRadius or self.BorderBottomLeftRadius,
            borderBottomRightRadius or self.BorderBottomRightRadius
        )


class Circle(Element):
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
        if screen is not None:
            pygame.draw.circle(
                screen,
                self.Colour,
                (self.x + self.Radius, self.y + self.Radius),
                self.Radius,
                self.BorderThickness,
            )
    
    def copy(
        self,
        name: str,
        pos: tuple[int, int],
        parent=None,
        colour: tuple[int, int, int] = (0, 0, 0),
        borderThickness: int = 0,
        radius: int = 5,):
        
        return Circle(
            name or self.Name,
            pos or (self._x, self._y),
            parent or self._parent,
            colour or self.Colour,
            borderThickness or self.BorderThickness,
            radius or self.Radius
        )


# TODO: All these basic shapes should be implemented!


class Line(Element):
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
        super().__init__(name, None, pos, parent)

        self.Hitbox = pygame.Rect(*pos, end_pos[0] - pos[0], end_pos[1] - pos[1])
        self.Colour = colour

        self.Thickness = thickness
        self.Radius = radius
        self.end_pos = end_pos
        

    def draw(self, screen=None, *args, **kwargs):
        if screen is not None:
            pygame.draw.line(screen, self.Colour, (self._x, self._y), self.end_pos, self.Thickness)
    
    def copy(self,
        name,
        pos:tuple[int, int],
        end_pos:tuple[int, int],
        parent=None,
        colour=(0, 0, 0),
        thickness=1,
        radius=5,):
        
        return Line(
            name or self.Name,
            pos or (self._x, self._y),
            end_pos or self.end_pos,
            parent or self._parent,
            colour or self.Colour,
            thickness or self.Thickness,
            radius or self.Radius
        )


class Group(Element):
    def __init__(self, name, pos, parent=None):
        super().__init__(name, None, pos, parent)

        self._elements = {}

    @property
    def Elements(self):
        return list(self._elements.values())

    def append_element(self, element):
        if (
            element not in [None, *list(self._elements.values())]
            and element.Name not in self._elements
        ):
            self._elements[element.Name] = element

    def remove_element(self, element):
        if element.Name in self._elements:
            del self._elements[element.Name]
        elif element in list(self._elements.values()):
            index = list(self._elements.values()).index(element)
            name = list(self._elements.keys())[index]
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

    def intereacted_at_pos(self, pos):
        pass
    
