import math
import pygame
import random
import Definitions
import Timer
class Entity:
    """
    Walk speed is tile per second
    """
    All = {}
    currentId = 0
    sprites = {} #name-layer-sprite
    maxAngles = 16
    spriteAngles = {}
    angleStep = 2*math.pi / maxAngles

    
    @classmethod
    def initiate_sprite(cls, name, spriteLayers):
        for layer in spriteLayers:
            for angle in range(cls.maxAngles):
                cls.spriteAngles[name] = cls.spriteAngles.get(name, {})
                cls.spriteAngles[name][layer] = cls.spriteAngles.get(layer, {})
                cls.spriteAngles[name][layer][angle] = pygame.transform.rotate(spriteLayers[layer], cls.angleStep * angle)
            
    
    def __init__(self, x, y, currentAngleStep, spriteName, walkSpeed, maxHealth, health,z=Definitions.FLOOR_HEIGHT + 1):
        self.id = Entity.currentId
        Entity.currentId += 1
        self.walkSpeed = walkSpeed
        self.maxHealth = maxHealth
        self.health = health
        self.x = x
        self.y = y
        self.z = z
        self.angle = currentAngleStep*Entity.angleStep
        self.currentAngleStep = currentAngleStep
        self.inventory = {}
        self.spriteName = spriteName
        Entity.All[self.id] = self
        
        
class ASTARTarget:
    __className__ = "ASTARTarget"

class TeleportTarget:
    __className__ = "ASTARTarget"
    def __init__(self, coord, active,room):
        self.coord = coord
        self.active = active
        self.room = room
        
class AI(Entity):
    layers = {}
    All = {}
    Moving = {}
    currentId = 0
    
    def __init__(self, x, y, currentAngleStep, spriteName, walkSpeed, maxHealth, health, dungeon, spawnRoom, frame,  dungeonLevel=0,z=Definitions.FLOOR_HEIGHT + 1):
        super().__init__(x, y, currentAngleStep, spriteName, walkSpeed,maxHealth,health,z)
        self.frame = frame
        self.id = AI.currentId
        AI.currentId += 1
        AI.All[self.id] = self
        if self not in spawnRoom.entities:
            spawnRoom.entities.append(self)
        self.dungeon = dungeon
        self.dungeonLevel = dungeonLevel
        self.currentTarget = None
        self._room = spawnRoom
        self.moveTimer = None
        self.outOfRange=True
        self.playerX = 0
        self.playerY = 0
        self.staticPeriod = [7,16] # static period, how long to stay still after teleporting # random -> [min,max]
        self._movementType =0
        self.movementType = 0 # movementType: -1=stay in spawn room never been visible, 0=shift between connected rooms randomly, 1=VisibleToPlayer wander around room, 2=attacking player, 3=scared, run away from player
        for layerNum in Definitions.MODELS[spriteName].images[self.frame]:
            if self.room is not None:
                spawnRoom.entityLayers[layerNum + Definitions.FLOOR_HEIGHT + 1] = self.room.entityLayers.get(layerNum + Definitions.FLOOR_HEIGHT + 1,[])
                spawnRoom.entityLayers[layerNum + Definitions.FLOOR_HEIGHT + 1].append(self)
    @property
    def room(self):
        return self._room
    
    @room.setter
    def room(self,value):
        for layerNum in Definitions.MODELS[self.spriteName].images[self.frame]:
            if layerNum + Definitions.FLOOR_HEIGHT + 1 in self._room.entityLayers and self in self._room.entityLayers[layerNum + Definitions.FLOOR_HEIGHT + 1]:
                self._room.entityLayers[layerNum + Definitions.FLOOR_HEIGHT + 1].remove(self)
                
            if value is not None:
                
                value.entityLayers[layerNum + Definitions.FLOOR_HEIGHT + 1] = value.entityLayers.get(layerNum + Definitions.FLOOR_HEIGHT + 1, [])
                
                if self not in value.entityLayers[layerNum + Definitions.FLOOR_HEIGHT + 1]:
                    value.entityLayers[layerNum + Definitions.FLOOR_HEIGHT + 1].append(self)

                
        self._room = value
        
        
    
    
    @property
    def movementType(self):
        return self._movementType
    
    @movementType.setter
    def movementType(self, value):
        AI.Moving[self._movementType] = AI.Moving.get(self._movementType,[])
        AI.Moving[value] = AI.Moving.get(value,[])
        
        if self in AI.Moving[self._movementType]:
            AI.Moving[self._movementType].remove(self)
            
        self._movementType = value
        AI.Moving[self._movementType].append(self)
        
        
    def moveTo(self,x,y):
        roomCoord = (int(x//7),int(y//7))
        if (self.room.x,self.room.y) != roomCoord and roomCoord in self.dungeon.rooms:
            if self in self.room.entities:
                self.room.entities.remove(self)
            
            self.room = self.dungeon.rooms[roomCoord]
            
            if self not in self.room.entities:
                self.room.entities.append(self)
        
        self.x = x
        self.y = y
        
    
    def targetActivation(self, activated):
        if self.currentTarget is not None:
            self.currentTarget.active = activated

    def chooseTarget(self):
        if self.movementType == -1:
            self.currentTarget = None
            return False
          
        elif self.movementType == 0: #Logical Teleportation
            
            
            
            selectedRoom = self.room.sideRooms[random.choice(list(self.room.sideRooms))]
            
            if random.randint(0,len(self.room.sideRooms)) == 0:
                selectedRoom = self.room
            
            if selectedRoom.locked and selectedRoom != self.room:
                self.currentTarget = None
                return False
            
            
            possibleTargets = []
            
            for coord in selectedRoom.shape:
                tileType = selectedRoom.shape[coord]
                if tileType == Definitions.TILE_TYPES["FLOOR"]:
                    possibleTargets.append(coord)
            
            if len(possibleTargets) == 0:
                self.currentTarget = None
                return False
            
            chosenCoord = random.choice(possibleTargets)
            
            distanceToTravel = ((self.x-chosenCoord[0])**2 + (self.y-chosenCoord[1])**2)**0.5
            walkTime = distanceToTravel/self.walkSpeed
            
            self.moveTimer = Timer.Timer(walkTime)
            self.moveTimer.name = "Walking"
            
            self.currentTarget = TeleportTarget(chosenCoord, False, selectedRoom)
            
            self.moveTimer.on_completion = self.targetActivation
            self.moveTimer.completionArgs = [True]
            self.moveTimer.begin()
    
    def distance_to_player(self):
        
        if self.dungeon.player != None:
            self.playerX = self.dungeon.player.x
            self.playerY = self.dungeon.player.y
        
        return ((self.x-self.playerX)**2 + (self.y-self.playerY)**2)**0.5
    
    def update(self):
        #join thread if done
        
        
        
        
        if type(self.currentTarget) is TeleportTarget and self.currentTarget.active:
            self.moveTo(*self.currentTarget.coord)
            
            self.room = self.currentTarget.room
            
            self.currentTarget = None
            
        if self.moveTimer is not None and self.moveTimer.complete:
            self.moveTimer = None
        
        if self.distance_to_player() < 40:
            if self not in AI.Moving[self._movementType]:
                AI.Moving[self._movementType].append(self)
            self.outOfRange = False
            if self.currentTarget == None and self.moveTimer == None:
                
                    
                
                self.moveTimer = Timer.Timer(random.randint(*self.staticPeriod))
                self.moveTimer.name = "Waiting"
                self.moveTimer.completionArgs = []
                self.moveTimer.on_completion = self.chooseTarget
                self.moveTimer.begin()
        else:
            if self in AI.Moving[self._movementType]:
                AI.Moving[self._movementType].remove(self)
            self.outOfRange=True
            
            
            
            
class Shadow(AI):
    def __init__(self, x, y, currentAngleStep, spriteName, walkSpeed, maxHealth, health, dungeon, spawnRoom, frame="Frame0", dungeonLevel=0,z=Definitions.FLOOR_HEIGHT + 1):
        super().__init__(x, y, currentAngleStep, spriteName, walkSpeed, maxHealth, health, dungeon, spawnRoom, frame, dungeonLevel,z)
        
        
            
            

            
                    
            

        
        
        

        
        