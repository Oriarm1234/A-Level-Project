import sys
import pygame
arguments = sys.argv[1:]

arguments = [*arguments, "Images\\Player\\Idle\\Idle.txt"]

def getFilePath(fileName):
    name = fileName.split("\\")[-1].split("/")[-1]
    
    path = fileName[::-1].replace(name[::-1],"", 1)[::-1]
    
    return path

for fileName in arguments:
    
    with open(fileName, "r") as file:
        contents = file.read().split("\n")
        voxels = {}
        for line in contents:
            if line.startswith("#"):
                continue
            
            
            if line.count(" ") == 3:
                x,y,z,hexColour = line.split(" ")
                
                r = int(hexColour[:2], 16)
                g = int(hexColour[2:4], 16)
                b = int(hexColour[4:6], 16)
                
                voxels[(int(x),int(y),int(z))] = (r,g,b)
                
            
        
        minPoint = min(voxels,key=lambda x: x[0])[0],min(voxels,key=lambda x: x[1])[1],min(voxels,key=lambda x: x[2])[2]
        maxPoint = max(voxels,key=lambda x: x[0])[0],max(voxels,key=lambda x: x[1])[1],max(voxels,key=lambda x: x[2])[2]
        
        xOffSet = maxPoint[0] - minPoint[0]
        yOffset = maxPoint[1] - minPoint[1]
        zOffset = abs(maxPoint[2] - minPoint[2])
        
        surfaces = {}
        
        for i in range(zOffset+1):
            print(i,type(i),zOffset+1)
            surfaces[i] = pygame.Surface((abs(xOffSet)+1, abs(yOffset)+1), pygame.SRCALPHA)
        
        print(maxPoint[2], minPoint[1])
        for i in range(zOffset+1):
            
        
            for coord in voxels:
                x,y,z = coord
                
                colour = voxels[coord]
                
                surfaces[z].set_at((x-minPoint[0],y-minPoint[1]), colour)
        
        for i,surface in list(surfaces.items()):
            pygame.image.save(surface, getFilePath(fileName) + str(i)+".png")