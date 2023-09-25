import pygame


class Element:
    def __init__(
        self,
        name,
        image,
        pos,
        parent=None,
        image_name="",
        isInteractive=False,
        Hitbox=None,
    ):
        self.Image = image
        self.BaseImage = image.copy() if image is not None else None
        self.Name = name

        self._interactive = isInteractive

        self.get_offset_x = lambda: 0
        self.get_offset_y = lambda: 0

        self._parent = parent
        self.Parent = parent

        self.pressed = None
        self.released = None
        self.held_down = None
        self.image_name = image_name

        self.update_function = lambda self, screen, *args, **kwargs: False

        
        
        if image != None:
            self.Hitbox = self.Image.get_rect()
        else:
            self.Hitbox = Hitbox # type: ignore

        self._x, self._y = pos
        self.x, self.y = pos

    @property
    def x(self):
        return self._x + self.get_offset_x()

    @property
    def y(self):
        return self._y + self.get_offset_y()

    @x.setter
    def x(self, value):
        self._x = value
        if type(self.Hitbox) == pygame.Rect:
            self.update_hitbox()
        return value

    @y.setter
    def y(self, value):
        self._y = value
        if type(self.Hitbox) == pygame.Rect:
            self.update_hitbox()
        return value

    @property
    def Parent(self):
        return self._parent

    @property
    def Interactive(self):
        return self._interactive

    @Interactive.setter
    def Interactive(self, value):
        if self._parent is not None:
            self._parent.setElementInteractive(self, value)

        return value

    @Parent.setter
    def Parent(self, newParent):
        if self._parent is not None:
            self._parent.removeElement(self)
        if newParent is not None:
            newParent.appendElement(self)
        self._parent = newParent

    def update_hitbox(self):
        if type(self.Hitbox) == pygame.Rect:
            self.Hitbox.x = self._x + self.get_offset_x()
            self.Hitbox.y = self._y + self.get_offset_y()

    def draw(self, *args, **kwargs):
        pass

    def resize_image(self, width, height):
        image = self.BaseImage if self.BaseImage is not None else self.Image

        self.Image = pygame.transform.scale(image, (width, height))
        self.Hitbox = self.Image.get_rect()
        self.update_hitbox()

    def resize_image_by_amount(self, width, height):
        image = self.BaseImage if self.BaseImage is not None else self.Image

        if type(self.Hitbox) == pygame.Rect:
            self.Image = pygame.transform.scale(
                image, (self.Hitbox.w + width, self.Hitbox.h + height)
            )
            self.Hitbox = self.Image.get_rect()
            self.update_hitbox()

    def crop_image(self, x, y, width, height):
        try:
            self.Image = self.Image.subsurface(pygame.Rect(x, y, width, height))
            self.Hitbox = self.Image.get_rect()
            self.update_hitbox()
        except Exception:
            return False

    @property
    def AlignMode(self):
        return self._alignMode

    def align_to_center(self):
        if type(self.Hitbox) == pygame.Rect:
            self.Hitbox: pygame.Rect

            self.get_offset_x = lambda: -self.Hitbox.w / 2
            self.get_offset_y = lambda: -self.Hitbox.h / 2
            self.update_hitbox()
            self._alignMode = "Center"

    def align_to_top_left(self):
        if type(self.Hitbox) == pygame.Rect:
            self.Hitbox: pygame.Rect

            self.get_offset_x = lambda: -self.Hitbox.w
            self.get_offset_y = lambda: -self.Hitbox.h
            self.update_hitbox()
            self._alignMode = "TopLeft"

    def align_to_top_middle(self):
        if type(self.Hitbox) == pygame.Rect:
            self.Hitbox: pygame.Rect

            self.get_offset_x = lambda: -self.Hitbox.w / 2
            self.get_offset_y = lambda: -self.Hitbox.h
            self.update_hitbox()
            self._alignMode = "TopMiddle"

    def align_to_top_right(self):
        if type(self.Hitbox) == pygame.Rect:
            self.Hitbox: pygame.Rect

            self.get_offset_x = lambda: 0
            self.get_offset_y = lambda: -self.Hitbox.h
            self.update_hitbox()
            self._alignMode = "TopRight"

    def align_to_middle_right(self):
        if type(self.Hitbox) == pygame.Rect:
            self.Hitbox: pygame.Rect

            self.get_offset_x = lambda: 0
            self.get_offset_y = lambda: -self.Hitbox.h / 2
            self.update_hitbox()
            self._alignMode = "MiddleRight"

    def align_to_middle_left(self):
        if type(self.Hitbox) == pygame.Rect:
            self.Hitbox: pygame.Rect

            self.get_offset_x = lambda: -self.Hitbox.w
            self.get_offset_y = lambda: -self.Hitbox.h / 2
            self.update_hitbox()
            self._alignMode = "MiddleLeft"

    def align_to_bottom_left(self):
        if type(self.Hitbox) == pygame.Rect:
            self.Hitbox: pygame.Rect

            self.get_offset_x = lambda: -self.Hitbox.w
            self.get_offset_y = lambda: 0
            self.update_hitbox()
            self._alignMode = "BottomLeft"

    def align_to_bottom_middle(self):
        if type(self.Hitbox) == pygame.Rect:
            self.Hitbox: pygame.Rect

            self.get_offset_x = lambda: -self.Hitbox.w / 2
            self.get_offset_y = lambda: 0
            self.update_hitbox()
            self._alignMode = "BottomMiddle"

    def align_to_bottom_right(self):
        if type(self.Hitbox) == pygame.Rect:
            self.Hitbox: pygame.Rect

            self.get_offset_x = lambda: 0
            self.get_offset_y = lambda: 0
            self.update_hitbox()
            self._alignMode = "BottomRight"

    @staticmethod
    def post_update(object, screen, *args, **kwargs):
        pass

    def update(self, screen, *args, **kwargs):
        self.update_function(self, screen, *args, **kwargs)

        self.post_update(self, screen, *args, **kwargs)

        self.draw(screen, *args, **kwargs)

    def move_forwards(self, amount):
        if self.Parent != None and self in self.Parent.Elements:
            index = self.Parent.Elements.index(self)

            self.Parent.insertElement(self, max(index + amount, 0))

    def move_backwards(self, amount):
        if self.Parent != None and self in self.Parent.Elements:
            index = self.Parent.Elements.index(self)

            self.Parent.insertElement(self, max(index - amount, 0))
