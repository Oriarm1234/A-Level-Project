import pygame
import random
import time
import Definitions
import math
from DungeonTiles import Tile
MODELS = Definitions.MODELS

class Room:
    roomType = "None"
    def __init__(self, x,y, parent, type = "puzzle", shape = ("Name", ((0,0,0),(0,0,0),(0,0,0))), sides = {}, id = 0,locked = False,zoneId=0):
        self.x = x
        self.y = y
        self.parent = parent
        self.type = type
        self.roomLayout = {}
        self.shapeType = shape[0]
        self.shape = list(dict(((x*Definitions.ROOM_SIZE[0]+i,y*Definitions.ROOM_SIZE[1]+j),tileType) for i,tileType in enumerate(row)) for j,row in enumerate(shape[1]))  # convert to list of dicts
        shape = {}
        for Dict in self.shape:
            shape.update(Dict)
        self.shape = shape
        self.sides = sides
        self.sideRooms = {}
        self.locked = locked
        self.id = id
        self.zoneId = zoneId
        
        minPointX = min(self.shape, key = lambda coord: coord[0])[0]
        maxPointX = max(self.shape, key = lambda coord: coord[0])[0] + 1
        
        minPointY = min(self.shape, key = lambda coord: coord[1])[1]
        maxPointY = max(self.shape, key = lambda coord: coord[1])[1] + 1
        self.screenRoomSize = (abs(maxPointX-minPointX) * Definitions.GRID_SQUARE_WIDTH+2, abs(maxPointY-minPointY) * Definitions.GRID_SQUARE_HEIGHT+2)

        
