from .room import Room
import math
import random
from . import Definitions
def generate_image_layout(dungeon):
        
        dungeon.generate_tiles()
        
        dungeon.dungeonLayout = {}
        layer0 = {}
        layer1 = {}
        
        brickWall = Definitions.MODELS["Brick_Wall"].images
        border= Definitions.MODELS["Wood_Border"].images
        brickFloor= Definitions.MODELS["Brick"].images
        
        for coord in dungeon.tiles:
            i,j = coord
            tileType = dungeon.tiles[coord]
            tileName = Definitions.TILE_NAMES[tileType]
            roomX = i // Definitions.ROOM_SIZE[0]
            roomY = j // Definitions.ROOM_SIZE[1]
            room = dungeon.rooms.get((roomX, roomY))
            
            if room:
                if tileName == "FLOOR" or tileType in Definitions.TAGS_TILES["TRANSPARENT"]:
                    for layer in brickFloor[0]:
                        layer0[layer] = layer0.get(layer, {})
                        layer0[layer][(i,j)] = brickFloor[0][layer]
                        
                if tileName == "WALL" or tileName == "CONDITIONAL_DOOR": 
                    for layer in brickWall[0]:
                        layer1[layer] = layer1.get(layer, {})
                        layer1[layer][(i,j)] = brickWall[0][layer]
                
                elif tileName == "CONDITIONAL_WALL":
                    for layer in brickWall[0]:
                        layer1[layer] = layer1.get(layer, {})
                        layer1[layer][(i,j)] = brickWall[0][layer]
                        
                elif tileName == "DOOR":
                    if room.locked:
                        for layer in border[0]:
                            layer1[layer] = layer1.get(layer, {})
                            layer1[layer][(i,j)] = border[0][layer]
                        
                elif tileName == "CONDITIONAL_DOOR":
                    if room.locked:
                        for layer in border[0]:
                            layer1[layer] = layer1.get(layer, {})
                            layer1[layer][(i,j)] = border[0][layer]
                        
        dungeon.dungeonLayout[0] = layer0
        dungeon.dungeonLayout[max(layer0)] = layer1