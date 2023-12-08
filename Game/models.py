import pygame
import glob
import DungeonTiles

def loadModels(models = {}):
    files = glob.glob("Images\\**\\*.png", recursive=True)

    for fileName in files:
        
        dictionaryLocation = fileName.split("\\")[1:][:-1]
        imageLayer = fileName.split("\\")[-1].split(".")[0]
        variation = dictionaryLocation.pop()
        modelName = dictionaryLocation.pop()
        if modelName not in models:
            models[modelName] = DungeonTiles.Model(modelName,variation, {})
            
        
        try:
            
            imageLayer = int(imageLayer)
            variation = int(variation) if variation.isnumeric() else variation
            
            img = pygame.image.load(fileName)
            
            models[modelName].images[variation] = models[modelName].images.get(variation, {})
            
            models[modelName].images[variation][imageLayer] = img
            
            
            
            
            
        except:
            input("Bad Image, BURN " + fileName)
            
    for modelName, model in models.items():
        for varationKey, variation in model.images.items():
            
            model.images[varationKey] = dict([imgKey, variation[imgKey]] for imgKey in sorted(variation))
            
    return models
