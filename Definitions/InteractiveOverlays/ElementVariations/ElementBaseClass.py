import pygame


class Element:
    
    __ClassName__ = "Element"
    
    def __init__(
        self,
        name,
        image,
        pos,
        parent=None,
        imageName="",
        isInteractive=False,
        hitbox=None,
        visible=True,
    ):
        self.image = image
        self.baseImage = image.copy() if image is not None else None
        self.name = name

        self._interactive = isInteractive

        self.get_offset_x = lambda: 0
        self.get_offset_y = lambda: 0


        self.pressed = None
        self.released = None
        self.held_down = None
        self.other_element_pressed = None
        self.imageName = imageName
        self._visible = visible
        
        self.update_function = lambda self, screen, *args, **kwargs: False
        
        if image != None:
            self.hitbox = self.image.get_rect()
        else:
            self.hitbox = hitbox # type: ignore

        self._x, self._y = pos
        self.x, self.y = pos
        
        self._parent = parent
        self.parent = parent
        
    @property
    def visible(self):
        return self._visible
    
    @visible.setter
    def visible(self, value):
        self._visible = value
        return value

    @property
    def x(self):
        return self._x + self.get_offset_x()

    @property
    def y(self):
        return self._y + self.get_offset_y()

    @x.setter
    def x(self, value):
        self._x = value
        if type(self.hitbox) == pygame.Rect:
            self.update_hitbox()
        return value

    @y.setter
    def y(self, value):
        self._y = value
        if type(self.hitbox) == pygame.Rect:
            self.update_hitbox()
        return value

    @property
    def parent(self):
        return self._parent

    @property
    def interactive(self):
        return self._interactive

    @interactive.setter
    def interactive(self, value):
        if self._parent is not None:
            self._parent.set_element_interactive(self, value)

        return value

    @parent.setter
    def parent(self, newParent):
        if self._parent is not None:
            self._parent.remove_element(self)
        if newParent is not None:
            newParent.append_element(self)
        

    def update_hitbox(self):
        if type(self.hitbox) == pygame.Rect:
            self.hitbox.x = self._x + self.get_offset_x()
            self.hitbox.y = self._y + self.get_offset_y()

    def draw(self, *args, **kwargs):
        pass

    def resize_image(self, width, height):
        image = self.baseImage if self.baseImage is not None else self.image

        self.image = pygame.transform.scale(image, (width, height))
        self.hitbox = self.image.get_rect()
        self.update_hitbox()

    def resize_image_by_amount(self, width, height):
        image = self.baseImage if self.baseImage is not None else self.image

        if type(self.hitbox) == pygame.Rect:
            self.image = pygame.transform.scale(
                image, (self.hitbox.w + width, self.hitbox.h + height)
            )
            self.hitbox = self.image.get_rect()
            self.update_hitbox()

    def crop_image(self, x, y, width, height):
        try:
            self.image = self.image.subsurface(pygame.Rect(x, y, width, height))
            self.hitbox = self.image.get_rect()
            self.update_hitbox()
        except Exception:
            return False

    @property
    def alignMode(self):
        return self._alignMode

    def align_to_center(self):
        if type(self.hitbox) == pygame.Rect:
            self.hitbox: pygame.Rect

            self.get_offset_x = lambda: -self.hitbox.w / 2
            self.get_offset_y = lambda: -self.hitbox.h / 2
            self.update_hitbox()
            self._alignMode = "Center"

    def align_to_top_left(self):
        if type(self.hitbox) == pygame.Rect:
            self.hitbox: pygame.Rect

            self.get_offset_x = lambda: -self.hitbox.w
            self.get_offset_y = lambda: -self.hitbox.h
            self.update_hitbox()
            self._alignMode = "TopLeft"

    def align_to_top_middle(self):
        if type(self.hitbox) == pygame.Rect:
            self.hitbox: pygame.Rect

            self.get_offset_x = lambda: -self.hitbox.w / 2
            self.get_offset_y = lambda: -self.hitbox.h
            self.update_hitbox()
            self._alignMode = "TopMiddle"

    def align_to_top_right(self):
        if type(self.hitbox) == pygame.Rect:
            self.hitbox: pygame.Rect

            self.get_offset_x = lambda: 0
            self.get_offset_y = lambda: -self.hitbox.h
            self.update_hitbox()
            self._alignMode = "TopRight"

    def align_to_middle_right(self):
        if type(self.hitbox) == pygame.Rect:
            self.hitbox: pygame.Rect

            self.get_offset_x = lambda: 0
            self.get_offset_y = lambda: -self.hitbox.h / 2
            self.update_hitbox()
            self._alignMode = "MiddleRight"

    def align_to_middle_left(self):
        if type(self.hitbox) == pygame.Rect:
            self.hitbox: pygame.Rect

            self.get_offset_x = lambda: -self.hitbox.w
            self.get_offset_y = lambda: -self.hitbox.h / 2
            self.update_hitbox()
            self._alignMode = "MiddleLeft"

    def align_to_bottom_left(self):
        if type(self.hitbox) == pygame.Rect:
            self.hitbox: pygame.Rect

            self.get_offset_x = lambda: -self.hitbox.w
            self.get_offset_y = lambda: 0
            self.update_hitbox()
            self._alignMode = "BottomLeft"

    def align_to_bottom_middle(self):
        if type(self.hitbox) == pygame.Rect:
            self.hitbox: pygame.Rect

            self.get_offset_x = lambda: -self.hitbox.w / 2
            self.get_offset_y = lambda: 0
            self.update_hitbox()
            self._alignMode = "BottomMiddle"

    def align_to_bottom_right(self):
        if type(self.hitbox) == pygame.Rect:
            self.hitbox: pygame.Rect

            self.get_offset_x = lambda: 0
            self.get_offset_y = lambda: 0
            self.update_hitbox()
            self._alignMode = "BottomRight"

    @staticmethod
    def pre_update(object, screen, *args, **kwargs):
        pass

    @staticmethod
    def post_update(object, screen, *args, **kwargs):
        pass

    def update(self, screen, *args, **kwargs):
        self.pre_update(self, screen, *args, **kwargs)
        
        self.update_function(self, screen, *args, **kwargs)

        self.post_update(self, screen, *args, **kwargs)

        self.draw(screen, *args, **kwargs)

    def move_forwards(self, amount):
        if self.parent != None and self in self.parent.elements:
            index = self.parent.elements.index(self)

            self.parent.insert_element(self, max(index + amount, 0))

    def move_backwards(self, amount):
        if self.parent != None and self in self.parent.elements:
            index = self.parent.elements.index(self)

            self.parent.insert_element(self, max(index - amount, 0))
    
    def bring_to_front(self):
        if self.parent != None and self in self.parent.elements:
            self.parent.insert_element(self, len(self.parent.elements))
    
    def send_to_back(self):
        if self.parent != None and self in self.parent.elements:
            self.parent.insert_element(self, 0)
            
            
            
    def copy(self):
        copy = type(self).__new__(type(self))
        
        for key in self.__dict__:
            if "copy" in dir(self.__dict__[key]):
                copy.__dict__[key] = self.__dict__[key].copy()
                
            else:
                copy.__dict__[key] = self.__dict__[key]
                
            
        
        return copy
    
    
class ElementList(list):
    def copy(self):
        newList = ElementList()
        for element in self:
            if "copy" in dir(element):
                newList.append(element.copy())
            else:
                newList.append(element)
        return newList

    
                
                
class ElementDict(dict):        
    def copy(self):
        newDict = ElementDict()
        for key in self:
            if "copy" in dir(self[key]):
                newDict[key] = self[key].copy()
            else:
                newDict[key] = self[key]
        return newDict