import pygame
import glob
import json
from . import DungeonTiles
import time
GRID_SQUARE_WIDTH = 74
GRID_SQUARE_HEIGHT = 74


def loadModels(models = {}):
    files = glob.glob("Game\\Images\\**\\*.png", recursive=True)

    for fileName in files:
        if "NONMODEL" in fileName:
            continue
        dictionaryLocation = fileName.split("\\")[1:][:-1]
        imageLayer = fileName.split("\\")[-1].split(".")[0]
        variation = dictionaryLocation.pop()
        modelName = dictionaryLocation.pop()
        if modelName not in models:
            models[modelName] = DungeonTiles.Model(modelName,variation, {})
            
        
        try:
            
            imageLayer = int(imageLayer)
            variation = int(variation) if variation.isnumeric() else variation
            
            img = pygame.image.load(fileName)
            img = pygame.transform.smoothscale(img, (GRID_SQUARE_WIDTH,GRID_SQUARE_HEIGHT))
            
            
            
            models[modelName].images[variation] = models[modelName].images.get(variation, {})
            
            models[modelName].images[variation][imageLayer] = img
            
            
            
            
            
        except:
            input("Bad Image, BURN " + fileName)
            
    for modelName, model in models.items():
        for varationKey, variation in model.images.items():
            
            model.images[varationKey] = dict([imgKey, variation[imgKey]] for imgKey in sorted(variation))
            
    return models
SCREEN_SIZE = (800,800)
fogOfWarSizeModifier = 1.5
FOG_OF_WAR_IMAGE = pygame.transform.smoothscale(pygame.image.load("Game\\Images\\NONMODEL\\fogOfWar.png"),(SCREEN_SIZE[0]*fogOfWarSizeModifier,
                                                                                                     SCREEN_SIZE[1]*fogOfWarSizeModifier))

O = 0 # PERMENANT EMPTY AREA - FLOOR
T = 1 # GENERATIVE AREA
D = 2 # ALWAYS DOOR
N = 3 # DOOR, IF CONNECTED TO WALL, ELSE O
W = 4 # ALWAYS WALL
M = 5 # WALL IF RANDOM(0,MAXAMOUNT) = 0 ELSE AIR, !!!!WILL FORCE NEIGHBOUR WT TO BECOME AIR IF SELF IS AIR, IF NEIGHBOUR IS VOID - WILL BE WALL
V = 6 # VOID
TILE_TYPES = {
    "FLOOR": O,
    "GENERATIVE_AREA": T,
    "DOOR": D,
    "CONDITIONAL_DOOR":N,
    "WALL":W,
    "CONDITIONAL_WALL":M,
    "VOID":V
}
TAGS_TILES = {
    "TRANSPARENT":(T,D,N,M,W)
}

FLOOR_HEIGHT = 5

TILE_NAMES = dict(
    [value, key] for key,value in list(TILE_TYPES.items())
)


ROOM_SIZE = (7,7)
loadArea = 7

EMPTY_ROOM = (
(O,O,O,O,O,O,O),
(O,T,T,T,T,T,O),
(O,T,T,T,T,T,O),
(O,T,T,T,T,T,O),
(O,T,T,T,T,T,O),
(O,T,T,T,T,T,O),
(O,O,O,O,O,O,O)
)

EMPTY2_ROOM = (
(O,O,O,O,O,O,O),
(O,T,T,O,T,T,O),
(O,T,T,O,T,T,O),
(O,O,O,O,O,O,O),
(O,T,T,O,T,T,O),
(O,T,T,O,T,T,O),
(O,O,O,O,O,O,O)
)

OPEN_TEMPLATE = (
(W,O,O,O,O,O,W),
(O,O,T,T,T,O,O),
(O,T,T,T,T,T,O),
(O,T,T,T,T,T,O),
(O,T,T,T,T,T,O),
(O,O,T,T,T,O,O),
(W,O,O,O,O,O,W)
)
CORNED_ROOM_TEMPLATE = (
(W,N,N,N,N,N,W),
(N,O,O,O,O,O,N),
(N,O,T,T,T,O,N),
(N,O,T,T,T,O,N),
(N,O,T,T,T,O,N),
(N,O,O,O,O,O,N),
(W,N,N,N,N,N,W)
)
NS_CORRIDOR = (
    (W,W,N,N,N,W,W),
    (W,O,O,O,O,O,W),
    (W,O,O,O,O,O,W),
    (W,O,O,O,O,O,W),
    (W,O,O,O,O,O,W),
    (W,O,O,O,O,O,W),
    (W,W,N,N,N,W,W)
)
WE_CORRIDOR = (
    (W,W,W,W,W,W,W),
    (W,O,O,O,O,O,W),
    (N,O,O,O,O,O,N),
    (N,O,O,O,O,O,N),
    (N,O,O,O,O,O,N),
    (W,O,O,O,O,O,W),
    (W,W,W,W,W,W,W)
)
NE_CORNER = (
    (W,W,N,N,N,W,W),
    (W,O,O,O,O,O,W),
    (W,O,O,O,O,O,N),
    (W,O,O,O,O,O,N),
    (W,O,O,O,O,O,N),
    (W,O,O,O,O,O,W),
    (W,W,W,W,W,W,W)
    
)
NW_CORNER = (
    (W,W,N,N,N,W,W),
    (W,O,O,O,O,O,W),
    (N,O,O,O,O,O,W),
    (N,O,O,O,O,O,W),
    (N,O,O,O,O,O,W),
    (W,O,O,O,O,O,W),
    (W,W,W,W,W,W,W)
    
)
SE_CORNER = (
    (W,W,W,W,W,W,W),
    (W,O,O,O,O,O,W),
    (W,O,O,O,O,O,N),
    (W,O,O,O,O,O,N),
    (W,O,O,O,O,O,N),
    (W,O,O,O,O,O,W),
    (W,W,N,N,N,W,W)
    
)
SW_CORNER = (
    (W,W,W,W,W,W,W),
    (W,O,O,O,O,O,W),
    (N,O,O,O,O,O,W),
    (N,O,O,O,O,O,W),
    (N,O,O,O,O,O,W),
    (W,O,O,O,O,O,W),
    (W,W,N,N,N,W,W)
)
NES_CROSSROAD = (
    (W,W,N,N,N,W,W),
    (W,O,O,O,O,O,W),
    (W,O,O,O,O,O,N),
    (W,O,O,O,O,O,N),
    (W,O,O,O,O,O,N),
    (W,O,O,O,O,O,W),
    (W,W,N,N,N,W,W)
)
NWS_CROSSROAD = (
    (W,W,N,N,N,W,W),
    (W,O,O,O,O,O,W),
    (N,O,O,O,O,O,W),
    (N,O,O,O,O,O,W),
    (N,O,O,O,O,O,W),
    (W,O,O,O,O,O,W),
    (W,W,N,N,N,W,W)
)
ESW_CROSSROAD = (
    (W,W,W,W,W,W,W),
    (W,O,O,O,O,O,W),
    (N,O,O,O,O,O,N),
    (N,O,O,O,O,O,N),
    (N,O,O,O,O,O,N),
    (W,O,O,O,O,O,W),
    (W,W,N,N,N,W,W)
)
NEW_CROSSROAD = (
    (W,W,N,N,N,W,W),
    (W,O,O,O,O,O,W),
    (N,O,O,O,O,O,N),
    (N,O,O,O,O,O,N),
    (N,O,O,O,O,O,N),
    (W,O,O,O,O,O,W),
    (W,W,W,W,W,W,W)
)
N_ROOM = (
    (W,W,N,N,N,W,W),
    (W,O,O,O,O,O,W),
    (W,O,O,O,O,O,W),
    (W,O,O,O,O,O,W),
    (W,O,O,O,O,O,W),
    (W,O,O,O,O,O,W),
    (W,W,W,W,W,W,W)
)
S_ROOM = (
    (W,W,W,W,W,W,W),
    (W,O,O,O,O,O,W),
    (W,O,O,O,O,O,W),
    (W,O,O,O,O,O,W),
    (W,O,O,O,O,O,W),
    (W,O,O,O,O,O,W),
    (W,W,N,N,N,W,W),
)
E_ROOM = (
    (W,W,W,W,W,W,W),
    (W,O,O,O,O,O,W),
    (W,O,O,O,O,O,N),
    (W,O,O,O,O,O,N),
    (W,O,O,O,O,O,N),
    (W,O,O,O,O,O,W),
    (W,W,W,W,W,W,W)
)
W_ROOM = (
    (W,W,W,W,W,W,W),
    (W,O,O,O,O,O,W),
    (N,O,O,O,O,O,W),
    (N,O,O,O,O,O,W),
    (N,O,O,O,O,O,W),
    (W,O,O,O,O,O,W),
    (W,W,W,W,W,W,W)
)

NEIGHBOUR_OFFSETS = ((1,0), (0,1), (-1,0), (0,-1))

ROOMS = {
    "OPEN_ROOM" : (OPEN_TEMPLATE,["north","south","west","east"],["MUST-CONNECT"]),
    "CORNED_ROOM": (CORNED_ROOM_TEMPLATE,["north","south","west","east"],["MUST-CONNECT"]),
    "NS_CORRIDOR": (NS_CORRIDOR, ["north","south"], ["MUST-CONNECT"]),
    "WE_CORRIDOR": (WE_CORRIDOR, ["west","east"], ["MUST-CONNECT"]),
    "NE_CORNER": (NE_CORNER, ["north","east"], ["MUST-CONNECT"]),
    "SE_CORNER": (SE_CORNER, ["south","east"], ["MUST-CONNECT"]),
    "NW_CORNER": (NW_CORNER, ["north","west"], ["MUST-CONNECT"]),
    "SW_CORNER": (SW_CORNER, ["south","west"], ["MUST-CONNECT"]),
    "NES_CROSSROAD":(NES_CROSSROAD, ["north","south","east"], ["MUST-CONNECT"]),
    "NWS_CROSSROAD":(NWS_CROSSROAD, ["north","south","west"], ["MUST-CONNECT"]),
    "ESW_CROSSROAD":(ESW_CROSSROAD, ["east","south","west"], ["MUST-CONNECT"]),
    "NEW_CROSSROAD":(NEW_CROSSROAD, ["east","north","west"], ["MUST-CONNECT"]),
    "N_ROOM":(N_ROOM, ["north"], ["MUST-CONNECT"]),
    "E_ROOM":(E_ROOM, ["east"], ["MUST-CONNECT"]),
    "S_ROOM":(S_ROOM, ["south"], ["MUST-CONNECT"]),
    "W_ROOM":(W_ROOM, ["west"], ["MUST-CONNECT"]),
    "EMPTY_ROOM":(EMPTY_ROOM, ["north","south","west","east"],["MUST-CONNECT"]),
    "EMPTY2_ROOM":(EMPTY2_ROOM, ["north","south","west","east"],["MUST-CONNECT"]),
    
}

MODELS = loadModels()
ENTITY_NAMES = [
    "Shadow"
]

game_info = {
    "Level":0
}
