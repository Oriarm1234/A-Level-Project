import glob
import pygame
import Definitions

class Model:
    def __init__(self, images:dict):
        self.images = images

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.model = {}
        self.variation = '0'
