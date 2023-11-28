import pygame
import glob
import json
from models import loadModels
GRID_SQUARE_WIDTH = 32
GRID_SQUARE_HEIGHT = 32
SMALL_ROOM = (11,11)
MEDIUM_ROOM = (17,17)
LARGE_ROOM = (29,29)
SIZES = {"small": SMALL_ROOM, 
         "medium":MEDIUM_ROOM,
         "large":LARGE_ROOM}

MODELS = loadModels()

