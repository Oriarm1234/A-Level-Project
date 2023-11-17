import pygame
from ..ElementVariations.ElementSubclasses import Text
from ..ElementVariations.ElementBaseClass import ElementDict, ElementList

class Overlay:
    __ClassName__ = "Overlay"
    def __init__(
        self,
        name: str,
        size: tuple[int, int],
        pos: tuple[int, int],
        parent,
        screenFlags: list[int] = [],
        elements: list = ElementList(),
        visible: bool = False,
        screenFill: tuple[int, int, int, int] = (0, 0, 0, 0),
    ):
        self._elements = {"allElements": elements, "interactive": ElementList()}
        self._screen = pygame.Surface(size, *screenFlags)
        self._screen.fill(screenFill)

        self._hitbox = self._screen.get_rect()
        self._name = name
        self._screenFlags = screenFlags
        self._pos = pos
        self._size = size
        self._parent = parent
        self._visible = visible
        self.get_offset_x = lambda: 0
        self.get_offset_y = lambda: 0

        self.highlighted =None

    @property
    def size(self):
        return self._size

    @property
    def visible(self):
        return self._visible

    @property
    def pos(self):
        return self._pos[0] + self.get_offset_x(), self._pos[1] + self.get_offset_y()

    @property
    def parent(self):
        return self._parent

    @property
    def screenFlags(self):
        return self._screenFlags

    @property
    def name(self):
        return self._name

    @property
    def elements(self):
        return self._elements["allElements"]

    @property
    def interactiveElements(self):
        return self._elements["interactive"]
    
    @property
    def elementsByName(self):
        return dict(
            map(
            lambda element: [element.name, element],
            self._elements["allElements"]
        )
        )

    @property
    def screen(self):
        return self._screen

    def update_hitbox(self):
        self._hitbox.x = int(self._pos[0] + self.get_offset_x())
        self._hitbox.y = int(self._pos[1] + self.get_offset_y())

    @size.setter
    def size(self, value):
        oldSize = self._size
        self._screen = pygame.Surface(value, *self._screenFlags)
        self._size = value
        self._hitbox = self._screen.get_rect()
        self.update_hitbox()

        for element in self._elements["allElements"]:
            xPercent = element.x / oldSize[0]
            yPercent = element.y / oldSize[1]
            element.x = xPercent * value[0]
            element.y = yPercent * value[1]

            widthPercent = element.hitbox.width / oldSize[0]
            heightPercent = element.hitbox.height / oldSize[1]

            if type(element) == Text:
                element.size = element.size / oldSize[0] * value[0]

            element.resize_image(widthPercent * value[0], heightPercent * value[1])

        self.update()

    @pos.setter
    def pos(self, value):
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

    def append_element(self, element):
        if element._parent is not None:
            element._parent.remove_element(element)
        if element not in self._elements["allElements"]:
            self._elements["allElements"].append(element)
        if element.interactive:
            self._elements["interactive"].append(element)
        element._parent = self

    def remove_element(self, element):
        if element in self._elements["allElements"]:
            self._elements["allElements"].remove(element)
        if element in self._elements["interactive"]:
            self._elements["interactive"].remove(element)
        element._parent = None

    def insert_element(self, element, index):
        self.remove_element(element)
        self._elements["allElements"].insert(index, element)
        if element.interactive:
            self._elements["interactive"].insert(index, element)
        element._parent = self

    def set_element_interactive(self, element, isInteractive):
        if element is not None and element in self._elements["allElements"]:
            element._interactive = isInteractive
            if isInteractive:
                self._elements["interactive"].append(element)
            elif element in self._elements["interactive"]:
                self._elements["interactive"].remove(element)

    def move_element_forward(self, element, amount):
        if element in self._elements["allElements"]:
            index = self._elements["allElements"].index(element)

            self.insert_element(element, max(index + amount, 0))

    def move_element_backward(self, element, amount):
        if element in self._elements["allElements"]:
            index = self._elements["allElements"].index(element)

            self.insert_element(element, max(index - amount, 0))
            
    def collidepoint(self, element, x, y):
        if element.hitbox is not None:
            return element.hitbox.collidepoint(x, y)
        
        elif element.__ClassName__ == "Group":
            return pygame.Rect(element.x, element.y, element.width, element.height).collidepoint(x, y)
        
        return False

    def is_element_at_pos(self, x, y, onlyInteractive=False, onlyVisible=False):
        sortedElements = sorted(
            self._elements[["allElements", "interactive"][onlyInteractive]],
            key=lambda element: self.collidepoint(element, x, y) and (element.visible or onlyVisible),
        )

        if sortedElements != [] and sortedElements[0].hitbox.collidepoint(x, y):
            return True
        return False
    
    

    def get_element_at_pos(self, x, y, onlyInteractive=False, onlyVisible=False):
         
        sortedElements = sorted(
            self._elements[["allElements", "interactive"][onlyInteractive]],
            key=lambda element: self.collidepoint(element, x, y) and (element.visible or onlyVisible),
        )

        if sortedElements != [] and sortedElements[0].hitbox.collidepoint(x, y):
            return sortedElements[0]
        return None

    def get_elements_at_pos(self, x, y, onlyInteractive=False, onlyVisible=False):
        return list(
            filter(
                lambda element: self.collidepoint(element, x, y) and (element.visible or onlyVisible),
                self._elements[["allElements", "interactive"][onlyInteractive]],
            )
        )

    def pre_update(self, *args, **kwargs):
        pass

    def post_update(self, *args, **kwargs):
        pass

    def element_pre_update(self, element, *args, **kwargs):
        pass

    def element_post_update(self, element, *args, **kwargs):
        pass

    def update(self, *args, **kwargs):
        self._screen.fill((0, 0, 0, 0))
        self.pre_update(self, *args, **kwargs)
        for element in self._elements["allElements"]:
            self.element_pre_update(self, element, *args, **kwargs)
            element.update(screen=self._screen, *args, **kwargs)
            self.element_post_update(self, element, *args, **kwargs)

        self.post_update(self, *args, **kwargs)

    def draw(self, screen=None):
        if screen != None:
            screen.blit(
                self._screen,
                (
                    self._pos[0] + self.get_offset_x(),
                    self._pos[1] + self.get_offset_y(),
                ),
            )
