from room import Room
import math
import random

class Dungeon:
    def __init__(self, x, y, minRooms, maxRooms, rating = 0, loot = 0):
        self.x = x
        self.y = y
        self.minRooms = minRooms
        self.maxRooms = maxRooms
        self.rooms = {}
        self.starterRoom = [0,0]
        self.generate()
        
    def generate(self):
        
        sides = {"north":(0,-1),"east":(1,0),"south":(0,1),"west":(-1,0)}
        oppositeSide = {"north":"south",
                        "east":"west",
                        "south":"north",
                        "west":"east"}
        self.roomAmount = random.randint(self.minRooms, self.maxRooms)
        self.bossAmount = math.log2(self.roomAmount)

        rooms = {tuple(self.starterRoom):set()}
        
        generatedAmount = 0
        
        currentRoom = list(self.starterRoom)
        
        changeFocusChance = 0.7
        changeFocusEntirelyChance = 0.2
        
        while generatedAmount < self.roomAmount:
            
            sidesTaken = rooms[tuple(currentRoom)]
            
            if len(sidesTaken) == 4 or random.randint(0,10)/10 <= changeFocusChance:
                chosenSide = random.choice(list(sides))
                
                
                rooms[tuple(currentRoom)].add(chosenSide)
                
                
                currentRoom[0] += sides[chosenSide][0]
                currentRoom[1] += sides[chosenSide][1]
                
                rooms[tuple(currentRoom)] = rooms.get(tuple(currentRoom), set())
                rooms[tuple(currentRoom)].add(oppositeSide[chosenSide])
                
                
                generatedAmount += 1
                continue
            elif random.randint(0,10)/10 <= changeFocusEntirelyChance:
                
                currentRoom = random.choice(list(rooms))
                continue
        
        self.rooms = {}
        self.currentLootRooms = 0
        self.currentBossRooms = 0
        
        for room in rooms:
            room:tuple[int, int]
            self.rooms[room] = Room(*room, self)

        
            
            
            
            
            
        
d = Dungeon(0,0,6,12,0,0)
