from .room import Room
import math
import random
from . import Definitions

sides = {"north":(0,-1),"east":(1,0),"south":(0,1),"west":(-1,0)}
oppositeSide = {"north":"south",
                "east":"west",
                "south":"north",
                "west":"east"}

def get_suitable_room_shape(
        sides: list[str], 
        bannedRooms: list[str]|tuple[str,...] = []
        
    ) -> tuple[str, tuple[tuple[int, ...], ...]]:
    """
    Parameters:
        sides:
            A list containing strings, these strings can be any of the below:
                north,
                south,
                west,
                east
        bannedRooms:
            A list containing the name of room templates that shouldnt be considered for this spot:
                For example:
                    ["OPEN_ROOM", "NE_CORNER"]
        
    Function:
        Will go through the various types of rooms defined in Definitions.py (Definitions.ROOMS)
        and will get a list of rooms that match the surroundings and arent banned.
        It will then randomly select a room and return it, this room will be placed in the dungeon
        
    Output:
        Tuple -> (Rooms Name: string,
                  Rooms Template: tuple[tuple[int]])
    """
    
    suitableShapes = []
    
    
    #Iterate through all room types stored in Defintions.py
    for roomName in Definitions.ROOMS:
        
        room,roomSides,tags = Definitions.ROOMS[roomName] #Info about current room type
        
        # Suitable if the current room type has the sides we want it to
        # But only if it needs those sides ("MUST-CONNECT" will be in tags if it needs those sides)
        # Otherwise if it doesnt have the tag, it will always be suitable [NOT RECOMMENDED]
        suitable = sorted(roomSides) == sorted(sides) or "MUST-CONNECT" not in tags

        if suitable and roomName not in bannedRooms: # Check if it is allowed and suitable
            suitableShapes.append(roomName)
        
    
    if len(suitableShapes) == 0:
        input("NO ROOM FOR SIDES: " + str(sides)) #* MESSAGE BEFORE ERROR IN CASE A SITUATION HASNT BEEN ACCOUNTED FOR
    
    shape = random.choice(suitableShapes)
    
    
    return shape, Definitions.ROOMS[shape][0]


def generate_tiles(dungeon):
    dungeon.maxZoneId = 0
    dungeon.rooms = {}
    dungeon.tiles = {}
    
    
    lockedRooms = {}
    dungeon.roomAmount = random.randint(dungeon.minRooms, dungeon.maxRooms)
    dungeon.bossAmount = math.log2(dungeon.roomAmount)
    
    

    rooms = {tuple(dungeon.starterRoom):set()}
    
    generatedAmount = 1
    
    currentRoom = list(dungeon.starterRoom)
    
    changeFocusChance = 1
    changeFocusEntirelyChance = 0.8
    isLockedChance = 0.3
    lockedAmountThreshold = 0.1
    
    genData = {tuple(currentRoom):{
        "id":0,
        "locked":False,
        "zoneId":0
    }}
    
    while generatedAmount < dungeon.roomAmount:
        
        sidesTaken = rooms[tuple(currentRoom)]
        
        
        if (len(sidesTaken) >= 2 and genData[tuple(currentRoom)]["locked"]):
            currentRoom = list(random.choice(list(rooms)))
            continue
        
        dungeon.maxZoneId = max(dungeon.maxZoneId, genData[tuple(currentRoom)]["zoneId"])
        
        if genData[tuple(currentRoom)]["locked"] and currentRoom not in lockedRooms.get(genData[tuple(currentRoom)]["zoneId"], []):
            
            lockedLevel = lockedRooms.get(genData[tuple(currentRoom)]["zoneId"], [])
            lockedLevel.append(currentRoom)
            
            lockedRooms[genData[tuple(currentRoom)]["zoneId"]] = lockedLevel
            
        
        if (len(sidesTaken) == 4 or random.randint(0,10)/10 <= changeFocusChance):
            chosenSide = random.choice(list(sides))
            
            if (currentRoom[0] + sides[chosenSide][0], currentRoom[1] + sides[chosenSide][1]) in genData:
                newSide = genData[(currentRoom[0] + sides[chosenSide][0], currentRoom[1] + sides[chosenSide][1])]
                
                if newSide["locked"] or newSide["zoneId"] != genData[tuple(currentRoom)]["zoneId"]:
                    
                    currentRoom = list(random.choice(list(rooms)))
                    continue
            
            rooms[tuple(currentRoom)].add(chosenSide)
            
            newRoom = [0,0]
            newRoom[0] = currentRoom[0] + sides[chosenSide][0]
            newRoom[1] = currentRoom[1] + sides[chosenSide][1]
            
            if tuple(newRoom) not in genData:
                if genData[tuple(currentRoom)]["locked"]:
                    locked = False
                else:
                    locked =  random.randint(0,10)/10 <= isLockedChance if generatedAmount > dungeon.roomAmount*lockedAmountThreshold else False
                
                if locked:
                    newZoneId = (genData[tuple(currentRoom)]["zoneId"],dungeon.maxZoneId)[random.randint(0,1)] + 1
                else:
                    newZoneId = genData[tuple(currentRoom)]["zoneId"]
                
                genData[tuple(newRoom)] = {"id":generatedAmount,
                                                
                                                "locked": locked,
                                                "zoneId":  newZoneId}
                generatedAmount += 1
                
            


            rooms[tuple(newRoom)] = rooms.get(tuple(newRoom), set())
            rooms[tuple(newRoom)].add(oppositeSide[chosenSide])
            
            currentRoom = newRoom
            
            
            continue
        elif random.randint(0,10)/10 <= changeFocusEntirelyChance and rooms.get(tuple(currentRoom)) is not None:
            
            currentRoom = list(random.choice(list(rooms)))
            continue
            
        else:
            newSides = [side for side in sides if side not in sidesTaken]
            chosenSide = random.choice(newSides)
            
            if (currentRoom[0] + sides[chosenSide][0], currentRoom[1] + sides[chosenSide][1]) in genData and\
              genData[(currentRoom[0] + sides[chosenSide][0], currentRoom[1] + sides[chosenSide][1])]["locked"]:
                currentRoom = list(random.choice(list(rooms)))
                continue
            
            rooms[tuple(currentRoom)].add(chosenSide)
            newRoom = [0,0]
            newRoom[0] = sides[chosenSide][0] + currentRoom[0]
            newRoom[1] = sides[chosenSide][1] + currentRoom[1]
    
            
            if tuple(newRoom) not in genData:
                if genData[tuple(currentRoom)]["locked"]:
                    locked = False
                else:
                    locked =  random.randint(0,10)/10 <= isLockedChance if generatedAmount > dungeon.roomAmount*lockedAmountThreshold else False
                
                if locked:
                    newZoneId = (genData[tuple(currentRoom)]["zoneId"],dungeon.maxZoneId)[random.randint(0,1)] + 1
                else:
                    newZoneId = genData[tuple(currentRoom)]["zoneId"]
                
                genData[tuple(newRoom)] = {"id":generatedAmount,
                                                
                                                "locked":locked,
                                                "zoneId": newZoneId}

                generatedAmount += 1
            rooms[tuple(newRoom)] = rooms.get(tuple(newRoom), set())
            rooms[tuple(newRoom)].add(oppositeSide[chosenSide])
            
            
            
    
    dungeon.currentLootRooms = 0
    dungeon.currentBossRooms = 0
    for room in rooms:
            
        room:tuple[int, int]
        
        data = genData.get(room, {"id":-1,"locked":False, "zoneId":0})
        id = data["id"]
        locked = data["locked"]
        zoneId = data["zoneId"]
        roomSides = rooms[room]
        
        bannedRooms = []
        
        if room == (0,0):
            bannedRooms.append("OPEN_ROOM")
        
        dungeon.rooms[room] = Room(*room, dungeon, sides = rooms[room], 
                                   shape = get_suitable_room_shape(rooms[room], bannedRooms), 
                                   id = id, locked = locked, zoneId = zoneId)

        dungeon.levels[zoneId] = dungeon.levels.get(zoneId, [])
        dungeon.levels[zoneId].append(dungeon.rooms[room])
        
    for room in dungeon.rooms:
        sideRooms = {}
        
        for side in dungeon.rooms[room].sides:
            x,y = sides[side]
            
            sideRooms[side] = dungeon.rooms.get((x+room[0], y+room[1]))
            
            if sideRooms[side]:
                
                match side:
                    case "north":
                        for tileCoord in dungeon.rooms[room].shape:
                            if tileCoord[1] - dungeon.rooms[room].y*Definitions.ROOM_SIZE[1] == 0: #adjacent to north room
                                tile = dungeon.rooms[room].shape[tileCoord]
                                
                                if Definitions.TILE_NAMES[tile] == "CONDITIONAL_DOOR":
                                    dungeon.rooms[room].shape[tileCoord] = Definitions.TILE_TYPES["DOOR"]
                                    
                    case "east":
                        for tileCoord in dungeon.rooms[room].shape:
                            if tileCoord[0] - dungeon.rooms[room].x*Definitions.ROOM_SIZE[0] == Definitions.ROOM_SIZE[0]-1: #adjacent to north room
                                tile = dungeon.rooms[room].shape[tileCoord]
                                
                                if Definitions.TILE_NAMES[tile] == "CONDITIONAL_DOOR":
                                    dungeon.rooms[room].shape[tileCoord] = Definitions.TILE_TYPES["DOOR"]
                    
                    case "south":
                        for tileCoord in dungeon.rooms[room].shape:
                            if tileCoord[1] - dungeon.rooms[room].y*Definitions.ROOM_SIZE[1] == Definitions.ROOM_SIZE[1]-1: #adjacent to north room
                                tile = dungeon.rooms[room].shape[tileCoord]
                                
                                if Definitions.TILE_NAMES[tile] == "CONDITIONAL_DOOR":
                                    dungeon.rooms[room].shape[tileCoord] = Definitions.TILE_TYPES["DOOR"]
                    
                    case "west":
                        for tileCoord in dungeon.rooms[room].shape:
                            if tileCoord[0] - dungeon.rooms[room].x*Definitions.ROOM_SIZE[0] == 0: #adjacent to north room
                                tile = dungeon.rooms[room].shape[tileCoord]
                                
                                if Definitions.TILE_NAMES[tile] == "CONDITIONAL_DOOR":
                                    dungeon.rooms[room].shape[tileCoord] = Definitions.TILE_TYPES["DOOR"]
                                
                                
            
            
        dungeon.rooms[room].sideRooms = sideRooms
        
        dungeon.tiles.update(dungeon.rooms[room].shape)
    
    
    for coord in dungeon.tiles:
        
        for neighbourCoord in Definitions.NEIGHBOUR_OFFSETS:
            
            i = coord[0] + neighbourCoord[0]
            j = coord[1] + neighbourCoord[1]
            
            if (i,j) not in dungeon.tiles and dungeon.tiles[coord] != Definitions.TILE_TYPES == "VOID":
                dungeon.tiles[coord] = Definitions.TILE_TYPES["WALL"]