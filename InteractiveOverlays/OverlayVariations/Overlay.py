import pygame
from .OverlayManager import OverlayManager
from ..ElementVariations.ElementBaseClass import Element
from ..ElementVariations.ElementSubclasses import *
class Overlay:

    def __init__(self, 
                 Name:str, 
                 Size:list[int], 
                 Pos:list[int], 
                 Parent:OverlayManager,
                 ScreenFlags:list[int] = [],
                 Elements:list[Element] = []):
        
        self._elements = Elements
        self._screen = pygame.Surface(Size, *ScreenFlags)
        self._screen.fill((0,0,0,0))

        self._hitbox = self._screen.get_rect()
        self._name = Name
        self._screen_flags = ScreenFlags
        self._pos = Pos
        self._size = Size
        self._parent = Parent

    @property
    def Size(self): return self._size

    @property
    def Pos(self): return self._pos

    @property
    def Parent(self): return self._parent

    @property
    def ScreenFlags(self): return self._screen_flags

    @property
    def Name(self): return self._name

    @property
    def Elements(self): return self._elements

    @property
    def Screen(self): return self._screen

    @Size.setter
    def Size(self, value): 
        old_size = self._size
        self._screen = pygame.Surface(value, *self._screen_flags)
        self._size = value

        for element in self._elements:
            x_percent = element.x / old_size[0]
            y_percent = element.y / old_size[1]
            element.x = x_percent * value[0]
            element.y = y_percent * value[1]
            

            width_percent = element.Hitbox.width / old_size[0]
            height_percent = element.Hitbox.height / old_size[1]

            if type(element) == Text:
                element.Size = element.Size / old_size[0] * value[0]

            element.resize_image(width_percent * value[0],
                                 height_percent * value[1])
        
        self.update()
    
    @Pos.setter
    def Pos(self, value):
        self._hitbox.x = value[0]
        self._hitbox.y = value[1]
        self._pos = value


    




    def appendElement(self, element):
        if element not in self._elements:
            self._elements.append(element)

    def removeElement(self, element):
        if element in self._elements:
            self._elements.remove(element)

    def insertElement(self, element, index):
        self.removeElement(element)
        self._elements.insert(index, element)

    def moveElementForward(self, element, amount):
        if element in self._elements:
            index = self._elements.index(element)

            self.insertElement(element, max(index+amount, 0))

    def moveElementBackward(self, element, amount):
        if element in self._elements:
            index = self._elements.index(element)
            
            self.insertElement(element, max(index-amount, 0))
        
    def IsElementAtPos(self, x, y):

        SortedElements = sorted(self._elements, key=lambda Element:Element.Hitbox.collidepoint(x,y))

        if SortedElements != [] and SortedElements[0].Hitbox.collidepoint(x,y):
            return True
        return False
    
    def GetElementAtPos(self, x, y):
        SortedElements = sorted(self._elements, key=lambda Element:Element.Hitbox.collidepoint(x,y))

        if SortedElements != [] and SortedElements[0].Hitbox.collidepoint(x,y):
            return SortedElements[0]
        return None
    
    def GetElementsAtPos(self, x, y):

        return list(filter(lambda Element: Element.Hitbox.collidepoint(x,y), self._elements))
    
    def update(self):
        self._screen.fill((0,0,0,0))
        for element in self._elements:
            element.update(screen = self._screen)
        