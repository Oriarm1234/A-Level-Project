import pygame
from . import Dungeon
from . import Definitions

class Renderer: #Using a class object as a container, there should only ever be one instance in use.
    """
    The renderer class should only ever have one instance."""
    def __init__(self, dungeon:Dungeon.Dungeon, cameraObject):
        """
        The camera object can be any object that has an x and y position in terms of tile positions.
        The renderer will focus on this object, if the renderer does not have a cameraObject it will use the last used position
        """
        self.dungeon = dungeon
        self.cameraObject = cameraObject
        
        if cameraObject is not None:
            self._xPos,self._yPos = cameraObject.x,cameraObject.y
        else:
            self._xPos,self._yPos = (0,0) #Default camera pos
            
        self.lastPos = None
            
        self._offsetX = -Definitions.ROOM_SIZE[0] / 2 # Middle X pos of the room
        self._offsetY = -Definitions.ROOM_SIZE[1] / 2 # Middle Y pos of the room
        
        self.layers = {}
        
    @property
    def xPos(self):
        if self.cameraObject is not None:
            self._xPos = self.cameraObject.x
        
        return self._xPos
    
    @property
    def yPos(self):
        if self.cameraObject is not None:
            self._yPos = self.cameraObject.y
        
        return self._yPos
    
    @xPos.setter
    def xPos(self, newValue):
        self.cameraObject = None

        self._xPos = newValue
            
        return self._xPos
    
    @yPos.setter
    def yPos(self, newValue):
        self.cameraObject = None

        self._yPos = newValue
            
        return self._yPos
        
    
            
    def get_screen_pos_for_tile(self, x,y):
        
        #Takes in an unadjusted tile coordinate and adjusts it to fit the camera position and place it on the screen
        
        screenX = (x+self._offsetX-self.xPos)*Definitions.GRID_SQUARE_WIDTH  # room is centered on (0,0) needs to be centered in middle of screen
        screenY = (y+self._offsetY-self.yPos)*Definitions.GRID_SQUARE_HEIGHT # adjustment is therefore needed
        return screenX + Definitions.SCREEN_SIZE[0]/2, screenY + Definitions.SCREEN_SIZE[1]/2
    
    def get_screen_pos_for_room(self, x, y):    
        
        #Takes in an unadjusted room coordinate and adjusts it to fit the camera position and place it on the screen

        screenX = (x*Definitions.ROOM_SIZE[0]+self._offsetX-self.xPos)*Definitions.GRID_SQUARE_WIDTH  # room is centered on (0,0) needs to be centered in middle of screen
        screenY = (y*Definitions.ROOM_SIZE[1]+self._offsetY-self.yPos)*Definitions.GRID_SQUARE_HEIGHT # adjustment is therefore needed
        return screenX + Definitions.SCREEN_SIZE[0]/2, screenY + Definitions.SCREEN_SIZE[1]/2
    
    def get_layers(self):
    
        xPos = self.xPos
        yPos = self.yPos
        
        if self.lastPos != (xPos,yPos):
            self.lastPos = xPos,yPos 
            
            self.layers = self.dungeon.get_layers(Definitions.SCREEN_SIZE,(self.lastPos))
            
        
        return self.layers