import pygame
import Definitions
from DungeonTiles import Tile

class Room:
    roomType = "None"
    def __init__(self, x,y, parent, type = "puzzle", size = Definitions.SMALL_ROOM, sides = {}):
        self.x = x
        self.y = y
        self.parent = parent
        self.type = type
        self.roomLayers = {}
        self.size = size
        self.sides = sides

    def generate(self):
        screenSize = pygame.Surface((self.size[0] * Definitions.GRID_SQUARE_WIDTH, self.size[1] * Definitions.GRID_SQUARE_HEIGHT))
        #layer 0
        layer0 = pygame.Surface(screenSize, pygame.SRCALPHA)
        