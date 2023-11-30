import pygame
import random
import time
import Definitions
import math
from DungeonTiles import Tile
MODELS = Definitions.MODELS

class Room:
    roomType = "None"
    def __init__(self, x,y, parent, type = "puzzle", size = Definitions.MEDIUM_ROOM, sides = {}):
        self.x = x
        self.y = y
        self.parent = parent
        self.type = type
        self.roomLayout = {}
        self.size = size
        self.sides = sides
        self.screenRoomSize = (self.size[0] * Definitions.GRID_SQUARE_WIDTH, self.size[1] * Definitions.GRID_SQUARE_HEIGHT)

    def generate(self):
        self.roomLayout = {}
        layer0 = {}
        layer1 = {}
        layer2 = {}
        
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                    
                variation2 = MODELS["Brick"].images[random.randint(0,1)]
                for layer in variation2:
                    layer0[layer] = layer0.get(layer, {})
                    layer0[layer][(i,j)] = variation2[layer]
                
                
                    
        self.roomLayout[0] = layer0
        self.roomLayout[max(layer0)] = layer1   
                
    def draw(self):
        
        layers = {}
        
        for layerIndex in self.roomLayout:
            layer = self.roomLayout[layerIndex]
            layers[layerIndex] = {}
            for index in layer:
                layers[layerIndex][index] = pygame.Surface(self.screenRoomSize, pygame.SRCALPHA)
                layers[layerIndex][index].fill((0,0,0,0))
                for coord in layer[index]:
                    x,y = coord
                    
                    x = (x+.5) * Definitions.GRID_SQUARE_WIDTH
                    y = (y+.5) * Definitions.GRID_SQUARE_HEIGHT
                    
                    img = layer[index][coord]
                    layers[layerIndex][index].blit(img, (x-img.get_width()/2,y-img.get_height()/2))
                
        return layers