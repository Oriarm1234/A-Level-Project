import pygame

class Element:

    def __init__(self, name, image, pos, parent=None):
        self.Image = image
        self.BaseImage = image.copy()
        self.Name  = name
        

        self.get_offset_x = lambda:0
        self.get_offset_y = lambda:0
        
        self._parent = parent
        self.Parent  = parent

        self.updateFunction = lambda object: False
        
        

        if image != None:
            self.Hitbox:pygame.Rect
            self.Hitbox = self.Image.get_rect()
            self.Hitbox.x,self.Hitbox.y = pos

        self._x, self._y = pos
        self.x,self.y = pos



    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y
    
    @x.setter
    def x(self, value):
        self._x = value
        self.Hitbox.x = value + self.get_offset_x()
        return value
    
    @y.setter
    def y(self, value):
        self._y = value
        self.Hitbox.y = value + self.get_offset_y()
        return value
    
    @property
    def Parent(self):
        return self._parent
    
    @Parent.setter
    def Parent(self, newParent):
        if self._parent != None:
            try:
                self._parent.removeElement(self)
            except:
                pass
            self._parent.appendElement(self)
            self._parent = newParent
    
    def update_hitbox(self):
        self.Hitbox.x = self._x + self.get_offset_x()
        self.Hitbox.y = self._y + self.get_offset_y()


        
    
    def pressed(self, *args, **kwargs):
        pass

    def released(self, *args, **kwargs):
        pass

    def held_down(self, *args, **kwargs):
        pass

    def update(self, *args, **kwargs):
        self.updateFunction(self)

        self.draw(kwargs.get("screen", None))

    def draw(self, *args, **kwargs):
        pass

    def resize_image(self, width, height):
        self.Image =  pygame.transform.scale(self.BaseImage, (width, height))
        self.Hitbox = self.Image.get_rect()
        self.update_hitbox()

    def resize_image_by_amount(self, width, height):
        self.Image =  pygame.transform.scale(self.BaseImage, (self.Hitbox.w + width, self.Hitbox.h + height))
        self.Hitbox = self.Image.get_rect()
        self.update_hitbox()

    def crop_image(self, x, y, width, height):
        try:
            self.Image = self.Image.subsurface(pygame.Rect(x, y, width, height))
            self.Hitbox = self.Image.get_rect()
            self.update_hitbox()
        except:
            return False
    
    @property
    def AlignMode(self):
        return self._alignMode

    def align_to_center(self):
        self.get_offset_x = lambda: -self.Hitbox.w/2
        self.get_offset_y = lambda: -self.Hitbox.h/2
        self.update_hitbox()
        self._alignMode = "Center"

    def align_to_top_left(self):
        self.get_offset_x = lambda: -self.Hitbox.w
        self.get_offset_y = lambda: -self.Hitbox.h
        self.update_hitbox()
        self._alignMode = "TopLeft"
    
    def align_to_top_middle(self):
        self.get_offset_x = lambda: -self.Hitbox.w/2
        self.get_offset_y = lambda: -self.Hitbox.h
        self.update_hitbox()
        self._alignMode = "TopMiddle"
    
    def align_to_top_right(self):
        self.get_offset_x = lambda: 0
        self.get_offset_y = lambda: -self.Hitbox.h
        self.update_hitbox()
        self._alignMode = "TopRight"
    
    def align_to_middle_right(self):
        self.get_offset_x = lambda: 0
        self.get_offset_y = lambda: -self.Hitbox.h/2
        self.update_hitbox()
        self._alignMode = "MiddleRight"

    def align_to_middle_left(self):
        self.get_offset_x = lambda: -self.Hitbox.w
        self.get_offset_y = lambda: -self.Hitbox.h/2
        self.update_hitbox()
        self._alignMode = "MiddleLeft"
    
    def align_to_bottom_left(self):
        self.get_offset_x = lambda: -self.Hitbox.w
        self.get_offset_y = lambda: 0
        self.update_hitbox()
        self._alignMode = "BottomLeft"
    
    def align_to_bottom_middle(self):
        self.get_offset_x = lambda: -self.Hitbox.w/2
        self.get_offset_y = lambda: 0
        self.update_hitbox()
        self._alignMode = "BottomMiddle"
    
    def align_to_bottom_right(self):
        self.get_offset_x = lambda: 0
        self.get_offset_y = lambda: 0
        self.update_hitbox()
        self._alignMode = "BottomRight"

    def update(self, update_function = lambda object:False, screen = None):
        update_function(self)

        self.draw(screen)

    def move_forwards(self, amount):
        if self.Parent != None and self in self.Parent.Elements:
            index = self.Parent.Elements.index(self)
            
            self.Parent.insertElement(self, max(index+amount, 0))

    def move_backwards(self, amount):
        if self.Parent != None and self in self.Parent.Elements:
            index = self.Parent.Elements.index(self)
            
            self.Parent.insertElement(self, max(index-amount, 0))
