import pygame
from ...InteractiveOverlays import Text, Overlay

class OverlayManager:
    __ClassName__ = "OverlayManager"
    def __init__(
        self,
        name: str,
        size: tuple[int, int],
        pos: tuple[int, int],
        screenFlags: list[int] = [],
        overlays: list = [],
        colour: tuple[int, int, int, int] = (0, 0, 0, 0),
    ):
        """
        Initializes an OverlayManager instance.

        The constructor sets up internal state like overlays, screen, name, etc.
        It also initializes a held_down dict for tracking pressed keys.

        Args:
        self: The OverlayManager instance being initialized.
        name (str): The name of the OverlayManager.
        size (tuple[int, int]): The size of the managed screen surface.
        pos (tuple[int, int]): The position of the OverlayManager.
        screenFlags (list[int]): Optional flags for the managed screen surface.
        overlays (list): The initial list of managed overlays.
        colour (tuple[int, int, int, int]): The color to fill the screen surface with.
        
        """
        self._overlays = overlays
        self._screen = pygame.Surface(size, *screenFlags)
        self._screen.fill((0, 0, 0, 0))

        self._hitbox = self._screen.get_rect()
        self._name = name
        self._screenFlags = screenFlags
        self._size = size
        self._colour = colour

        self._x, self._y = pos
        self.x, self.y = pos

        self.held_down = {}

    @property
    def size(self):
        return self._size

    @property
    def screenFlags(self):
        return self._screenFlags

    @property
    def name(self):
        return self._name

    @property
    def overlays(self):
        return self._overlays

    @property
    def screen(self):
        return self._screen
    
    def update_hitbox(self):
        self._hitbox.x = self.x
        self._hitbox.y = self.y
    
    @size.setter
    def size(self, value):
        oldSize = self._size
        self._screen = pygame.Surface(value, *self._screenFlags)
        self._size = value
        self._hitbox = self._screen.get_rect()
        self.update_hitbox()

        for overlay in self._overlays:
            xPercent = overlay.pos[0] / oldSize[0]
            yPercent = overlay.pos[1] / oldSize[1]
            overlay.pos = xPercent * value[0], yPercent * value[1]


    def get_state_event(self, event):
        return self.held_down.get(event, False)

    def set_state_event(self, event, state):
        self.held_down[event] = state
        return state

    def append_overlay(self, overlay):
        if overlay._parent is not None:
            overlay._parent.remove_overlay(overlay)
        if overlay not in self._overlays:
            self._overlays.append(overlay)
        overlay._parent = self

    def remove_overlay(self, overlay):
        if overlay in self._overlays:
            self._overlays.remove(overlay)
        overlay._parent = None

    def insert_overlay(self, overlay, index):
        self.remove_overlay(overlay)
        self._overlays.insert(index, overlay)
        overlay._parent = self

    def move_overlay_forward(self, overlay, amount):
        if overlay in self.overlays:
            index = self._overlays.index(overlay)

            self.insert_overlay(overlay, max(index + amount, 0))

    def move_overlay_backward(self, overlay, amount):
        if overlay in self._overlays:
            index = self._overlays.index(overlay)

            self.insert_overlay(overlay, max(index - amount, 0))

    def is_overlay_at_pos(self, x, y):
        sortedOverlays = list(
            filter(
                self._overlays, key=lambda overlay: overlay._hitbox.collidepoint(x, y)
            )
        )

        if sortedOverlays != [] and sortedOverlays[0]._hitbox.collidepoint(x, y):
            return True
        return False

    def get_overlay_at_pos(self, x, y): 
        return (result[0] if len(result:=
            list(
                overlay
                for overlay in self._overlays[::-1]
                if overlay._hitbox.collidepoint(x, y)
            )) else\
            None
        )

    def get_overlays_at_pos(self, x, y, shouldBeVisible=False):
        overlays = []
        
        for overlay in self._overlays:
            if (overlay._visible or not shouldBeVisible) and overlay.collidepoint(x, y):
                overlays.append(overlay)
        
        
        return overlays
    
    def get_overlay_by_name(self, name):
        
        overlays = []
        
        for overlay in self._overlays:
            if overlay.name == name:
                overlays.append(overlay)
        
        
        return overlays[0] if len(overlays) != 0 else None

    def get_visible_overlays(self):
        return list(filter(lambda x: x._visible, self._overlays))

    def set_overlay_visible(self, overlay, visible=True):
        assert type(overlay) == Overlay, f"overlay needs to be of type Overlay, not {type(overlay)}"
        overlay._visible = visible


    @staticmethod
    def pre_update(overlayManager, *args, **kwargs):
        pass

    @staticmethod
    def post_update(overlayManager, *args, **kwargs):
        pass

    @staticmethod
    def pre_draw(overlayManager, *args, **kwargs):
        pass

    @staticmethod
    def post_draw(overlayManager, *args, **kwargs):
        pass

    @staticmethod
    def pre_overlay_update(overlayManager, overlay, *args, **kwargs):
        pass

    @staticmethod
    def post_overlay_update(overlayManager, overlay, *args, **kwargs):
        pass

    @staticmethod
    def pre_overlay_draw(overlayManager, overlay, *args, **kwargs):
        pass

    @staticmethod
    def post_overlay_draw(overlayManager, overlay, *args, **kwargs):
        pass

    def update(self, *args, **kwargs):
        """Updates the OverlayManager by calling various pre/post update hooks and 
        drawing all visible overlays.

        Args:
        self: The OverlayManager instance.
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

        Returns: 
        None
        """
        self._screen.fill((0, 0, 0, 0))
        
        overlays = self.get_visible_overlays()

        self.pre_update(self, *args, **kwargs)  #

        for overlay in overlays:
            self.pre_overlay_update(self, overlay, *args, **kwargs)
            overlay.update(*args, **kwargs)
            self.post_overlay_update(self, overlay, *args, **kwargs)

        self.post_update(self, *args, **kwargs)

        self.pre_draw(self, *args, **kwargs)

        for overlay in overlays:
            self.pre_overlay_draw(self, overlay, *args, **kwargs)
            overlay.draw(screen=self._screen)
            self.post_overlay_draw(self, overlay, *args, **kwargs)

        self.post_draw(self, *args, **kwargs)
