import random
from Game.Dungeon import *         
            
            
dung = Dungeon(0,0,150,300,0,0)

for i in range(40):
    
    room = random.choice(list(dung.rooms))
    badGuy = Shadow(room[0]*7+random.randint(0,6),room[1]*7+random.randint(0,6),0,"Shadow",1,10,10,dung,dung.rooms[room],"Frame0",dung.rooms[room].zoneId)
    badGuy.movementType = 0

    

x1,y1 = 1,1

currentRoom = dung.rooms[(0,0)]


layers = dung.get_layers(Definitions.SCREEN_SIZE, (x1,y1))
screen = pygame.display.set_mode(Definitions.SCREEN_SIZE)
angle = 0
clock = pygame.time.Clock()

moving = False

beenIn = []#




while True:
    deltaTime = clock.tick(200)/1000
    events=pygame.event.get()
    keys = pygame.key.get_pressed()
    
    w,d,s,a = keys[pygame.K_w],keys[pygame.K_d],keys[pygame.K_s],keys[pygame.K_a]
    
    if w and not moving:
        #if "north" in currentRoom.sideRooms:
            currentRoom = currentRoom.sideRooms.get("north", currentRoom)
            
            
            
            y1+=1*deltaTime
            
            layers = dung.get_layers(Definitions.SCREEN_SIZE, (x1,y1))
            
            if currentRoom not in beenIn:
                beenIn.append(currentRoom)
        
    if d and not moving:
        #if "east" in currentRoom.sideRooms:
            currentRoom = currentRoom.sideRooms.get("east", currentRoom)
            
            x1-=1*deltaTime
            
            
            layers = dung.get_layers(Definitions.SCREEN_SIZE, (x1,y1))
            
            if currentRoom not in beenIn:
                beenIn.append(currentRoom)
    
    if s and not moving:
        #if "south" in currentRoom.sideRooms:
            currentRoom = currentRoom.sideRooms.get("south", currentRoom)
            
            y1-=1*deltaTime
            
            layers = dung.get_layers(Definitions.SCREEN_SIZE, (x1,y1))
            
            if currentRoom not in beenIn:
                beenIn.append(currentRoom)
        
    if a and not moving:
       # if "west" in currentRoom.sideRooms:
            currentRoom = currentRoom.sideRooms.get("west", currentRoom)
            
            x1+=1*deltaTime
            
            layers = dung.get_layers(Definitions.SCREEN_SIZE, (x1,y1))
            
            if currentRoom not in beenIn:
                beenIn.append(currentRoom)
        
    if (not (w or d or s or a)) and moving:
        moving = False
        
    entityLayers = {}
    for room in dung.rooms:
        x,y = room  
        
        
        distance = ((x - currentRoom.x)**2 + (y - currentRoom.y)**2)**0.5
        
        if distance <= 4:
            roomObj = dung.rooms[room]
            for ai in roomObj.entities:
                ai.playerX = currentRoom.x*7
                ai.playerY = currentRoom.y*7
                ai.update()    
            
            for layer in roomObj.entityLayers:
                entityLayers[layer] = entityLayers.get(layer,[])
                entityLayers[layer].append(roomObj.entityLayers[layer])
                
    

    
    
    pygame.display.set_caption(str(clock.get_fps()))
    
        
    
    #
    
    
    screen.fill((0,0,0))
    
    for id,layerIndex in enumerate(layers):

        for index in layers[layerIndex]:
            size = currentRoom.screenRoomSize
            modifier = size[1] / Definitions.SCREEN_SIZE[1]
            layer = layers[layerIndex][index]
            
            screen.blit(layer, (Definitions.SCREEN_SIZE[0]//2-layer.get_width()/2+(-index-layerIndex)/8,Definitions.SCREEN_SIZE[1]//2-layer.get_height()/2+(-index-layerIndex)))

            
            Zvalue = index+layerIndex+id
            
            if Zvalue in entityLayers:
                for entitys in entityLayers[Zvalue]:
                    for entity in entitys:
                        
                        x,y = entity.x, entity.y
                        
                        drawCoord = (x+.5+int(x1*7))*Definitions.GRID_SQUARE_WIDTH,(y+.5+int(y1*7))*Definitions.GRID_SQUARE_HEIGHT

                        
                        screen.blit(Definitions.MODELS[entity.spriteName].images[entity.frame][Zvalue-(Definitions.FLOOR_HEIGHT + 1)],drawCoord)
                        
                        
                    
            

                    
    for room in dung.rooms:
        x,y = room
        
        
        colour = (255,255,255)
        
        if dung.rooms[room] != currentRoom:
            if dung.rooms[room].locked:
                colour = (165,165,165)
            
            else:
                if dung.rooms[room] not in beenIn:
                    colour = (int(255/dung.maxZoneId*dung.rooms[room].zoneId),0,0)
                else:
                    colour = (0,0,255)
            
            colour = (int(255/dung.maxZoneId*dung.rooms[room].zoneId),0,0)
        else:
            colour = (0,255,0)
            
        pygame.draw.circle(screen, colour, (x*10+currentRoom.screenRoomSize[0]//2, y*10+currentRoom.screenRoomSize[1]//2), 5)
    
                
            
    
    #screen.blit(Definitions.FOG_OF_WAR_IMAGE,fogOfWarCenterPos)
    pygame.display.update()