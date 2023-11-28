import pygame
import glob
import DungeonTiles

def loadModels(models = {}):
    files = glob.glob("Images\\**\\*.png", recursive=True)

    allModels = {}

    for fileName in files:
        
        dictionaryLocation = fileName.split("\\")[1:][:-1]
        variation = dictionaryLocation.pop()
        name = dictionaryLocation.pop()
        
        model = DungeonTiles.Model({})
        
        try:
            img = pygame.image.load(fileName)
            
            model.images[variation] = model.images.get(variation, [])
            
            
            
            
            
        except:
            currentLevel[loc].append(None)
            
    return models
            
