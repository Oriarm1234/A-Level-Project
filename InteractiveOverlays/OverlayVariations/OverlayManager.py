import pygame


class OverlayManager:

    def __init__(self, 
                 Name:str, 
                 Size:list[int], 
                 Pos:list[int],
                 ScreenFlags:list[int] = [],
                 Overlays:list = [],
                 Colour:list[int] = (0,0,0,0)):
        
        self._overlays = Overlays
        self._screen = pygame.Surface(Size, *ScreenFlags)
        self._screen.fill((0,0,0,0))

        self._hitbox = self._screen.get_rect()
        self._name = Name
        self._screen_flags = ScreenFlags
        self._size = Size
        self._colour = Colour
        self._visibleOverlay = None

        self.held_down = {}


    @property
    def Size(self): return self._size

    @property
    def ScreenFlags(self): return self._screen_flags

    @property
    def Name(self): return self._name

    @property
    def Overlays(self): return self._overlays

    @property
    def Screen(self): return self._screen


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

            self.insertOverlay(overlay, max(index+amount, 0))
        

    def moveOverlayBackward(self, overlay, amount):
        if overlay in self._overlays:
            index = self._overlays.index(overlay)
            
            self.insertOverlay(overlay, max(index-amount, 0))
        
    def IsOverlayAtPos(self, x, y):

        SortedOverlays = list(filter(self._overlays, key=lambda Overlay:Overlay._hitbox.collidepoint(x,y)))

        if SortedOverlays != [] and SortedOverlays[0]._hitbox.collidepoint(x,y):
            return True
        return False
    
    def GetOverlayAtPos(self, x, y):
        overlayAtPos = None
        for Overlay in self._overlays[::-1]:
            if Overlay._hitbox.collidepoint(x,y):
                overlayAtPos = Overlay
                break

        return overlayAtPos
    
    def GetOverlaysAtPos(self, x, y, shouldBeVisible=False):

        overlaysAtPos = []
        for Overlay in self._overlays:
            if (Overlay._visible or not shouldBeVisible) and Overlay._hitbox.collidepoint(x,y):
                overlaysAtPos.append(Overlay)

        return overlaysAtPos
    
    def getOverlayByName(self, name):
        for Overlay in self._overlays:
            if Overlay._name == name:
                return Overlay
            
        return None
    
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

        overlays = self.getVisibleOverlays()
    
        self.preUpdate(self, *args, **kwargs)#

        for overlay in overlays:
            self.preOverlayUpdate(self, overlay, *args, **kwargs)
            overlay.update(*args, **kwargs)
            self.postOverlayUpdate(self, overlay, *args, **kwargs)

        self.postUpdate(self, *args, **kwargs)

        self.preDraw(self, *args, **kwargs)
        
        for overlay in overlays:
            self.preOverlayDraw(self, overlay, *args, **kwargs)
            overlay.draw(screen = self._screen)
            self.postOverlayDraw(self, overlay, *args, **kwargs)

        self.postDraw(self, *args, **kwargs)
        

        