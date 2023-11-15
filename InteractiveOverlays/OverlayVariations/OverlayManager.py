import pygame


class OverlayManager:
    __ClassName__ = "OverlayManager"
    def __init__(
        self,
        Name: str,
        Size: tuple[int, int],
        Pos: tuple[int, int],
        ScreenFlags: list[int] = [],
        Overlays: list = [],
        Colour: tuple[int, int, int, int] = (0, 0, 0, 0),
    ):
        """
        Initializes an OverlayManager instance.

        The constructor sets up internal state like overlays, screen, name, etc.
        It also initializes a held_down dict for tracking pressed keys.

        Args:
        self: The OverlayManager instance being initialized.
        Name (str): The name of the OverlayManager.
        Size (tuple[int, int]): The size of the managed screen surface.
        Pos (tuple[int, int]): The position of the OverlayManager.
        ScreenFlags (list[int]): Optional flags for the managed screen surface.
        Overlays (list): The initial list of managed overlays.
        Colour (tuple[int, int, int, int]): The color to fill the screen surface with.
        
        """
        self._overlays = Overlays
        self._screen = pygame.Surface(Size, *ScreenFlags)
        self._screen.fill((0, 0, 0, 0))

        self._hitbox = self._screen.get_rect()
        self._name = Name
        self._screen_flags = ScreenFlags
        self._size = Size
        self._colour = Colour
        self._visibleOverlay = None

        self.held_down = {}

    @property
    def Size(self):
        return self._size

    @property
    def ScreenFlags(self):
        return self._screen_flags

    @property
    def Name(self):
        return self._name

    @property
    def Overlays(self):
        return self._overlays

    @property
    def Screen(self):
        return self._screen

    def getStateEvent(self, event):
        return self.held_down.get(event, False)

    def setStateEvent(self, event, state):
        self.held_down[event] = state
        return state

    def appendOverlay(self, overlay):
        if overlay._parent is not None:
            overlay._parent.removeOverlay(overlay)
        if overlay not in self._overlays:
            self._overlays.append(overlay)
        overlay._parent = self

    def removeOverlay(self, overlay):
        if overlay in self._overlays:
            self._overlays.remove(overlay)
        overlay._parent = None

    def insertOverlay(self, overlay, index):
        self.removeOverlay(overlay)
        self._overlays.insert(index, overlay)
        overlay._parent = self

    def moveOverlayForward(self, overlay, amount):
        if overlay in self.Overlays:
            index = self._overlays.index(overlay)

            self.insertOverlay(overlay, max(index + amount, 0))

    def moveOverlayBackward(self, overlay, amount):
        if overlay in self._overlays:
            index = self._overlays.index(overlay)

            self.insertOverlay(overlay, max(index - amount, 0))

    def IsOverlayAtPos(self, x, y):
        SortedOverlays = list(
            filter(
                self._overlays, key=lambda Overlay: Overlay._hitbox.collidepoint(x, y)
            ) # type: ignore
        )

        if SortedOverlays != [] and SortedOverlays[0]._hitbox.collidepoint(x, y):
            return True
        return False

    def GetOverlayAtPos(self, x, y):
        return next(
            (
                Overlay
                for Overlay in self._overlays[::-1]
                if Overlay._hitbox.collidepoint(x, y)
            ),
            None,
        )

    def GetOverlaysAtPos(self, x, y, shouldBeVisible=False):
        return [
            Overlay
            for Overlay in self._overlays
            if (Overlay._visible or not shouldBeVisible)
            and Overlay._hitbox.collidepoint(x, y)
        ]

    def getOverlayByName(self, name):
        return next(
            (Overlay for Overlay in self._overlays if Overlay._name == name), None
        )

    def getVisibleOverlays(self):
        return list(filter(lambda x: x._visible, self._overlays))

    def SetOverlayVisible(self, Overlay, Visible=True):
        Overlay._visible = Visible
        self._visibleOverlay = Overlay

    @staticmethod
    def preUpdate(overlayManager, *args, **kwargs):
        pass

    @staticmethod
    def postUpdate(overlayManager, *args, **kwargs):
        pass

    @staticmethod
    def preDraw(overlayManager, *args, **kwargs):
        pass

    @staticmethod
    def postDraw(overlayManager, *args, **kwargs):
        pass

    @staticmethod
    def preOverlayUpdate(overlayManager, overlay, *args, **kwargs):
        pass

    @staticmethod
    def postOverlayUpdate(overlayManager, overlay, *args, **kwargs):
        pass

    @staticmethod
    def preOverlayDraw(overlayManager, overlay, *args, **kwargs):
        pass

    @staticmethod
    def postOverlayDraw(overlayManager, overlay, *args, **kwargs):
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
        
        overlays = self.getVisibleOverlays()

        self.preUpdate(self, *args, **kwargs)  #

        for overlay in overlays:
            self.preOverlayUpdate(self, overlay, *args, **kwargs)
            overlay.update(*args, **kwargs)
            self.postOverlayUpdate(self, overlay, *args, **kwargs)

        self.postUpdate(self, *args, **kwargs)

        self.preDraw(self, *args, **kwargs)

        for overlay in overlays:
            self.preOverlayDraw(self, overlay, *args, **kwargs)
            overlay.draw(screen=self._screen)
            self.postOverlayDraw(self, overlay, *args, **kwargs)

        self.postDraw(self, *args, **kwargs)
