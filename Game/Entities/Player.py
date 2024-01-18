import math
import pygame
from .Entity import Entity

class Player(Entity):
    
    controlling = None
    
    def __init__(self, x, y, currentAngleStep, spriteName, walkSpeed):
        super().__init__(x, y, currentAngleStep, spriteName, walkSpeed)
        

