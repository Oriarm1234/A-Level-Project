import glob
import pygame

class Model:
    def __init__(self, name, variation, images:dict):
        self.images = images
        self.name = name
        self.variation = variation

class Tile:
    def __init__(self, x, y, model = {}, variation = 0):
        self.x = x
        self.y = y

        self.model = model
        self.variation = variation
        