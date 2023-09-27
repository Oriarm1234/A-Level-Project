import pygame

from ..ElementVariations.ElementSubclasses import Text


class Overlay:
    __ClassName__ = "Overlay"
    def __init__(
        self,
        Name: str,
        Size: tuple[int, int],
        Pos: tuple[int, int],
        Parent,
        ScreenFlags: list[int] = [],
        Elements: list = [],
        Visible: bool = False,
        ScreenFill: tuple[int, int, int, int] = (0, 0, 0, 0),
    ):
        self._elements = {"allElements": Elements, "interactive": []}
        self._screen = pygame.Surface(Size, *ScreenFlags)
        self._screen.fill(ScreenFill)

        self._hitbox = self._screen.get_rect()
        self._name = Name
        self._screen_flags = ScreenFlags
        self._pos = Pos
        self._size = Size
        self._parent = Parent
        self._visible = Visible
        self.get_offset_x = lambda: 0
        self.get_offset_y = lambda: 0

        self.Highlighted = None

    @property
    def Size(self):
        return self._size

    @property
    def Visible(self):
        return self._visible

    @property
    def Pos(self):
        return self._pos[0] + self.get_offset_x(), self._pos[1] + self.get_offset_y()

    @property
    def Parent(self):
        return self._parent

    @property
    def ScreenFlags(self):
        return self._screen_flags

    @property
    def Name(self):
        return self._name

    @property
    def Elements(self):
        return self._elements["allElements"]

    @property
    def InteractiveElements(self):
        return self._elements["interactive"]

    @property
    def Screen(self):
        return self._screen

    def update_hitbox(self):
        self._hitbox.x = self._pos[0] + self.get_offset_x() # type: ignore
        self._hitbox.y = self._pos[1] + self.get_offset_y() # type: ignore

    @Size.setter
    def Size(self, value):
        old_size = self._size
        self._screen = pygame.Surface(value, *self._screen_flags)
        self._size = value
        self._hitbox = self._screen.get_rect()
        self.update_hitbox()

        for element in self._elements["allElements"]:
            x_percent = element.x / old_size[0]
            y_percent = element.y / old_size[1]
            element.x = x_percent * value[0]
            element.y = y_percent * value[1]

            width_percent = element.Hitbox.width / old_size[0]
            height_percent = element.Hitbox.height / old_size[1]

            if type(element) == Text:
                element.Size = element.Size / old_size[0] * value[0]

            element.resize_image(width_percent * value[0], height_percent * value[1])

        self.update()

    @Pos.setter
    def Pos(self, value):
        self._pos = value
        self.update_hitbox()

    def align_to_center(self):
        self.get_offset_x = lambda: -self._hitbox.w / 2
        self.get_offset_y = lambda: -self._hitbox.h / 2
        self.update_hitbox()

    def align_to_top_left(self):
        self.get_offset_x = lambda: -self._hitbox.w
        self.get_offset_y = lambda: -self._hitbox.h
        self.update_hitbox()

    def align_to_top_middle(self):
        self.get_offset_x = lambda: -self._hitbox.w / 2
        self.get_offset_y = lambda: -self._hitbox.h
        self.update_hitbox()

    def align_to_top_right(self):
        self.get_offset_x = lambda: 0
        self.get_offset_y = lambda: -self._hitbox.h
        self.update_hitbox()

    def align_to_middle_right(self):
        self.get_offset_x = lambda: 0
        self.get_offset_y = lambda: -self._hitbox.h / 2
        self.update_hitbox()

    def align_to_middle_left(self):
        self.get_offset_x = lambda: -self._hitbox.w
        self.get_offset_y = lambda: -self._hitbox.h / 2
        self.update_hitbox()

    def align_to_bottom_left(self):
        self.get_offset_x = lambda: -self._hitbox.w
        self.get_offset_y = lambda: 0
        self.update_hitbox()

    def align_to_bottom_middle(self):
        self.get_offset_x = lambda: -self._hitbox.w / 2
        self.get_offset_y = lambda: 0
        self.update_hitbox()

    def align_to_bottom_right(self):
        self.get_offset_x = lambda: 0
        self.get_offset_y = lambda: 0
        self.update_hitbox()

    def appendElement(self, element):
        if element._parent is not None:
            element._parent.removeElement(element)
        if element not in self._elements["allElements"]:
            self._elements["allElements"].append(element)
        element._parent = self

    def removeElement(self, element):
        if element in self._elements["allElements"]:
            self._elements["allElements"].remove(element)
        element._parent = None

    def insertElement(self, element, index):
        self.removeElement(element)
        self._elements["allElements"].insert(index, element)
        element._parent = self

    def setElementInteractive(self, element, isInteractive):
        if element is not None and element in self._elements["allElements"]:
            element._interactive = isInteractive
            if isInteractive:
                self._elements["interactive"].append(element)
            elif element in self._elements["interactive"]:
                self._elements["interactive"].remove(element)

    def moveElementForward(self, element, amount):
        if element in self._elements["allElements"]:
            index = self._elements["allElements"].index(element)

            self.insertElement(element, max(index + amount, 0))

    def moveElementBackward(self, element, amount):
        if element in self._elements["allElements"]:
            index = self._elements["allElements"].index(element)

            self.insertElement(element, max(index - amount, 0))
            
    def collidepoint(self, element, x, y):
        if element.Hitbox is not None:
            return element.Hitbox.collidepoint(x, y)
        
        elif element.__ClassName__ == "Group":
            return pygame.Rect(element.x, element.y, element.width, element.height).collidepoint(x, y)
        
        return False

    def IsElementAtPos(self, x, y, onlyInteractive=False):
        SortedElements = sorted(
            self._elements[["allElements", "interactive"][onlyInteractive]],
            key=lambda Element: self.collidepoints(Element, x, y),
        )

        if SortedElements != [] and SortedElements[0].Hitbox.collidepoint(x, y):
            return True
        return False
    
    

    def GetElementAtPos(self, x, y, onlyInteractive=False):
         
        SortedElements = sorted(
            self._elements[["allElements", "interactive"][onlyInteractive]],
            key=lambda Element: self.collidepoint(Element, x, y),
        )

        if SortedElements != [] and SortedElements[0].Hitbox.collidepoint(x, y):
            return SortedElements[0]
        return None

    def GetElementsAtPos(self, x, y, onlyInteractive=False):
        return list(
            filter(
                lambda Element: self.collidepoint(Element, x, y),
                self._elements[["allElements", "interactive"][onlyInteractive]],
            )
        )
        
    def copy(self, Name="", Size=None, Pos=None, Parent=None, ScreenFlags=None, Elements=None, Visible=None, ScreenFill=(0,0,0,0)):
        Copy = Overlay(
            self._name+"_copy" if Name == "" else Name, 
            self._size.copy() if Size == None else Size, 
            self._pos.copy() if Pos == None else Pos, 
            self._parent if Parent == None else Parent,
            self._screen_flags.copy() if ScreenFlags is None else ScreenFlags,
            self._elements.copy() if Elements is None else Elements,
            self._visible if Visible == None else Visible,
            ScreenFill)
        
        return Copy

    def preUpdate(self, *args, **kwargs):
        pass

    def postUpdate(self, *args, **kwargs):
        pass

    def elementPreUpdate(self, element, *args, **kwargs):
        pass

    def elementPostUpdate(self, element, *args, **kwargs):
        pass

    def update(self, *args, **kwargs):
        self.preUpdate(self, *args, **kwargs)
        for element in self._elements["allElements"]:
            self.elementPreUpdate(self, element, *args, **kwargs)
            element.update(screen=self._screen, *args, **kwargs)
            self.elementPostUpdate(self, element, *args, **kwargs)

        self.postUpdate(self, *args, **kwargs)

    def draw(self, screen=None):
        if screen != None:
            screen.blit(
                self._screen,
                (
                    self._pos[0] + self.get_offset_x(),
                    self._pos[1] + self.get_offset_y(),
                ),
            )
