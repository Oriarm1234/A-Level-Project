import pygame
import OverlayManager
from .Overlay import Overlay


class OverlayManager:

    def __init__(self, 
                 Name:str, 
                 Size:list[int], 
                 Pos:list[int], 
                 Parent:OverlayManager,
                 ScreenFlags:list[int] = [],
                 Overlays:list[Overlay] = []):
        
        self._overlays = Overlays
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
    def ScreenFlags(self): return self._screen_flags

    @property
    def Name(self): return self._name

    @property
    def Overlays(self): return self._overlays

    @property
    def Screen(self): return self._screen


    def appendOverlays(self, overlay):
        if overlay not in self.overlays:
            self.overlays.append(overlay)

    def removeOverlays(self, overlay):
        if overlay in self.overlays:
            self.overlays.remove(overlay)

    def insertOverlays(self, overlay, index):
        self.removeOverlays(overlay)
        self.overlays.insert(index, overlay)

    def moveOverlayForward(self, overlay, amount):
        if overlay in self.Overlays:
            index = self.overlays.index(overlay)

            self.insertOverlay(overlay, max(index+amount, 0))

    def moveOverlayBackward(self, overlay, amount):
        if overlay in self.overlays:
            index = self.overlays.index(overlay)
            
            self.insertOverlay(overlay, max(index-amount, 0))
        
    def IsOverlayAtPos(self, x, y):

        SortedOverlays = sorted(self.overlays, key=lambda Overlay:Overlay.Hitbox.collidepoint(x,y))

        if SortedOverlays != [] and SortedOverlays[0].Hitbox.collidepoint(x,y):
            return True
        return False
    
    def GetOverlayAtPos(self, x, y):
        SortedOverlays = sorted(self.overlays, key=lambda Overlay:Overlay.Hitbox.collidepoint(x,y))

        if SortedOverlays != [] and SortedOverlays[0].Hitbox.collidepoint(x,y):
            return SortedOverlays[0]
        return None
    
    def GetOverlaysAtPos(self, x, y):

        return list(filter(lambda Overlay: Overlay.Hitbox.collidepoint(x,y), self.overlays))
    
    def updateScreen(self):
        self.screen.fill((0,0,0,0))
        for overlay in self.overlays:
            overlay.update(screen = self.screen)
        